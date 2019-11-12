"""
IBM Confidential
Object Code Only Source Materials
5725-V90
(c) Copyright International Business Machines Corp. 2020
The source code for this program is not published or otherwise divested
of its trade secrets, irrespective of what has been deposited with the
U.S. Copyright Office.
"""

import logging
import multiprocessing
import atexit
import requests
import time
import socket
import sys
import ssl

from flask import Flask

from ibmsecurity.iag.system.environment import Environment

logger = logging.getLogger(__name__)

class WebServer:
    """
    This class is used to create a simple Web Server.  You must create a new
    object which inherits from this class to actually provide a Web server.
    An example class could be:

    class HelloWorldWebServer(WebServer):

        @WebServer.app.route("/")
        def hello_world():
          return "Hello World!"

    """

    app = Flask(__name__)

    def __init__(self, ssl = False):
        """
        Initialise this object.

        \param ssl [in] : Should we use http or https?
        """

        super(WebServer, self).__init__()

        # Get an ephemeral port on which the Web server can listen.
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            s.bind(("0.0.0.0", 0))

            self.port_ = s.getsockname()[1]
        except:
            self.port_ = 8079
        finally:
            s.close()

        # Work out the host name.
        self.host_ = None

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            s.connect(('10.255.255.255', 1))

            self.host_ = s.getsockname()[0]
        except:
            self.host_ = "127.0.0.1"
        finally:
            s.close()

        self.process_ = None
        self.ssl_     = ssl
        self.caCert_  = None

    def start(self):
        """
        Start the Web server.  The Web server will be started in a separate
        process and this function will wait until the Web server is
        reachable before returning.
        """

        logger.info("Starting the Web server: 0.0.0.0:{0}".format(self.port_))

        self.process = multiprocessing.Process(
                            target=self.__runServer, args=[self.ssl_]) 
        self.process.start() 

        atexit.register(self.stop)

        # Wait for the Web server to start.  
        running = False
        attempt = 0

        if self.ssl_:
            protocol="https"
        else:
            protocol="http"

        while not running and attempt < 30:
            time.sleep(1)

            try:
                requests.get("{0}://{1}:{2}".format(protocol, self.host_, 
                                        self.port_), verify=False, timeout=2)

                running = True
            except:
                attempt += 1

        if not running:
            message = "The Web server failed to start within the allocated time."
            logger.critical(message)

            raise Exception(message)

        # If we are using SSL we also need to grab the CA certificate from
        # the server.
        if self.ssl_:
            self.caCert_ = ssl.get_server_certificate((self.host_, self.port_))

        logger.info("The Web server has started")

    def stop(self):
        """
        Stop the Web server.
        """

        if self.process is not None:
            logger.info("Stopping the Web server.")

            self.process.terminate()
            self.process = None

    def port(self):
        """
        The port on which the Web server will be listening.
        """

        return self.port_

    def host(self):
        """
        Determine and return the host on which the Web server will be
        listening.  
        """

        return self.host_

    def ssl(self):
        """
        Return whether this server is SSL enabled or not.
        """

        return self.ssl_

    def caCertificate(self):
        """
        Return the CA certificate (in PEM format) of this server.
        """

        return self.caCert_;

    def __runServer(self, ssl):
        """
        This private function is used to actually start the server.
        """

        if ssl:
            ssl_context = "adhoc"
        else:
            ssl_context = None

        self.app.run(ssl_context=ssl_context, host="0.0.0.0", 
                        port=self.port_, use_reloader=False)

