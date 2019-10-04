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

class AuthorizationV1(Base):
    """
    This class is used to represent the authorization configuration of an IAG
    container.  
    """

    def __init__(self, rules):
        """
        Initialise this class instance.  The parameters are as follows:

        @param rules : An array of AuthorzationRule objects.
        """

        super(AuthorizationV1, self).__init__()

        self.rules = self._checkList(AuthorizationRuleV1, rules)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"

##############################################################################

class AuthorizationRuleV1(Base):
    """
    This class is used to represent an authorization rule which is stored in the
    global/shared area of the configuration data.
    """

    def __init__(self, name, rule):
        """
        Initialise this class instance.  The parameters are as follows:

        @param name : The name of the authorization rule.
        @param rule : The authorization rule string. This is a formatted rule
                      string which is evaluated to make an authorization
                      decision.
        """

        super(AuthorizationRuleV1, self).__init__()

        self.name = Simple(str, name)
        self.rule = Simple(str, rule)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"

##############################################################################

