import json
import logging
import time

logger = logging.getLogger(__name__)


def reboot(isamAppliance, check_mode=False, force=False):
    """
    Reboot the appliance
    """
    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:
        return isamAppliance.invoke_post("Rebooting appliance",
                                         "/diagnostics/restart_shutdown/reboot",
                                         {})


def shutdown(isamAppliance, check_mode=False, force=False):
    """
    Shutdown the appliance
    """
    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:
        return isamAppliance.invoke_post("Shutting down appliance",
                                         "/diagnostics/restart_shutdown/shutdown",
                                         {})


def _changes_available(isamAppliance):
    """
    Check for pending changes on the appliance
    :param isamAppliance:
    :return:
    """
    changes = isamAppliance.invoke_get("Get pending changes",
                                       "/isam/pending_changes")
    logger.debug("Pending changes on appliance are:")
    logger.debug(changes['data'])

    change_count = isamAppliance.invoke_get("Get pending changes count",
                                            "/isam/pending_changes/count")
    logger.debug("Pending change count on appliance is:")
    logger.debug(change_count['data'])

    if change_count['data']['count'] > 0 or len(changes['data']['changes']) > 0:
        logger.info("pending changes found")
        return True
    else:
        return False


def commit(isamAppliance, check_mode=False, force=False):
    """
    Commit the current pending changes.
    """
    if force is True or _changes_available(isamAppliance) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put("Committing the changes",
                                            "/isam/pending_changes",
                                            {})

    return isamAppliance.create_return_object()


def commit_and_restart(isamAppliance, check_mode=False, force=False):
    """
    Commit and Restart
    :param isamAppliance:
    :param check_mode:
    :param force:
    :return:
    """
    if force is True or _changes_available(isamAppliance) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post("Commit and Restart",
                                             "/restarts/commit_and_restart",
                                             {})
    return isamAppliance.create_return_object()


def rollback(isamAppliance, check_mode=False, force=False):
    """
    Rollback the current pending changes.
    """
    if force is True or _changes_available(isamAppliance) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete("Rollback the changes",
                                               "/isam/pending_changes")

    return isamAppliance.create_return_object()
