import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/wga/kerberos/config/libdefaults"
requires_modules = ['wga']
requires_version = None


def get_all(isamAppliance, recursive='yes', includeValues='yes', check_mode=False, force=False):
    """
    Retrieve Kerberos Configuration: Defaults
    """
    return isamAppliance.invoke_get("Retrieve Kerberos Configuration: Defaults",
                                    "{0}{1}".format(uri, tools.create_query_string(recursive=recursive,
                                                                                   includeValues=includeValues)),
                                    requires_modules=requires_modules, requires_version=requires_version)


def get(isamAppliance, name, check_mode=False, force=False):
    """
    Retrieve a specific Kerberos Configuration Default Property
    """
    ret_obj = search(isamAppliance, name=name, check_mode=check_mode, force=force)
    config_prop_name = ret_obj['data']
    warnings = ret_obj["warnings"]

    if config_prop_name == {}:
        logger.info("Kerberos Default config property {0} had no match, skipping retrieval.".format(name))
        warnings.append("Kerberos Default config property {0} had no match.".format(name))
        return isamAppliance.create_return_object(warnings=warnings)
    else:
        return _get(isamAppliance, name)


def _get(isamAppliance, config_prop_name, recursive="yes", includeValues="yes"):
    return isamAppliance.invoke_get("Retrieve a specific Kerberos Configuration default property",
                                    "{0}/{1}".format(uri, config_prop_name), requires_modules=requires_modules,
                                    requires_version=requires_version)


def search(isamAppliance, name, check_mode=False, force=False):
    """
    Search default kerberos config by name
    """
    ret_obj = get_all(isamAppliance)
    return_obj = isamAppliance.create_return_object()
    return_obj["warnings"] = ret_obj["warnings"]

    for obj in ret_obj['data']:
        if obj['name'] == name:
            logger.info("Found Kerberos Config Default property {0} id: {1}".format(name, obj['id']))
            return_obj['data'] = obj['id']
            return_obj['rc'] = 0

    return return_obj


def add(isamAppliance, name, value, check_mode=False, force=False):
    """
    Create Kerberos Configuration Default Property
    """
    ret_obj = search(isamAppliance, name=name, check_mode=check_mode, force=force)
    warnings = ret_obj["warnings"]
    if force is True or ret_obj["data"] == {}:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_post("Create Kerberos Configuration Default Property", uri,
                                             {
                                                 "name": name,
                                                 "value": value
                                             },
                                             requires_modules=requires_modules, requires_version=requires_version,
                                             warnings=warnings)

    return isamAppliance.create_return_object(warnings=warnings)


def delete(isamAppliance, name, check_mode=False, force=False):
    """
    Delete an Kerberos Configuration Default property
    """
    ret_obj = search(isamAppliance, name, check_mode=check_mode, force=force)
    config_prop_name = ret_obj['data']
    warnings = ret_obj["warnings"]

    if config_prop_name == {}:
        logger.info("Default property {0} not found, skipping delete.".format(name))
    else:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_delete(
                "Delete an Kerberos configuration default property",
                "{0}/{1}".format(uri, name), requires_modules=requires_modules,
                requires_version=requires_version, warnings=warnings)

    return isamAppliance.create_return_object(warnings=warnings)


def update(isamAppliance, name, value, check_mode=False,
           force=False):
    """
    Update a specified Kerberos Configuration Default property
    """
    ret_obj = get(isamAppliance, name)
    warnings = ret_obj["warnings"]

    if ret_obj["data"] == {}:
        warnings.append("Definiton {0} not found, skipping update.".format(name))
        return isamAppliance.create_return_object(warnings=warnings)
    else:
        config_prop_value = ret_obj["data"]
        logger.debug("property value is: {0}".format(config_prop_value))

    needs_update = False
    json_data = {
        "value": value
    }

    if force is not True:
        logger.debug(str(value))
        logger.debug(' '.join(config_prop_value))
        if str(value).lower() != (' '.join(config_prop_value)).lower():
            needs_update = True

    logger.debug("needs update is: {0}".format(needs_update))

    if force is True or needs_update is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_put(
                "Update a specified Kerberos Configuration Default property",
                "{0}/{1}".format(uri, name), json_data, requires_modules=requires_modules,
                requires_version=requires_version, warnings=warnings)

    return isamAppliance.create_return_object(warnings=warnings)

def set(isamAppliance, name, value, check_mode=False, force=False):
    """
    Set specified Kerberos Configuration Default property

    :param isamAppliance:
    :return:
    """
    ret_obj = search(isamAppliance, name)

    if ret_obj["data"] == {}:
        return add(isamAppliance, name, value, check_mode, force=True)

    return update(isamAppliance,  name, value, check_mode, force)

def compare(isamAppliance1, isamAppliance2):
    """
    Compare kerberos configuration defaults between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    for obj in ret_obj1['data']:
        del obj['id']
    for obj in ret_obj2['data']:
        del obj['id']

    return tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['id'])
