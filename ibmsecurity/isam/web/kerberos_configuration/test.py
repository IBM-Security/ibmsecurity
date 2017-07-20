import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/wga/kerberos/config/capaths"
requires_modules = ['wga']
requires_version = None


def get_all(isamAppliance, recursive='yes', includeValues='yes', addParent='yes', check_mode=False, force=False):
    """
    Retrieve Kerberos Configuration: CA Paths
    """
    return isamAppliance.invoke_get("Retrieve Kerberos Configuration: CA Paths",
                                    "{0}{1}".format(uri, tools.create_query_string(recursive=recursive,
                                                                                   includeValues=includeValues,
                                                                                   addParent=addParent)),
                                    requires_modules=requires_modules, requires_version=requires_version)


def get(isamAppliance, name, check_mode=False, force=False):
    """
   Retrieve a specific Kerberos Client Realm Configuration 
    """
    ret_obj = search(isamAppliance, client_realm=name, check_mode=check_mode, force=force)
    ret_name = ret_obj['data']
    warnings = ret_obj["warnings"]

    if ret_name == {}:
        logger.info("Client realm: {0} had no match, skipping retrieval.".format(name))
        warnings.append("Client realm: {0} had no match.".format(name))
        return isamAppliance.create_return_object(warnings=warnings)
    else:
        return _get(isamAppliance, ret_name)


def _get(isamAppliance, name):
    return isamAppliance.invoke_get("Retrieve a specific client realm entry",
                                    "{0}/{1}".format(uri, name), requires_modules=requires_modules,
                                    requires_version=requires_version)


def search(isamAppliance, client_realm, check_mode=False, force=False):
    """
    Search client realm by name
    """
    ret_obj = get_all(isamAppliance)
    return_obj = isamAppliance.create_return_object()
    return_obj["warnings"] = ret_obj["warnings"]

    for obj in ret_obj['data']:
        if obj['name'] == client_realm:
            logger.info("Found name {0} id: {1}".format(client_realm, obj['id']))
            return_obj['data'] = obj['name']
            return_obj['rc'] = 0

    return return_obj


def add(isamAppliance, client_realm, check_mode=False, force=False):
    """
    Add a client realm entry 
    """
    ret_obj = search(isamAppliance, client_realm=client_realm, check_mode=check_mode, force=force)
    warnings = ret_obj["warnings"]

    if force is True or ret_obj["data"] == {}:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_post(
                "Create an Kerberos Configuration Client realm entry", uri,
                {
                    "subsection": client_realm
                }, requires_modules=requires_modules, requires_version=requires_version, warnings=warnings)

    return isamAppliance.create_return_object(warnings=warnings)


def delete(isamAppliance, client_realm, check_mode=False, force=False):
    """
    Delete an client realm entry
    """
    ret_obj = search(isamAppliance, client_realm, check_mode=check_mode, force=force)
    client_realm = ret_obj['data']
    warnings = ret_obj["warnings"]

    if client_realm == {}:
        logger.info("Client Realm {0} not found, skipping delete.".format(client_realm))
    else:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_delete(
                "Delete an Kerberos Configuration Client Realm entry",
                "{0}/{1}".format(uri, client_realm), requires_modules=requires_modules,
                requires_version=requires_version, warnings=warnings)

    return isamAppliance.create_return_object(warnings=warnings)


def compare(isamAppliance1, isamAppliance2):
    """
    Compare kerberos configuration ca paths between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    for obj in ret_obj1['data']:
        del obj['id']
    for obj in ret_obj2['data']:
        del obj['id']

    return tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['id'])
