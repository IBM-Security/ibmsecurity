import logging

logger = logging.getLogger(__name__)


def reboot(isvgAppliance, check_mode=False, force=False):
    """
    Reboot the appliance
    """
    if check_mode is True:
        return isvgAppliance.create_return_object(changed=True)
    else:
        # obtain appliance lastboot time
        import ibmsecurity.isvg.firmware
        import time
        ret_obj_appliance = ibmsecurity.isvg.firmware.get(isvgAppliance)
        for firm in ret_obj_appliance['data']:
            if firm['active'] is True:
                before_reboot_last_boot = firm['last_boot']
                logger.info(
                    "Active partition last boot time {0} before reboot process initiated.".format(before_reboot_last_boot))

        ret_obj = isvgAppliance.invoke_post("Rebooting appliance",
                                         "/diagnostics/restart_shutdown/reboot",
                                         {})

        # Depending on resource allocated, isvg appliance can take up to 30s or more before it reboots
        # after it is being told to do so.
        # Loop until appliance returns an error, or reboot is detected, before returning control.
        try:
            while True:
                ret_obj_appliance = ibmsecurity.isvg.firmware.get(isvgAppliance)
                for firm in ret_obj_appliance['data']:
                    if firm['active'] is True:
                        last_boot = firm['last_boot']
                        logger.info(
                            "Active partition last boot time {0} after reboot process initiated.".format(last_boot))
                        if last_boot > before_reboot_last_boot:
                            raise Exception ("Break out of loop")
                time.sleep(15)
        except Exception as e:
            logger.debug("Exception occured: {0}. Assuming appliance has now initiated reboot process".format(e))
            pass

        return ret_obj


def shutdown(isvgAppliance, check_mode=False, force=False):
    """
    Shutdown the appliance
    """
    if check_mode is True:
        return isvgAppliance.create_return_object(changed=True)
    else:
        return isvgAppliance.invoke_post("Shutting down appliance",
                                         "/diagnostics/restart_shutdown/shutdown",
                                         {})


def _changes_available(isvgAppliance):
    """
    Check for pending changes on the appliance
    :param isvgAppliance:
    :return:
    """
    #    changes = isvgAppliance.invoke_get("Get pending changes",
    #                                       "/pending_changes")
    #    logger.debug("Pending changes on appliance are:")
    #    logger.debug(changes['data'])
    #
    #    change_count = isvgAppliance.invoke_get("Get pending changes count",
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


def commit(isvgAppliance, check_mode=False, force=False):
    """
    Commit the current pending changes.
    """
    if force is True or _changes_available(isvgAppliance) is True:
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True)
        else:
            return isvgAppliance.invoke_get("Committing the changes",
                                            "/pending_changes/deploy",
                                            {})

    return isvgAppliance.create_return_object()


def commit_and_restart(isvgAppliance, check_mode=False, force=False):
    """
    Commit and Restart LMI
    :param isvgAppliance:
    :param check_mode:
    :param force:
    :return:
    """
    if force is True or _changes_available(isvgAppliance) is True:
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True)
        else:
            return isvgAppliance.invoke_post("Commit and Restart",
                                             "/restarts/commit_and_restart",
                                             {})
    return isvgAppliance.create_return_object()


def rollback(isvgAppliance, check_mode=False, force=False):
    """
    Rollback the current pending changes.
    """
    if force is True or _changes_available(isvgAppliance) is True:
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True)
        else:
            return isvgAppliance.invoke_get("Rollback the changes",
                                            "/pending_changes/forget")

    return isvgAppliance.create_return_object()
