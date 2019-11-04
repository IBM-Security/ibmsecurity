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

logger = logging.getLogger(__name__)

from ibmsecurity.iag.system.config.base import Base
from ibmsecurity.iag.system.config.base import Simple
from ibmsecurity.iag.system.config.base import SimpleList
from ibmsecurity.iag.system.config.base import AutoNumber

##############################################################################

class AdvancedV1(Base):
    """
    This class is used to represent the advanced configuration of an IAG
    container.  
    """

    def __init__(self, configuration):
        """
        Initialise this class instance.  The parameters are as follows:

        @param configuration : An array of 
                               ibmsecurity.iag.system.config.AdvConfigV1
                               objects.
        """

        super(AdvancedV1, self).__init__()

        self.configuration = self._checkList(AdvConfigV1, configuration)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"

##############################################################################

class AdvConfigV1(Base):
    """
    This class is used to represent an advanced configuration update.
    """

    def __init__(self, stanza, entry, operation, value = None):
        """
        Initialise this class instance.  The parameters are as follows:

        @param stanza    : The name of the configuration stanza.
        @param entry     : The name of the configuration entry.
        @param operation : An ibmsecurity.iag.system.config.AdvConfigOperationV1
                           object which is used to specify the operation type.
        @param value     : An array of configuration values.
        """

        super(AdvConfigV1, self).__init__()

        self.stanza    = Simple(str, stanza)
        self.entry     = Simple(str, entry)
        self.operation = self._check(AdvConfigOperationV1, operation)
        self.value     = SimpleList(str, value)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"

##############################################################################

class AdvConfigOperationV1(AutoNumber):
    """
    This class is used to represent a single advanced configuration operation.
    """

    add    = ()
    set    = ()
    delete = ()

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"

    def getData(self, version):
        """
        Return the data which is managed by this object.  
        """

        if (self.version() > version):
            version = self.version()

        return self.name.replace("_","."), version

##############################################################################

