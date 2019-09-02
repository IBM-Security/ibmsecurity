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

##############################################################################

class AdvancedV1(Base):
    """
    This class is used to represent the advanced configuration of an IAG
    container.  
    """

    def __init__(self, stanzas):
        """
        Initialise this class instance.  The parameters are as follows:

        @param stanzas : An array of Stanza objects.
        """

        super(AdvancedV1, self).__init__()

        self.stanzas = self._checkList(StanzaV1, stanzas)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"

##############################################################################

class StanzaV1(Base):
    """
    This class is used to represent a stanza which will be updated as a part
    of the advanced configuration.
    """

    def __init__(self, name, entries):
        """
        Initialise this class instance.  The parameters are as follows:

        @param name    : The name of the stanza.
        @param entries : The stanza entries.  This should be a dictionary of
                         name/value pairs which represent the configuration
                         entries within the stanza.
        """

        super(StanzaV1, self).__init__()

        setattr(self, name, Simple(dict, entries))

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"

##############################################################################

