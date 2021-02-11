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


def set(isamAppliance, admin_id, admin_pwd, admin_domain="Default", check_mode=False, force=False):
    """
    Store the ISAM administrator credentials
    """
    return isamAppliance.invoke_post("Store the ISAM administrator credentials",
                                     "{0}".format(uri),
                                     {
                                         'admin_id': admin_id,
                                         'admin_pwd': admin_pwd,
                                         'admin_domain': admin_domain
                                     },
                                     requires_modules=requires_modules, requires_version=requires_version)


def delete(isamAppliance, check_mode=False, force=False):
    """
    Delete the stored ISAM administrator credential
    """
    return isamAppliance.invoke_delete("Delete the stored ISAM administrator credential",
                                       "{0}".format(uri),
                                       requires_modules=requires_modules, requires_version=requires_version)
