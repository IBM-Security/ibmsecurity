import logging
from ibmsecurity.utilities import tools
from ibmsecurity.isvg.im import property_file

logger = logging.getLogger(__name__)

# URI for this module
uri = "/v1/property"


def get_all(isvgAppliance, propertyFile, check_mode=False, force=False):
    """
    Retrieve all property/value pairs for a given property file
    """
    ret_obj = property_file.search(isvgAppliance, propertyFile=propertyFile, check_mode=check_mode, force=force)
    warnings = ret_obj['warnings']

    if ret_obj['data'] == {}:
        return isvgAppliance.create_return_object(warnings=warnings)
    else:
        return isvgAppliance.invoke_get("Retrieve all property/value pair for a given file", "{0}?PropertyFile={1}".format(uri, propertyFile))


def get(isvgAppliance, propertyFile, propertyName, check_mode=False, force=False):
    """
    Retrieve specific property/value pair for a given property file
    """
    ret_obj = property_file.search(isvgAppliance, propertyFile, check_mode=check_mode, force=force)
    warnings = ret_obj['warnings']

    if ret_obj['data'] == {}:
        warnings.append("Property file {0} had no match.".format(propertyFile))
        return isvgAppliance.create_return_object(warnings=warnings)
    else:
        return isvgAppliance.invoke_get("Retrieve a specific property/value pair for a given file", "{0}?PropertyFile={1}&PropertyName{2}".format(uri, propertyFile, propertyName))


def search(isvgAppliance, propertyFile, propertyName, check_mode=False, force=False):
    """
    Search for existing property/value pair for a given file.
    Just care for presence of property, not its actual value.
    """
    ret_obj = get(isvgAppliance, propertyFile=propertyFile, propertyName=propertyName)
    return_obj = isvgAppliance.create_return_object()

    for obj in ret_obj['data']:
        if obj['PropertyName'] == propertyName:
            logger.info("Found property {0}: {1}".format(propertyName, obj['PropertyValue']))
            return_obj['data'] = obj
            return_obj['rc'] = 0
            break

    return return_obj


def add(isvgAppliance, propertyFile, propertyName, propertyValue, check_mode=False, force=False):
    """
    Create an new property/value pair
    """
    ret_obj = property_file.search(isvgAppliance, propertyFile, check_mode=check_mode, force=force)
    if ret_obj['data'] == {}:
        warnings = ret_obj['warnings']
        warnings.append(
            "Property file {0} is not found. Cannot process request.".format(propertyFile))
        return isvgAppliance.create_return_object(warnings=warnings)

    ret_obj = search(isvgAppliance, propertyFile, propertyName, check_mode=check_mode, force=force)
    warnings = ret_obj['warnings']

    if force is True or ret_obj['data'] == {}:
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            # Create a simple json with just the property/value pair
            property_json = {
                "PropertyFile": propertyFile,
                "PropertyName": propertyName,
                "PropertyValue": propertyValue
            }

            return isvgAppliance.invoke_post(
                "Create a new property/value pair", uri, property_json, warnings=warnings)

    return isvgAppliance.create_return_object(warnings=warnings)


def delete(isvgAppliance, propertyFile, propertyName, check_mode=False, force=False):
    """
    Delete a property/value pair
    """
    ret_obj = property_file.search(isvgAppliance, propertyFile, check_mode=check_mode, force=force)
    warnings = ret_obj['warnings']

    if ret_obj['data'] == {}:
        warnings = ret_obj['warnings']
        warnings.append(
            "Property file {0} is not found. Cannot process request.".format(propertyFile))
        return isvgAppliance.create_return_object(warnings=warnings)

    ret_obj = search(isvgAppliance, propertyFile, propertyName, check_mode=check_mode, force=force)
    if force is True or ret_obj['data'] != {}:
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isvgAppliance.invoke_delete(
                "Delete a property/value pair", "{0}?PropertyFile={1}&PropertyName{2}".format(uri, propertyFile, propertyName), warnings=warnings)

    return isvgAppliance.create_return_object(warnings=warnings)


def update(isvgAppliance, propertyFile, propertyName, propertyValue, check_mode=False, force=False):
    """
    Update a property/value pair
    """
    ret_obj = property_file.search(isvgAppliance, propertyFile, check_mode=check_mode, force=force)
    if ret_obj['data'] == {}:
        warnings = ret_obj['warnings']
        warnings.append(
            "Property file {0} is not found. Cannot process request.".format(propertyFile))
        return isvgAppliance.create_return_object(warnings=warnings)

    ret_obj = search(isvgAppliance, propertyFile, propertyName, check_mode=check_mode, force=force)
    warnings = ret_obj['warnings']

    needs_update = True
    if ret_obj['data'] != {}:
        if ret_obj['data']['PropertyName'] == propertyName and ret_obj['data']['PropertyValue'] == propertyValue:
            needs_update = False

    if force is True or needs_update is True:
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            # Create a simple json with just the property/value pair
            property_json = {
                "PropertyFile": propertyFile,
                "PropertyName": propertyName,
                "PropertyValue": propertyValue
            }

            return isvgAppliance.invoke_put(
                "Update an existing property/value pair", uri, property_json, warnings=warnings)

    return isvgAppliance.create_return_object(warnings=warnings)


def set(isvgAppliance, propertyFile, propertyName, propertyValue, check_mode=False, force=False):
    """
    Creating or Modifying a property/value pair
    """
    if (search(isvgAppliance, propertyFile, propertyName))['data'] == {}:
        # Force the add - we already know object does not exist
        logger.info("Property {0} had no match, requesting to add new one.".format(propertyName))
        return add(isvgAppliance, propertyFile, propertyName, propertyValue, check_mode=check_mode, force=True)
    else:
        # Update request
        logger.info("Property {0} exists, requesting to update.".format(propertyName))
        return update(isvgAppliance, propertyFile, propertyName, propertyValue, check_mode=check_mode, force=force)
