import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/jvm_property"


def get_all(isvgAppliance, check_mode=False, force=False):
    """
    Retrieve all property/value pairs
    """
    return isvgAppliance.invoke_get("Retrieve all property/value pair", "{0}".format(uri))


def get(isvgAppliance,  propertyName, check_mode=False, force=False):
    """
    Retrieve specific property/value pair
    """
    return isvgAppliance.invoke_get("Retrieve a specific property/value pair", "{0}?propertyName={1}".format(uri, propertyName))


def search(isvgAppliance, propertyName, check_mode=False, force=False):
    """
    Search for existing property/value pair for a given file.
    Just care for presence of property, not its actual value.
    """
    ret_obj = get(isvgAppliance, propertyName)
    return_obj = isvgAppliance.create_return_object()

    for obj in ret_obj['data']:
        if 'Error' not in obj:
            if obj['propertyName'] == propertyName:
                logger.info("Found property {0}: {1}".format(propertyName, obj['propertyValue']))
                return_obj['data'] = obj
                return_obj['rc'] = 0

    return return_obj


def add(isvgAppliance, propertyName, propertyValue, check_mode=False, force=False):
    """
    Create an new property/value pair
    """
    ret_obj = search(isvgAppliance, propertyName, check_mode=check_mode, force=force)
    warnings = ret_obj['warnings']

    if force is True or ret_obj['data'] == {}:
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            # Create a simple json with just the property/value pair
            property_json = {
                "propertyName": propertyName,
                "propertyValue": propertyValue
            }

            return isvgAppliance.invoke_post(
                "Create a new property/value pair", uri, property_json, warnings=warnings)

    return isvgAppliance.create_return_object(warnings=warnings)


def delete(isvgAppliance, propertyName, check_mode=False, force=False):
    """
    Delete a property/value pair
    """
    ret_obj = search(isvgAppliance, propertyName, check_mode=check_mode, force=force)
    if force is True or ret_obj['data'] != {}:
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isvgAppliance.invoke_delete(
                "Delete a property/value pair", "{0}?propertyName={1}".format(uri, propertyName), warnings=warnings)

    return isvgAppliance.create_return_object(warnings=warnings)


def update(isvgAppliance, propertyName, propertyValue, check_mode=False, force=False):
    """
    Update a property/value pair
    """
    ret_obj = search(isvgAppliance, propertyName, check_mode=check_mode, force=force)
    warnings = ret_obj['warnings']

    needs_update = True
    if 'propertyName' in ret_obj['data']:
        if ret_obj['data']['propertyName'] == propertyName and ret_obj['data']['propertyValue'] == propertyValue:
            needs_update = False

    if force is True or needs_update is True:
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            # Create a simple json with just the property/value pair
            property_json = {
                "propertyName": propertyName,
                "propertyValue": propertyValue
            }

            return isvgAppliance.invoke_put(
                "Update an existing property/value pair", uri, property_json, warnings=warnings)

    return isvgAppliance.create_return_object(warnings=warnings)


def set(isvgAppliance, propertyName, propertyValue, check_mode=False, force=False):
    """
    Creating or Modifying a property/value pair
    """
    if (search(isvgAppliance, propertyName))['data'] == {}:
        # Force the add - we already know object does not exist
        logger.info("Property {0} had no match, requesting to add new one.".format(propertyName))
        return add(isvgAppliance, propertyName, propertyValue, check_mode=check_mode, force=True)
    else:
        # Update request
        logger.info("Property {0} exists, requesting to update.".format(propertyName))
        return update(isvgAppliance, propertyName, propertyValue, check_mode=check_mode, force=force)
