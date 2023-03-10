import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/iam/access/v8/databases/hvdb"
requires_modules = None
requires_version = None


def get(isamAppliance, check_mode=False, force=False):
    """
    Get the status of the most recent deletion of data that completed

    """
    return isamAppliance.invoke_get("Get the status of the most recent deletion of data that completed",
                                    "{0}/status".format(uri),
                                    requires_modules=requires_modules, requires_version=requires_version)


def cancel_all(isamAppliance, check_mode=False, force=False):
    """
    Cancel the deletion of all data

    """
    return isamAppliance.invoke_get("Cancel the deletion of all data",
                                    "{0}/cancel".format(uri),
                                    requires_modules=requires_modules, requires_version=requires_version)


def cancel_all_user(isamAppliance, check_mode=False, force=False):
    """
    Cancel the deletion of all user data

    """
    return isamAppliance.invoke_get("Cancel the deletion of all user data",
                                    "{0}/userdata/cancel".format(uri),
                                    requires_modules=requires_modules, requires_version=requires_version)


def cancel_all_devices(isamAppliance, check_mode=False, force=False):
    """
    Cancel the deletion of all user devices

    """
    return isamAppliance.invoke_get("Cancel the deletion of all user devices",
                                    "{0}/devices/cancel".format(uri),
                                    requires_modules=requires_modules, requires_version=requires_version)


def clear(isamAppliance, check_mode=False, force=False):
    """
    Clear the status of the most recent deletion of data that completed

    """

    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:

        return isamAppliance.invoke_delete(
            "Clear the status of the most recent deletion of data that completed",
            "{0}/status".format(uri),
            requires_modules=requires_modules, requires_version=requires_version
        )

    return isamAppliance.create_return_object()


def delete_all(isamAppliance, check_mode=False, force=False):
    """
    Delete all data

    """

    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:

        return isamAppliance.invoke_delete(
            "Delete all data",
            "{0}".format(uri),
            requires_modules=requires_modules, requires_version=requires_version
        )

    return isamAppliance.create_return_object()


def delete_user(isamAppliance, userId, check_mode=False, force=False):
    """
    Delete all user data for a specific user

    """

    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:

        return isamAppliance.invoke_delete(
            "Delete all user data for a specific user",
            "{0}/{1}".format(uri, userId),
            requires_modules=requires_modules, requires_version=requires_version
        )

    return isamAppliance.create_return_object()


def delete_all_user(isamAppliance, check_mode=False, force=False):
    """
    Delete all user data
    """

    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:

        return isamAppliance.invoke_delete(
            "Delete all user data",
            "{0}/userdata".format(uri),
            requires_modules=requires_modules, requires_version=requires_version
        )

    return isamAppliance.create_return_object()


def delete_all_devicces(isamAppliance, check_mode=False, force=False):
    """
    Delete all user devices
    """

    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:

        return isamAppliance.invoke_delete(
            "Delete all user devices",
            "{0}/devices".format(uri),
            requires_modules=requires_modules, requires_version=requires_version
        )

    return isamAppliance.create_return_object()
