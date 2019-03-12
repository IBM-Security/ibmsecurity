import json
import logging
import time

logger = logging.getLogger(__name__)


def reboot(isdsAppliance, check_mode=False, force=False):
    """
    Reboot the appliance
    """
    if check_mode is True:
        return isdsAppliance.create_return_object(changed=True)
    else:
        return isdsAppliance.invoke_post("Rebooting appliance",
                                         "/diagnostics/restart_shutdown/reboot",
                                         {})


def shutdown(isdsAppliance, check_mode=False, force=False):
    """
    Shutdown the appliance
    """
    if check_mode is True:
        return isdsAppliance.create_return_object(changed=True)
    else:
        return isdsAppliance.invoke_post("Shutting down appliance",
                                         "/diagnostics/restart_shutdown/shutdown",
                                         {})


def _changes_available(isdsAppliance):
    """
    Check for pending changes on the appliance
    :param isdsAppliance:
    :return:
    """
    #    changes = isdsAppliance.invoke_get("Get pending changes",
    #                                       "/pending_changes")
    #    logger.debug("Pending changes on appliance are:")
    #    logger.debug(changes['data'])
    #
    #    change_count = isdsAppliance.invoke_get("Get pending changes count",
    #                                            "/pending_changes/count")
    #    logger.debug("Pending change count on appliance is:")
    #    logger.debug(change_count['data'])
    #
    #    if change_count['data']['count'] > 0 or len(changes['data']['changes']) > 0:
    #        logger.info("pending changes found")
    #        return True
    #    else:
    #        return False

    return True


def commit(isdsAppliance, check_mode=False, force=False):
    """
    Commit the current pending changes.
    """
    if force is True or _changes_available(isdsAppliance) is True:
        if check_mode is True:
            return isdsAppliance.create_return_object(changed=True)
        else:
            return isdsAppliance.invoke_get("Committing the changes",
                                            "/pending_changes/deploy",
                                            {})

    return isdsAppliance.create_return_object()


def commit_and_restart(isdsAppliance, check_mode=False, force=False):
    """
    Commit and Restart LMI
    :param isdsAppliance:
    :param check_mode:
    :param force:
    :return:
    """
    if force is True or _changes_available(isdsAppliance) is True:
        if check_mode is True:
            return isdsAppliance.create_return_object(changed=True)
        else:
            return isdsAppliance.invoke_post("Commit and Restart",
                                             "/restarts/commit_and_restart",
                                             {})
    return isdsAppliance.create_return_object()


def rollback(isdsAppliance, check_mode=False, force=False):
    """
    Rollback the current pending changes.
    """
    if force is True or _changes_available(isdsAppliance) is True:
        if check_mode is True:
            return isdsAppliance.create_return_object(changed=True)
        else:
            return isdsAppliance.invoke_get("Rollback the changes",
                                            "/pending_changes/forget")

    return isdsAppliance.create_return_object()
