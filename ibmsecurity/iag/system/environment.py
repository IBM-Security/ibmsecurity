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
import yaml
import os
import sys

from functools import reduce

logger  = logging.getLogger(__name__)

class Environment(object):
    """
    This class is used to manage access to the configuration data for the
    test run.
    """

    # Our configuration data.  The fact that this is defined as a class
    # level variables means that it will be static and we only have to
    # load the configuration a single time.
    config_ = None

    iag_user = 5001
    iag_group = 1000

    def __init__(self):
        super(Environment, self).__init__()

        Environment.loadConfig()

    @staticmethod
    def get(path):
        """
        Retrieve the configuration data with the specified path.  The path
        is a JSON path which uses a period as a path separator.  For example:
        'container.image_name'.
        """

        # The first thing which we need to do is to see if the path is
        # available as an environment variable.
        if path in os.environ:
            return os.environ[path]

        # If the path is not available as an environment variable we now 
        # check to see if it is contained in our configuration files.
        Environment.loadConfig()

        value = reduce(lambda acc, nxt: acc[nxt], path.split("."), 
                        Environment.config_)

        if value is None:
            message = "The {0} configuration value is missing!".format(path)

            logger.error(message)

            raise Exception(message)

        return value

    @staticmethod
    def loadConfig():
        """
        Load the configuration for this test run.  The configuration is loaded
        into a static variable so that we only perform the load a single time.
        """

        if Environment.config_ is None:
            # We always load our default yaml file, but can also be instructed
            # to augment this configuration with an additional yaml file.  This
            # allows us to specify a yaml file which over-rides certain
            # configuration entries from the default yaml file.

            config_files = [ 
                os.path.abspath(__file__  + "../../../../../../etc/config.yaml")
            ]

            if "CONFIG_FILE" in os.environ:
                config_files.append(os.environ['CONFIG_FILE'])

            Environment.config_ = {}

            for config_file in config_files:
                if os.path.isfile(config_file):
                    with open(config_file, 'r') as stream:
                        try:
                            Environment.config_.update(yaml.safe_load(stream))

                        except yaml.YAMLError as exc:
                            logger.critical(exc)
                            sys.exit(1)

            logger.debug("Configuration: {0}".format(Environment.config_))

    def is_container_context():
        return os.environ.get('IS_CONTAINER', "false") == "true"
