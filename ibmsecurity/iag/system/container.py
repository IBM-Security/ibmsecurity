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
import yaml

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
    import uuid
else:
    import docker

class VersionException(Exception):
    """
    This exception will be raised if the configuration version is greater 
    than the version of the IAG container.
    """
    pass

class Container(object):
    """
    This class is used to manage the IAG container.  It will
    essentially allow you to start and stop IAG containers with
    the specified configuration information.  It essence it is simply
    a wrapper to the service specific Container objects.
    """

    config_volume_path = "/var/iag/config"

    def __init__(self, config_file = None, volume = None):
        """
        Initialize this class.  Note that a VersionException will be raised
        if the version number contained within the configuration file is
        greater than the version number of the requested IAG image.
        """

        super(Container, self).__init__()

        # If a configuration file is specified we need to ensure that the
        # IAG version supports the version of the specified configuration
        # file.
        if config_file is not None:
            with open(config_file, 'r') as stream:
                data = yaml.safe_load(stream)

                if data['version'] > Environment().get("image.tag"):
                    raise VersionException(
                        "The configuration file is not supported "
                        "with the specified image version: {0}".format(
                            Environment().get("image.tag")))

        if run_kubernetes():
            self.client_ = KubernetesContainer(config_file)
        else:
            self.client_ = DockerContainer(config_file=config_file, volume=volume)

    def setEnv(self, name, value):
        """
        Set an environment variable which will be used when starting the
        IAG container.
        """

        self.client_.setEnv(name, value)

    def addSecretToEnv(self, name):
        """
        Make an pre-created secret available to the container as an
        environment variable.
        """

        self.client_.addSecretToEnv(name)

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
                        verify=False, allow_redirects=False, timeout=2)

                running = True
            except:
                self.client_.reload()
                attempt += 1

        if not running:
            message = "The container failed to start within the allocated time."
            logger.critical(message)

            logger.critical(self.client_.container_.logs())

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

    def __init__(self, config_file=None, volume=None):
        super(DockerContainer, self).__init__()

        self.env_       = {}
        self.cfgFile_   = config_file
        self.volume_    = volume
        self.client_    = docker.from_env()
        self.container_ = None

    def __del__(self):
        if (self.container_ is not None):
            self.container_.stop()
            self.container_.remove()

    def setEnv(self, name, value):
        """
        Set an environment variable which will be used when starting the
        IAG container.
        """
        self.env_[name] = value

    def addSecretToEnv(self, name):
        """
        Make an pre-created secret available to the container as an
        environment variable.  Please note that secrets are not
        supported under Docker and so we raise an Exception here.
        """
        raise Exception("Secrets are not supported under Docker.")

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
        if self.volume_ is not None:
            volumes.append("{0}:{1}".format(
                self.volume_, Container.config_volume_path))

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

    # The name of the key within the configuration map which holds our
    # configuration file.
    __config_map_key = "config.yaml"

    def __init__(self, config_file):
        super(KubernetesContainer, self).__init__()

        if "KUBERNETES_SERVICE_PORT" in os.environ:
            kubernetes.config.load_incluster_config()
        else:
            kubernetes.config.load_kube_config()

        self.env_            = []
        self.secrets_        = []
        self.config_file_    = config_file
        self.apps_api_       = kubernetes.client.AppsV1Api()
        self.core_api_       = kubernetes.client.CoreV1Api()
        self.namespace_      = Environment.get("kubernetes.namespace")
        self.port_           = None
        self.deploymentName_ = "iag-{0}".format(uuid.uuid1())
        self.configmapName_  = "iag.config.{0}".format(uuid.uuid1())

        logger.info("Using a kubernetes public IP of {0}.  Use the "
            "kubernetes.ip configuration entry to change the IP to suit "
            "your environment.".format(Environment.get("kubernetes.ip")))

    def setEnv(self, name, value):
        """
        Set an environment variable which will be used when starting the
        IAG container.
        """

        self.env_.append(kubernetes.client.V1EnvVar(
                            name  = name,
                            value = value))

    def addSecretToEnv(self, name):
        """
        Make an pre-created secret available to the container as
        environment variables.
        """

        self.secrets_.append(kubernetes.client.V1EnvFromSource(
                secret_ref = kubernetes.client.V1SecretEnvSource(
                    name = name
                )
        ))

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

        # If the configuration file has been specified we need to first
        # create the configmap.
        if self.config_file_ is not None:
            api_response = self.core_api_.create_namespaced_config_map(
                namespace = self.namespace_,
                body      = self.__createConfigMap()
            )

            logger.debug("ConfigMap created: status='{0}'".format(
                        api_response))

        # Create the deployment.
        deployment = self.__createDeploymentObject(image)

        api_response = self.apps_api_.create_namespaced_deployment(
            body      = deployment,
            namespace = self.namespace_)

        logger.debug("Deployment created: status='{0}'".format(
                        api_response.status))

        service_type = "ClusterIP" if "KUBERNETES_SERVICE_PORT" in os.environ \
                    else "NodePort"

        # Create the service.
        service = kubernetes.client.V1Service(
                    api_version = "v1",
                    kind        = "Service",
                    metadata    = kubernetes.client.V1ObjectMeta(
                        name = self.deploymentName_
                    ),
                    spec        = kubernetes.client.V1ServiceSpec(
                        type     = service_type,
                        selector = { "app" : self.deploymentName_ },
                        ports    = [ kubernetes.client.V1ServicePort(
                                port = 8443
                        )]
                    )
                )

        api_response = self.core_api_.create_namespaced_service(
                            body      = service,
                            namespace = self.namespace_)

        self.port_ = 8443 if "KUBERNETES_SERVICE_PORT" in os.environ \
                        else api_response.spec.ports[0].node_port

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

        return self.deploymentName_ if "KUBERNETES_SERVICE_PORT" in os.environ \
                else Environment.get("kubernetes.ip")

    def stopContainer(self):
        """
        The following command is used to stop the running IAG container.
        """

        if self.port_ is not None:
            logger.info("Stopping the deployment: {0}".format(
                                            self.deploymentName_))

            try: 
                # Grab the log file of the pod.  The first thing to do is 
                # determine the pod name, and then we can retrieve the log for 
                # the pod.
                api_response = self.core_api_.list_namespaced_pod(
                    self.namespace_,
                    label_selector = "app = {0}".format(self.deploymentName_))

                api_response = self.core_api_.read_namespaced_pod_log(
                                api_response.items[0].metadata.name, 
                                self.namespace_)

                logger.info("Container log: {0}".format(api_response))
            except kubernetes.client.rest.ApiException as e:
                logger.error(
                    "Failed to retrieve the log file from the pod: {0}".\
                    format(e))

            # Now we can delete the deployment and service.
            try:
                api_response = self.apps_api_.delete_namespaced_deployment(
                        name      = self.deploymentName_,
                        namespace = self.namespace_,
                        body      = kubernetes.client.V1DeleteOptions(
                            propagation_policy   = 'Foreground',
                            grace_period_seconds = 5
                        ))

                logger.debug("Deployment deleted: status={0}".format(
                                                api_response.status))
            except Exception as exc:
                logger.error(exc)
                

            try:
                api_response = self.core_api_.delete_namespaced_service(
                        name      = self.deploymentName_,
                        namespace = self.namespace_,
                        body      = kubernetes.client.V1DeleteOptions(
                            propagation_policy   = 'Foreground',
                            grace_period_seconds = 5
                        ))

                logger.debug("Service deleted: status={0}".format(
                                                api_response.status))
            except Exception as exc:
                logger.error(exc)

            # Delete the configmap.
            try:
                if self.config_file_ is not None:
                    api_response = self.core_api_.delete_namespaced_config_map(
                        name      = self.configmapName_,
                        namespace = self.namespace_,
                        body      = kubernetes.client.V1DeleteOptions(
                            propagation_policy   = 'Foreground',
                            grace_period_seconds = 5
                        ))

                    logger.debug("Configmap deleted: status={0}".format(
                                                api_response))
            except Exception as exc:
                logger.error(exc)

            self.port_ = None

    def __createDeploymentObject(self, image):
        """
        Create the deployment object for IAG.
        """

        # If a configuration file has been specified we want to mount the
        # configmap.
        volumes       = []
        volume_mounts = []

        if self.config_file_ is not None:
            volumes.append(kubernetes.client.V1Volume(
                    config_map = kubernetes.client.V1ConfigMapVolumeSource(
                            items = [
                                kubernetes.client.V1KeyToPath(
                                    path = "config.yaml",
                                    key  = self.__config_map_key
                                )
                            ],
                            name = self.configmapName_
                    ),
                    name = self.deploymentName_
            ))

            volume_mounts.append(kubernetes.client.V1VolumeMount(
                mount_path = Container.config_volume_path,
                name       = self.deploymentName_
            ))


        # Create the pod template container
        container = kubernetes.client.V1Container(
            name          = self.deploymentName_,
            image         = image,
            ports         = [
                    kubernetes.client.V1ContainerPort(container_port=8443)],
            env           = self.env_,
            volume_mounts = volume_mounts,
            env_from      = self.secrets_
        )

        # Create the secret which is used when pulling the IAG image.
        secret = kubernetes.client.V1LocalObjectReference(
                        name = Environment.get("kubernetes.image_pull_secret")
        )

        # Create and configurate a spec section
        template = kubernetes.client.V1PodTemplateSpec(
            metadata = kubernetes.client.V1ObjectMeta( 
                            labels = {"app": self.deploymentName_}),
            spec     = kubernetes.client.V1PodSpec(
                            containers         = [ container ],
                            image_pull_secrets = [ secret ],
                            volumes            = volumes )
        )

        # Create the specification of the deployment
        spec = kubernetes.client.V1DeploymentSpec(
            replicas = 1,
            template = template,
            selector = {'matchLabels': {'app': self.deploymentName_}}
        )

        # Instantiate the deployment object
        deployment = kubernetes.client.V1Deployment(
            api_version = "apps/v1",
            kind        = "Deployment",
            metadata    = kubernetes.client.V1ObjectMeta(
                                    name = self.deploymentName_),
            spec        = spec)

        return deployment

    def __createConfigMap(self):
        """
        Create the configuration map which holds the configuration file
        contents.
        """

        metadata = kubernetes.client.V1ObjectMeta(
            annotations                   = { 'app': self.deploymentName_ },
            deletion_grace_period_seconds = 30,
            labels                        = { 'app' : self.deploymentName_ },
            name                          = self.configmapName_,
            namespace                     = self.namespace_
        )

        # Get the file content.
        with open(self.config_file_, 'r') as f:
            file_content = f.read()

        # Instantiate the configmap object
        configmap = kubernetes.client.V1ConfigMap(
                        api_version = "v1",
                        kind        = "ConfigMap",
                        data        = { self.__config_map_key: file_content },
                        metadata    = metadata
                    )

        return configmap

