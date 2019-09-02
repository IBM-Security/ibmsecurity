"""
IBM Confidential
Object Code Only Source Materials
5725-V90
(c) Copyright International Business Machines Corp. 2020
The source code for this program is not published or otherwise divested
of its trade secrets, irrespective of what has been deposited with the
U.S. Copyright Office.
"""

import atexit
import logging
import time
import requests
import urllib3
import os

from ibmsecurity.iag.system.command     import Command
from ibmsecurity.iag.system.environment import Environment

logger = logging.getLogger(__name__)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def run_kubernetes():
    """
    Determine whether we are running in kubernetes or docker.
    """

    env_name = "CONTAINER_SERVICE"

    return env_name in os.environ and os.environ[env_name] == "kubernetes"

if run_kubernetes():
    import kubernetes
else:
    import docker

class Container(object):
    """
    This class is used to manage the IAG container.  It will
    essentially allow you to start and stop IAG containers with
    the specified configuration information.  It essence it is simply
    a wrapper to the service specific Container objects.
    """

    config_volume_path = "/var/iag/config"

    def __init__(self, config_file = None):
        super(Container, self).__init__()

        if run_kubernetes():
            self.client_ = KubernetesContainer()
        else:
            self.client_ = DockerContainer(config_file)

    def setEnv(self, name, value):
        """
        Set an environment variable which will be used when starting the
        IAG container.
        """

        self.client_.setEnv(name, value)

    def startContainer(self):
        """
        The following command is used to start the IAG container using the
        supplied configuration.
        """

        image  = "{0}:{1}".format(
                    Environment().get("image.name"),
                    Environment().get("image.tag"))

        logger.info("Starting the container from {0}".format(image))

        self.client_.startContainer(image)

        atexit.register(self.stopContainer)

        # Wait for the container to become healthy.  We should really be using
        # the health of the container, but this takes a while to kick in.  So,
        # we instead poll the https port of the server until we make a 
        # successful SSL connection.

        running = False
        attempt = 0

        while not running and attempt < 30:
            time.sleep(1)

            try:
                requests.get("https://{0}:{1}".format(
                        self.ipaddr(), self.port()), 
                        verify=False, allow_redirects=False)

                running = True
            except:
                self.client_.reload()
                attempt += 1

        if not running:
            message = "The container failed to start within the allocated time."
            logger.critical(message)

            raise Exception(message)

        logger.info("The container has started")

    def port(self):
        """
        Retrieve the port for the current running container.
        """

        return self.client_.port()

    def ipaddr(self):
        """
        Retrieve the IP address which can be used to access the container.
        """

        return self.client_.ipaddr()

    def stopContainer(self):
        """
        The following command is used to stop the running IAG container.
        """

        self.client_.stopContainer()

        atexit.unregister(self.stopContainer)

        logger.info("The container has stopped")

class DockerContainer(object):
    """
    This class is used to manage the IAG docker container.  It will
    essentially allow you to start and stop IAG docker containers with
    the specified configuration information.
    """

    def __init__(self, config_file):
        super(DockerContainer, self).__init__()

        self.env_       = {}
        self.cfgFile_   = config_file
        self.client_    = docker.from_env()
        self.container_ = None

    def setEnv(self, name, value):
        """
        Set an environment variable which will be used when starting the
        IAG container.
        """
        self.env_[name] = value

    def startContainer(self, image):
        """
        The following command is used to start the IAG container using the
        supplied configuration.
        """

        if self.container_ is not None:
            logger.critical(
                "A container has already been started in this object.")

            raise Exception(
                    "A container has already been started in this object.")

        volumes = []

        if self.cfgFile_ is not None:
            volumes.append("{0}:{1}/config.yaml".format(
                                self.cfgFile_, Container.config_volume_path))

        self.container_ = self.client_.containers.run(image, auto_remove=True, 
                                environment=self.env_, detach=True,
                                publish_all_ports=True,
                                volumes = volumes)

    def reload(self):
        """
        Reload the information associated with the container.
        """

        if self.container_ is None:
            logger.critical("Error> the container is not currently running!")

            raise Exception("The container is not currently running!")

        self.container_.reload()

    def port(self):
        """
        Retrieve the port for the current running container.
        """

        if self.container_ is None:
            logger.critical("Error> the container is not currently running!")

            raise Exception("The container is not currently running!")

        return self.container_.attrs['NetworkSettings']['Ports']['8443/tcp']\
                [0]['HostPort']

    def ipaddr(self):
        """
        Retrieve the IP address which can be used to access the container.
        """

        if self.container_ is None:
            logger.critical("Error> the container is not currently running!")

            raise Exception("The container is not currently running!")

        ipaddr = self.container_.attrs['NetworkSettings']['Ports']['8443/tcp']\
                [0]['HostIp']

        if ipaddr == "0.0.0.0":
            ipaddr = Environment.get("docker.ip")

        return ipaddr

    def stopContainer(self):
        """
        The following command is used to stop the running IAG container.
        """

        if self.container_ is not None:
            logger.info("Stopping the container: {0}".format(
                                            self.container_.name))
            logger.info("Container log: {0}".format(
                                    self.container_.logs().decode("utf-8")))

            self.container_.stop()

            self.container_ = None

class KubernetesContainer(object):
    """
    This class is used to manage the IAG Kubernetes container.  It will
    essentially allow you to start and stop IAG Kubernetes containers with
    the specified configuration information.
    """

    # The name of our deployment.
    __deploymentName = "iag-test"

    def __init__(self):
        super(KubernetesContainer, self).__init__()

        kubernetes.config.load_kube_config()

        self.env_       = []
        self.apps_api_  = kubernetes.client.AppsV1Api()
        self.core_api_  = kubernetes.client.CoreV1Api()
        self.namespace_ = Config.get("kubernetes.namespace")
        self.port_      = None

        logger.info("Using a kubernetes public IP of {0}.  Use the "
            "kubernetes.ip configuration entry to change the IP to suit "
            "your environment.".format(Config.get("kubernetes.ip")))

    def setEnv(self, name, value):
        """
        Set an environment variable which will be used when starting the
        IAG container.
        """

        self.env_.append(kubernetes.client.V1EnvVar(
                            name  = name,
                            value = value))

    def startContainer(self, image):
        """
        The following command is used to start the IAG container using the
        supplied configuration.
        """

        if self.port_ is not None:
            logger.critical(
                "A container has already been started in this object.")

            raise Exception(
                    "A container has already been started in this object.")

        # Create the deployment.
        deployment = self.__createDeploymentObject(image)

        api_response = self.apps_api_.create_namespaced_deployment(
            body      = deployment,
            namespace = self.namespace_)

        logger.debug("Deployment created: status='{0}'".format(
                        api_response.status))

        # Create the service.
        service = kubernetes.client.V1Service(
                    api_version = "v1",
                    kind        = "Service",
                    metadata    = kubernetes.client.V1ObjectMeta(
                        name = self.__deploymentName
                    ),
                    spec        = kubernetes.client.V1ServiceSpec(
                        type     = "NodePort",
                        selector = { "app" : self.__deploymentName },
                        ports    = [ kubernetes.client.V1ServicePort(
                                port = 8443
                        )]
                    )
                )

        api_response = self.core_api_.create_namespaced_service(
                            body      = service,
                            namespace = self.namespace_)

        self.port_ = api_response.spec.ports[0].node_port

        logger.debug("Service created: status='{0}'".format(
                        api_response.status))

    def reload(self):
        """
        Reload the information associated with the container.
        """

        # Nothing to do here.

    def port(self):
        """
        Retrieve the port for the current running container.
        """

        if self.port_ is None:
            logger.critical("Error> the container is not currently running!")

            raise Exception("The container is not currently running!")

        return self.port_

    def ipaddr(self):
        """
        Retrieve the IP address which can be used to access the container.
        """

        if self.port_ is None:
            logger.critical("Error> the container is not currently running!")

            raise Exception("The container is not currently running!")

        return Config.get("kubernetes.ip")

    def stopContainer(self):
        """
        The following command is used to stop the running IAG container.
        """

        if self.port_ is not None:
            logger.info("Stopping the deployment: {0}".format(
                                            self.__deploymentName))

            try: 
                # Grab the log file of the pod.  The first thing to do is 
                # determine the pod name, and then we can retrieve the log for 
                # the pod.
                api_response = self.core_api_.list_namespaced_pod(
                    self.namespace_,
                    label_selector = "app = {0}".format(self.__deploymentName))

                api_response = self.core_api_.read_namespaced_pod_log(
                                api_response.items[0].metadata.name, 
                                self.namespace_)

                logger.info("Container log: {0}".format(api_response))
            except kubernetes.client.rest.ApiException as e:
                logger.error(
                    "Failed to retrieve the log file from the pod: {0}".\
                    format(e))

            # Now we can delete the deployment and service.
            api_response = self.apps_api_.delete_namespaced_deployment(
                        name      = self.__deploymentName,
                        namespace = self.namespace_,
                        body      = kubernetes.client.V1DeleteOptions(
                            propagation_policy   = 'Foreground',
                            grace_period_seconds = 5
                        ))

            logger.debug("Deployment deleted: status={0}".format(
                                                api_response.status))

            api_response = self.core_api_.delete_namespaced_service(
                        name      = self.__deploymentName,
                        namespace = self.namespace_,
                        body      = kubernetes.client.V1DeleteOptions(
                            propagation_policy   = 'Foreground',
                            grace_period_seconds = 5
                        ))

            logger.debug("Service deleted: status={0}".format(
                                                api_response.status))

            self.port_ = None

    def __createDeploymentObject(self, image):

        # Create the pod template container
        container = kubernetes.client.V1Container(
            name  = self.__deploymentName,
            image = image,
            ports = [kubernetes.client.V1ContainerPort(container_port=8443)],
            env   = self.env_
        )

        # Create the secret which is used when pulling the IAG image.
        secret = kubernetes.client.V1LocalObjectReference(
                            name = Config.get("kubernetes.image_pull_secret")
        )

        # Create and configurate a spec section
        template = kubernetes.client.V1PodTemplateSpec(
            metadata = kubernetes.client.V1ObjectMeta( 
                            labels = {"app": self.__deploymentName}),
            spec     = kubernetes.client.V1PodSpec(
                            containers         = [ container ],
                            image_pull_secrets = [ secret ])
        )

        # Create the specification of the deployment
        spec = kubernetes.client.V1DeploymentSpec(
            replicas = 1,
            template = template,
            selector = {'matchLabels': {'app': self.__deploymentName}}
        )

        # Instantiate the deployment object
        deployment = kubernetes.client.V1Deployment(
            api_version = "apps/v1",
            kind        = "Deployment",
            metadata    = kubernetes.client.V1ObjectMeta(
                                    name = self.__deploymentName),
            spec        = spec)

        return deployment

