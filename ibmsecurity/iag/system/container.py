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
import docker
import time
import requests
import urllib3

from ibmsecurity.iag.system.command     import Command
from ibmsecurity.iag.system.environment import Environment

logger = logging.getLogger(__name__)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Container(object):
    """
    This class is used to manage the IAG docker container.  It will
    essentially allow you to start and stop IAG docker containers with
    the specified configuration information.
    """

    def __init__(self):
        super(Container, self).__init__()

        self.env_       = {}
        self.client_    = docker.from_env()
        self.container_ = None

    def setEnv(self, name, value):
        """
        Set an environment variable which will be used when starting the
        IAG container.
        """
        self.env_[name] = value


    def startContainer(self):
        """
        The following command is used to start the IAG container using the
        supplied configuration.
        """

        if self.container_ is not None:
            logger.critical(
                "A container has already been started in this object.")

            sys.exit(1)

        image  = "{0}:{1}".format(
                    Environment().get("image.name"),
                    Environment().get("image.tag"))

        logger.info("Starting the container from {0}".format(image))

        self.container_ = self.client_.containers.run(image, auto_remove=True, 
                                environment=self.env_, detach=True,
                                publish_all_ports=True)

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
                self.container_.reload()
                attempt += 1

        if not running:
            message = "The container failed to start within the allocated time."
            logger.critical(message)

            raise Exception(message)

        logger.info("The container, {0}, has started".format(
                            self.container_.name))

    def port(self):
        """
        Retrieve the port for the current running container.
        """

        if self.container_ is None:
            logger.critical("Error> the container is not currently running!")
            sys.exit(1)

        return self.container_.attrs['NetworkSettings']['Ports']['8443/tcp']\
                [0]['HostPort']

    def ipaddr(self):
        """
        Retrieve the IP address which can be used to access the container.
        """

        if self.container_ is None:
            logger.critical("Error> the container is not currently running!")
            sys.exit(1)

        ipaddr = self.container_.attrs['NetworkSettings']['Ports']['8443/tcp']\
                [0]['HostIp']

        if ipaddr == "0.0.0.0":
            ipaddr = Environment.get("container.ip")

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

        atexit.unregister(self.stopContainer)

