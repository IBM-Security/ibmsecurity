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

    def __init__(self):
        """
        Initialise this object.

        \param port [in] : The port on which this server will be listening.
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

    def start(self):
        """
        Start the Web server.  The Web server will be started in a separate
        process and this function will wait until the Web server is
        reachable before returning.
        """

        logger.info("Starting the Web server: 0.0.0.0:{0}".format(self.port_))

        self.process = multiprocessing.Process(target=self.__runServer) 
        self.process.start() 

        atexit.register(self.stop)

        # Wait for the Web server to start.  
        running = False
        attempt = 0

        while not running and attempt < 30:
            time.sleep(1)

            try:
                requests.get("http://{0}:{1}".format(self.host_, self.port_), 
                                    timeout=2)

                running = True
            except:
                attempt += 1

        if not running:
            message = "The Web server failed to start within the allocated time."
            logger.critical(message)

            raise Exception(message)

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

    def __runServer(self):
        """
        This private function is used to actually start the server.
        """

        self.app.run(host="0.0.0.0", port=self.port_, use_reloader=False)


class HelloWorldWebServer(WebServer):

    """
    This class is used to create a simple Hello World Web Server.  It 
    really serves to illustrate how to create a Web Server using the WebServer
    class.
    """


    @WebServer.app.route("/")
    def hello_world():
        """
        Our default route, which will simply return the 'hello world' response.
        """

        return "Hello World!"


