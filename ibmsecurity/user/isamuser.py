import logging
from .user import User


class ISAMUser(User):
    super_user = "sec_master"

    def __init__(self, password, username=None):
        self.logger = logging.getLogger(__name__)
        self.logger.debug('Creating a user')

        if username is None:
            User.__init__(self, password=password, username=self.super_user)
            self.logger.debug('Creating a super-user')
        else:
            User.__init__(self, password=password, username=username)
