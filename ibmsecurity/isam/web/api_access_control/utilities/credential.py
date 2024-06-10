import logging

from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

uri = "/wga/apiac/credentials"
requires_modules = ["wga"]
requires_version = "9.0.7"


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieve the stored ISAM credential
    """
    return isamAppliance.invoke_get("Retrieve the stored ISAM credential",
                                    "{0}".format(uri),
                                    requires_modules=requires_modules, requires_version=requires_version)


def add(isamAppliance, admin_id, admin_pwd, admin_domain="Default", check_mode=False, force=False):
    """
    Store the ISAM administrator credentials
    """
    exist, warnings = _check(isamAppliance)

    if not force and exist:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
    else:
        if not check_mode:
            return isamAppliance.invoke_post("Store the ISAM administrator credentials",
                                         "{0}".format(uri),
                                         {
                                             'admin_id': admin_id,
                                             'admin_pwd': admin_pwd,
                                             'admin_domain': admin_domain
                                         },
                                         requires_modules=requires_modules, requires_version=requires_version)
    return isamAppliance.create_return_object(warnings=warnings)


def delete(isamAppliance, check_mode=False, force=False):
    """
    Delete the stored ISAM administrator credential
    """
    exist, warnings = _check(isamAppliance)

    if force or exist:
        if check_mode:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_delete("Delete the stored ISAM administrator credential",
                                               "{0}".format(uri),
                                               requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object(warnings=warnings)

def _check(isamAppliance, check_mode=False, force=False):
    ret_obj = get(isamAppliance)
    if ret_obj['data'] == {}:
        return False, ret_obj['warnings']
    elif ret_obj['data']['admin_id'] is None:
        return False, ret_obj['warnings']
    else:
        return True, ret_obj['warnings']
