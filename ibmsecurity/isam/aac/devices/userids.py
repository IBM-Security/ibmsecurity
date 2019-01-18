import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/iam/access/v8/devicefingerprints/userIds/"
requires_modules = ["mga"]
requires_version = None


def get_all(isamAppliance, filter=None, sortBy=None, check_mode=False, force=False):
    """
    Retrieve a list of user IDs from devices fingerprints
    """
    return isamAppliance.invoke_get("Retrieve a list of user IDs from Devices Fingerprints",
                                    uri,
                                    requires_modules=requires_modules, requires_version=requires_version)


def search(isamAppliance, userID, force=False, check_mode=False):
    """
    Search device id by userId
    """
    ret_obj = get_all(isamAppliance)
    return_obj = isamAppliance.create_return_object()

    for obj in ret_obj['data']:
        if obj['userID'] == userID:
            logger.info("Found user {0}".format(userID))
            return_obj['data'] = userID
            return_obj['rc'] = 0

    return return_obj


def get(isamAppliance, userID, check_mode=False, force=False):
    """
    Retrieve a list of device fingerprints for a given user ID
    """
    warnings = []
    ret_obj = search(isamAppliance, userID=userID, check_mode=check_mode, force=force)
    id = ret_obj['data']

    if id == {}:
        warnings.append("User {0} had no match, skipping retrieval.".format(userID))
        return isamAppliance.create_return_object(changed=False, warnings=warnings)
    else:
        return isamAppliance.invoke_get("Retrieve a list of device fingerprints for a given user ID",
                                        "{0}/{1}".format(uri, userID))


def delete(isamAppliance, userID, check_mode=False, force=False):
    """
    Delete all device fingerprints for the given user ID
    """
    warnings = []
    ret_obj = search(isamAppliance, userID=userID, check_mode=check_mode, force=force)
    id = ret_obj['data']

    if id == {}:
        warnings.append("User {0} had no match, skipping Delete.".format(userID))
        return isamAppliance.create_return_object(changed=False, warnings=warnings)
    else:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete("Delete all device fingerprints for the given user ID",
                                               "{0}/{1}".format(uri, userID))
