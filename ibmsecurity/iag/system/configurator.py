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
import os
import yaml

from tempfile import mkstemp

from ibmsecurity.iag.system.config.frontend_v1 import FrontendV1
from ibmsecurity.iag.system.config.logging_v1  import LoggingV1
from ibmsecurity.iag.system.config.advanced_v1 import AdvancedV1
from ibmsecurity.iag.system.config.identity_v1 import IdentityV1
from ibmsecurity.iag.system.config.application_v1 import ApplicationV1

logger = logging.getLogger(__name__)

class Configurator(object):
    """
    This class is used to produce the configuration which can be used when
    starting an IAG container.
    """

    def __init__(self, 
                    frontend    = None, 
                    identity    = None, 
                    application = None,
                    logging     = None,
                    advanced    = None):
        """
        Initialise this class instance.  The parameters are as follows:

        @param frontend    : An ibmsecurity.iag.system.config.Frontend
                             object which is used to define the configuration
                             of the front-end part of IAG.
        @param identity    : One of ibmsecurity.iag.system.config.Identity
                             types of object which is used to define the
                             configuration for the authentication part of IAG.
        @param application : An array of ibmsecurity.iag.system.config.Application
                             objects which define the applications that will be
                             protected by the IAG.
        @param logging     : An ibmsecurity.iag.system.config.Logging object
                             which defines the logging to be used by the IAG.
        @param advanced    : An ibmsecurity.iag.system.config.Advanced object
                             which defines any advanced configuration for the
                             IAG.
        """
          
        super(Configurator, self).__init__()

        self.frontend    = self.__validate(FrontendV1, frontend)
        self.identity    = self.__validate(IdentityV1, identity)
        self.application = self.__validateList(ApplicationV1, application)
        self.logging     = self.__validate(LoggingV1, logging)
        self.advanced    = self.__validate(AdvancedV1, advanced)

    def write(self, filename = None):
        """
        Write the current configuration as a yaml file which can be used by
        the IAG.

        @param filename : The name of the file to write.  If no file is 
                          specified a temporary file will be created.

        @retval The name of the file which has been written.
        """

        # Construct the data.
        data    = {}
        version = "0"

        for name, value in vars(self).items():
            if value is not None:
                if isinstance(value, list):
                    data[name] = []
                    for entry in value:
                        inst, version = entry.getData(version)
                        data[name].append(inst)
                else:
                    data[name], version = value.getData(version)

        data['version'] = version

        # If we have not been provided with a file name we create a file name
        # now.
        if filename is None:
            fd, filename = mkstemp(suffix = ".yml")
            os.close(fd)

        # Write the data.
        with open(filename, 'w') as outfile:
            yaml.dump(data, outfile)

        logger.info("Wrote the IAG configuration to {0}".format(filename))

        return filename

    @classmethod
    def __validate(self, data_type, data):
        """
        This private method is used to check to ensure that the specified data 
        is of the correct data type.  An exception will be thrown if the data
        type is incorrect.

        @param data_type : The type of data
        @param data      : The data itself

        @retval The data
        """

        if data is not None and not isinstance(data, data_type):
            raise Exception("Data of an incorrect type was specified.")

        return data

    @classmethod
    def __validateList(self, data_type, data):
        """
        This private method is used to check to ensure that the specified data 
        is of the correct data type.  An exception will be thrown if the data
        type is incorrect.

        @param data_type : The type of data
        @param data      : The data itself

        @retval The data
        """

        if data is not None:
            if not isinstance(data, list):
                raise Exception("Data of an incorrect type was specified.")

            if len(data) > 0 and not isinstance(data[0], data_type):
                raise Exception("Data of an incorrect type was specified.")

        return data

