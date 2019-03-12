import logging

logger = logging.getLogger(__name__)


def set_pw(isamAppliance, password, check_mode=False, force=False):
    """
    Changing the administrator password of the embedded LDAP server
    """
    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:
        return isamAppliance.invoke_post("Changing the administrator password of the embedded LDAP server",
                                         "/isam/embedded_ldap/change_pwd/v1",
                                         {
                                             "password": password
                                         })
