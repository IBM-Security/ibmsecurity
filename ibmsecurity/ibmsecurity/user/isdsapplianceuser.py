import logging
from .user import User


class ISDSApplianceUser(User):
    super_user = "admin"  # Use name that will work regardless of Management Authentication setting

    def __init__(self, password, username=None):
        self.logger = logging.getLogger(__name__)
        self.logger.debug('Creating a user')

        if username is None:
            User.__init__(self, password, self.super_user)
            self.logger.debug('Creating a super-user')
        else:
            User.__init__(self, password, username)
