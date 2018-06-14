import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/iam/access/v8/devicefingerprints/"
requires_modules = ["mga"]
requires_version = None


def get_all(isamAppliance, filter=None, sortBy=None, check_mode=False, force=False):
    """
    Retrieve a list of devices fingerprints
    """
    return isamAppliance.invoke_get("Retrieve a list of Device Fingerprints",
                                    "{0}/{1}".format(uri, tools.create_query_string(filter=filter, sortBy=sortBy)),
                                    requires_modules=requires_modules, requires_version=requires_version)


def get(isamAppliance, name, check_mode=False, force=False):
    """
    Retrieve a device fingerprint for a specific device
    """
    warnings = []
    ret_obj = search(isamAppliance, name=name, check_mode=check_mode, force=force)
    id = ret_obj['data']

    if id == {}:
        warnings.append("Device {0} had no match, skipping retrieval.".format(name))
        return isamAppliance.create_return_object(changed=False, warnings=warnings)
    else:
        return isamAppliance.invoke_get("Retrieve a specific Device Fingerprint",
                                        "{0}/{1}".format(uri, id))


def search(isamAppliance, name, force=False, check_mode=False):
    """
    Search device id by name
    """
    ret_obj = get_all(isamAppliance)
    return_obj = isamAppliance.create_return_object()

    for obj in ret_obj['data']:
        if obj['name'] == name:
            logger.info("Found Device {0} id: {1}".format(name, obj['id']))
            return_obj['data'] = obj['id']
            return_obj['rc'] = 0

    return return_obj


def delete(isamAppliance, name, check_mode=False, force=False):
    """
    Delete a device fingerprint for a specific device
    """
    warnings = []
    ret_obj = search(isamAppliance, name=name, check_mode=check_mode, force=force)
    id = ret_obj['data']

    if id == {}:
        warnings.append("Device {0} had no match, skipping delete.".format(name))
        return isamAppliance.create_return_object(changed=False, warnings=warnings)
    else:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete("Delete a specific Device Fingerprint",
                                               "{0}/{1}".format(uri, id))


def delete_set(isamAppliance, devices, check_mode=False, force=False):
    """
    Delete a set of device fingerprints
    """
    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:
        return isamAppliance.invoke_delete(description="Delete a set of device fingerprints",
                                           uri=uri, data=devices, ignore_error=True)
