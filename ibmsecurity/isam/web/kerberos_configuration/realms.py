import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/wga/kerberos/config/realms/"
requires_modules = ['wga']
requires_version = None


def get_all(isamAppliance, recursive='yes', includeValuesInLine='yes', addParent='yes', check_mode=False, force=False):
    """
    Retrieve Kerberos Configuration: Realms
    """
    return isamAppliance.invoke_get("Retrieve Kerberos Configuration: Realms",
                                    "{0}{1}".format(uri, tools.create_query_string(recursive=recursive,
                                                                                   includeValuesInLine=includeValuesInLine,
                                                                                   addParent=addParent)),
                                    requires_modules=requires_modules, requires_version=requires_version)


def add(isamAppliance, realm, check_mode=False, force=False):
    """
    Creating a Kerberos realm (Subsection)
    """
    ret_obj = search(isamAppliance=isamAppliance, realm=realm)

    if force is True or ret_obj['data'] == {}:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post(
                "Creating a Kerberos realm",
                "{0}".format(uri),
                {
                    "subsection": realm
                })

    return isamAppliance.create_return_object()


def delete(isamAppliance, realm, check_mode=False, force=False):
    """
    Deleting a Kerberos realm
    """
    ret_obj = search(isamAppliance=isamAppliance, realm=realm)

    if force is True or ret_obj['data'] != {}:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Deleting a Kerberos realm",
                "{0}{1}".format(uri, realm))

    return isamAppliance.create_return_object()


def get(isamAppliance, realm, check_mode=False, force=False):
    """
    Retrieve a specific Kerberos Configuration realm
    """
    return isamAppliance.invoke_get("Retrieve a specific Kerberos realm details",
                                    "{0}{1}".format(uri, realm),
                                    requires_modules=requires_modules,
                                    requires_version=requires_version)


def search(isamAppliance, realm, check_mode=False, force=False):
    """
    Search kerberos realm by name
    """
    ret_obj = get_all(isamAppliance)
    return_obj = isamAppliance.create_return_object()
    return_obj["warnings"] = ret_obj["warnings"]

    for obj in ret_obj['data']:
        if obj['name'] == realm:
            logger.info("Found Kerberos realm {0} id: {1}".format(realm, obj['id']))
            return_obj['data'] = obj['id']
            return_obj['rc'] = 0

    return return_obj


def compare(isamAppliance1, isamAppliance2):
    """
    Compare kerberos configuration realms between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    return tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
