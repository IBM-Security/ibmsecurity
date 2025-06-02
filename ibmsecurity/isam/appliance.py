import json
import logging
import time
import ibmsecurity.isam.base.lmi

logger = logging.getLogger(__name__)
requires_model="Appliance"


def reboot(isamAppliance, check_mode=False, force=False):
    """
    Restart the appliance
    """
    if check_mode:
        return isamAppliance.create_return_object(changed=True)
    else:
        return isamAppliance.invoke_post("Restart the appliance",
                                         "/diagnostics/restart_shutdown/reboot",
                                         {}, requires_model=requires_model)


def shutdown(isamAppliance, check_mode=False, force=False):
    """
    Shutdown the appliance
    """
    if check_mode:
        return isamAppliance.create_return_object(changed=True)
    else:
        return isamAppliance.invoke_post("Shutting down appliance",
                                         "/diagnostics/restart_shutdown/shutdown",
                                         {}, requires_model=requires_model)


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
    logger.debug(changes)

    change_count = isamAppliance.invoke_get("Get pending changes count",
                                            "/isam/pending_changes/count")
    logger.debug("Pending change count on appliance is:")
    logger.debug(change_count['data'])
    logger.debug(change_count)

    if change_count['data']['count'] > 0 or len(changes['data']['changes']) > 0:
        logger.info("pending changes found")
        return True
    else:
        return False


def commit(isamAppliance, publish=False, check_mode=False, force=False):
    """
    Commit the current pending changes.
    """
    if force or _changes_available(isamAppliance):
        if check_mode:
            return isamAppliance.create_return_object(changed=True)
        else:
            iviaVersion = isamAppliance.facts['version']
            if publish and ibmsecurity.utilities.tools.version_compare(iviaVersion, "10.0.8.0") >= 0:
                logger.debug("Commit: commit and publish")
                return isamAppliance.invoke_put("Committing the changes (containers)",
                                            f"/isam/pending_changes?publish={publish}",
                                            {})
            else:
                logger.debug("Commit: simple commit")
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
    if force or _changes_available(isamAppliance):
        if check_mode:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post("Commit and Restart",
                                             "/restarts/commit_and_restart",
                                             {})
    return isamAppliance.create_return_object()


def reboot_and_wait(isamAppliance, wait_time=300, check_freq=5, check_mode=False, force=False):
    """
    Reboot and wait
    :param isamAppliance:
    :param wait_time:
    :param check_freq:
    :param check_mode:
    :param force:
    :return:
    """
    warnings = []
    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:
        firmware = ibmsecurity.isam.base.firmware.get(isamAppliance, check_mode=check_mode, force=force)

        ret_obj = reboot(isamAppliance)

        if ret_obj['rc'] == 0:
            sec = 0

            # Now check if it is up and running
            while 1:
                ret_obj = ibmsecurity.isam.base.firmware.get(isamAppliance, check_mode=check_mode, force=force,
                                                             ignore_error=True)

                # check partition last_boot time
                if ret_obj['rc'] == 0 and isinstance(ret_obj['data'], list) and len(ret_obj['data']) > 0 and \
                        (('last_boot' in ret_obj['data'][0] and ret_obj['data'][0]['last_boot'] != firmware['data'][0][
                            'last_boot'] and ret_obj['data'][0]['active'] == True) or (
                                 'last_boot' in ret_obj['data'][1] and ret_obj['data'][1]['last_boot'] !=
                                 firmware['data'][1]['last_boot'] and ret_obj['data'][1]['active'] == True)):
                    logger.info("Server is responding and has a different boot time!")
                    return isamAppliance.create_return_object(warnings=warnings)
                else:
                    time.sleep(check_freq)
                    sec += check_freq
                    logger.debug(
                        f"Server is not responding yet. Waited for {sec} secs, next check in {check_freq} secs.")

                if sec >= wait_time:
                    warnings.append(f"Server reboot not detected or completed, exiting... after {sec} seconds")
                    break

    return isamAppliance.create_return_object(warnings=warnings)


def commit_and_restart_and_wait(isamAppliance, wait_time=300, check_freq=5, check_mode=False, force=False):
    """
    Restart LMI after commit
    :param isamAppliance:
    :param wait_time:
    :param check_freq:
    :param check_mode:
    :param force:
    :return:
    """
    warnings = []
    if check_mode:
        return isamAppliance.create_return_object(changed=True)
    else:
        lmi = ibmsecurity.isam.base.lmi.get(isamAppliance, check_mode=check_mode, force=force)

        ret_obj = commit_and_restart(isamAppliance)

        if ret_obj['rc'] == 0:
            sec = 0

            # Now check if it is up and running
            while 1:
                ret_obj = ibmsecurity.isam.base.lmi.get(isamAppliance, check_mode=check_mode, force=force)

                # check partition last_boot time
                if ret_obj['rc'] == 0 and isinstance(ret_obj['data'], list) and len(ret_obj['data']) > 0 and \
                        ('start_time' in ret_obj['data'][0] and ret_obj['data'][0]['start_time'] != lmi['data'][0][
                            'start_time']):
                    logger.info("LMI is responding and has a different start time!")
                    return isamAppliance.create_return_object(warnings=warnings)
                else:
                    time.sleep(check_freq)
                    sec += check_freq
                    logger.debug(f"LMI is not responding yet. Waited for {sec} secs, next check in {check_freq} secs.")

                if sec >= wait_time:
                    warnings.append(
                        f"The LMI restart not detected or completed, exiting... after {sec} seconds")
                    break

    return isamAppliance.create_return_object(warnings=warnings)


def rollback(isamAppliance, check_mode=False, force=False):
    """
    Rollback the current pending changes.
    """
    if force or _changes_available(isamAppliance):
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete("Rollback the changes",
                                               "/isam/pending_changes")

    return isamAppliance.create_return_object()
