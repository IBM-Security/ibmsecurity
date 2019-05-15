import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/wga/kerberos/config/domain_realm/"
requires_modules = ['wga']
requires_version = None


def get_all(isamAppliance, recursive='yes', includeValues='yes', check_mode=False, force=False):
    """
    Retrieve Kerberos Configuration: all Domain to Realm mappings defined
    """
    return isamAppliance.invoke_get("Retrieve Kerberos Configuration: Domains",
                                    "{0}{1}".format(uri, tools.create_query_string(recursive=recursive,
                                                                                   includeValues=includeValues)),
                                    requires_modules=requires_modules, requires_version=requires_version)


def add(isamAppliance, name, value, check_mode=False, force=False):
    """
    Creating a Kerberos Doamin (Local DNS Value)
    """
    ret_obj = search(isamAppliance, name)

    if force is True or ret_obj['data'] == {}:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post(
                "Creating a Kerberos domain",
                "{0}".format(uri),
                {
                    "name": name,
                    "value": value
                })

    return isamAppliance.create_return_object()


def delete(isamAppliance, name, check_mode=False, force=False):
    """
    Deleting a Kerberos Doamin
    """
    ret_obj = search(isamAppliance, name)

    if force is True or ret_obj['data'] != {}:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Deleting a Kerberos realm",
                "{0}{1}".format(uri, name))

    return isamAppliance.create_return_object()


def get(isamAppliance, name, check_mode=False, force=False):
    """
    Get a specific kerberos domain by name
    """
    ret_obj = get_all(isamAppliance)
    return_obj = isamAppliance.create_return_object()
    return_obj["warnings"] = ret_obj["warnings"]

    for obj in ret_obj['data']:
        if obj['name'] == name:
            logger.info("Found Kerberos domain {0} id: {1}".format(name, obj['id']))
            return_obj['data'] = obj
            return_obj['rc'] = 0

    return return_obj


def search(isamAppliance, name, check_mode=False, force=False):
    """
    Search kerberos domain to realm mapping by name
    """
    ret_obj = get_all(isamAppliance)
    return_obj = isamAppliance.create_return_object()
    return_obj["warnings"] = ret_obj["warnings"]

    for obj in ret_obj['data']:
        if obj['name'] == name:
            logger.info("Found Kerberos domain {0} id: {1}".format(name, obj['id']))
            return_obj['data'] = obj['id']
            return_obj['rc'] = 0

    return return_obj


def update(isamAppliance, name, value, check_mode=False, force=False):
    """
    Update a specified API domain mapping
    """
    warnings = []
    ret_obj = get(isamAppliance, name)
    if ret_obj['data'] == {}:
        warnings.append("Name: {0} not found, hence cannot update.".format(name))
    elif ret_obj['data']['value'] != value or force is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Update a specified domain to realm mapping entry",
                "{0}{1}".format(uri, name), {
                    "id": name,
                    "value": value
                }, requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object(warnings=warnings)


def compare(isamAppliance1, isamAppliance2):
    """
    Compare kerberos configuration domains between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    for obj in ret_obj1['data']:
        del obj['id']
    for obj in ret_obj2['data']:
        del obj['id']

    return tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['id'])
