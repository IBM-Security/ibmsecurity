import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/wga/kerberos/config/realms/"
requires_modules = ['wga']
requires_version = None


def get(isamAppliance, recursive='yes', includeValuesInLine='yes', check_mode=False, force=False):
    """
    Retrieve Kerberos Configuration: Realms
    """
    return isamAppliance.invoke_get("Retrieve Kerberos Configuration: Realms",
                                    "{0}{1}".format(uri, tools.create_query_string(recursive=recursive,
                                                                                   includeValuesInLine=includeValuesInLine)),
                                    requires_modules=requires_modules, requires_version=requires_version)

def add(isamAppliance, realm_name, check_mode=False, force=False):
    """
    Creating a Kerberos realm (Subsection)
    """
    if force is True or _check(isamAppliance, realm_name) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post(
                "Creating a Kerberos realm",
                "{0}".format(uri),
                {
                    "subsection": realm_name
                })

    return isamAppliance.create_return_object()

def delete(isamAppliance, id, check_mode=False, force=False):
    """
    Deleting a Kerberos realm
    """
    if force is True or _check(isamAppliance, id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Deleting a Kerberos realm",
                "{0}{1}".format(uri, id))

    return isamAppliance.create_return_object()

def compare(isamAppliance1, isamAppliance2):
    """
    Compare kerberos configuration realms between two appliances
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    return tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])

def _check(isamAppliance, realm_name):
    """
    Check if realm name already exists
    """
    ret_obj = get(isamAppliance)

    for obj in ret_obj['data']:
        if obj['name'] == realm_name:
            return True

    return False
