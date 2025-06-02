import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/workflowextension"


def get_all(isvgAppliance, check_mode=False, force=False):
    """
    Retrieve all extensions
    """
    return isvgAppliance.invoke_get("Retrieve all extensions", "{0}".format(uri))


def search(isvgAppliance, name, check_mode=False, force=False):
    """
    Search for existing extension.
    Just care for presence of extension, not its actual content.
    """
    ret_obj = get_all(isvgAppliance)
    return_obj = isvgAppliance.create_return_object()

    for obj in ret_obj['data']:
        if obj['name'] == name:
            logger.info("Found extension {0}".format(name))
            return_obj['data'] = obj
            return_obj['rc'] = 0
            break

    return return_obj


def add(isvgAppliance, name, extension, check_mode=False, force=False):
    """
    Create an new extension
    For now only support adding extension with the 'Provide XML' method
    """
    ret_obj = search(isvgAppliance, name, check_mode=check_mode, force=force)
    warnings = ret_obj['warnings']

    # extension content must be on a single line
    content = open(extension).read().replace('\n', '')

    if force is True or ret_obj['data'] == {}:
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            # Create a simple json with just the extension data
            extension_json = {
                "name": name,
                "servletName": "",
                "servletDescription": "",
                "servletClass": "",
                "urlPattern": "",
                "loadOnStartup": "0",
                "mode":"advanced",
                "extension": content
            }

            return isvgAppliance.invoke_post(
                "Create a new extension", uri, extension_json, warnings=warnings)

    return isvgAppliance.create_return_object(warnings=warnings)


def delete(isvgAppliance, name, extension, check_mode=False, force=False):
    """
    Delete an existing extension
    """
    ret_obj = search(isvgAppliance, name, check_mode=check_mode, force=force)
    if force is True or ret_obj['data'] != {}:
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            if 'uuid' in ret_obj['data']:
                uuid = ret_obj['data']['uuid']
                warnings = ret_obj['warnings']
                return isvgAppliance.invoke_delete(
                    "Delete an existing extension", "{0}/{1}".format(uri, uuid), warnings=warnings)

    return isvgAppliance.create_return_object(warnings=warnings)


def update(isvgAppliance, name, extension, check_mode=False, force=False):
    """
    Update an existing extension
    For now only support adding extension with the 'Provide XML' method
    """
    ret_obj = search(isvgAppliance, name, check_mode=check_mode, force=force)
    warnings = ret_obj['warnings']

    # extension content must be on a single line
    content = open(extension).read().replace('\n', '')

    needs_update = True
    if ret_obj['data'] != {}:
        if ret_obj['data']['extension'] == content:
            needs_update = False

    if force is True or needs_update is True:
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            if 'uuid' in ret_obj['data']:
                uuid = ret_obj['data']['uuid']
                # Create a simple json with just the extension data
                extension_json = {
                    "name": name,
                    "servletName": "",
                    "servletDescription": "",
                    "servletClass": "",
                    "urlPattern": "",
                    "loadOnStartup": "0",
                    "mode":"advanced",
                    "extension": content
                }

                return isvgAppliance.invoke_put(
                    "Update an existing extension", "{0}/{1}".format(uri,uuid), extension_json, warnings=warnings)

    return isvgAppliance.create_return_object(warnings=warnings)


def set(isvgAppliance, name, extension, check_mode=False, force=False):
    """
    Creating or Modifying a extension
    """
    if (search(isvgAppliance, name, extension))['data'] == {}:
        # Force the add - we already know object does not exist
        logger.info("Extension {0} had no match, requesting to add new one.".format(extension))
        return add(isvgAppliance, name, extension, check_mode=check_mode, force=True)
    else:
        # Update request
        logger.info("Extension {0} exists, requesting to update.".format(extension))
        return update(isvgAppliance, name, extension, check_mode=check_mode, force=force)
