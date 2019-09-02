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
import base64
import os

logger = logging.getLogger(__name__)

from ibmsecurity.iag.system.config.base import Base

##############################################################################

class File(Base):
    """
    This class is used to represent a file which will be base-64 encoded
    and inserted into the container configuration.
    """

    def __init__(self, filename):
        """
        Initialise this class instance.  The parameters are as follows:

        @param filename : The name of the file which is to be used.
        """

        super(File, self).__init__()

        self._check(str, filename)

        if not os.path.isfile(filename):
            raise Exception("File does not exist: {0}".format(filename))

        with open(filename, "rb") as fh:
            self.value = "B64:{0}".format(
                    base64.b64encode(fh.read()).decode("utf-8"))

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"

    def getData(self, version):
        """
        Return the data which is managed by this object.  
        """

        return self.value, version

##############################################################################
