import logging
import ibmsecurity.utilities.tools
import time

logger = logging.getLogger(__name__)


def get(isamAppliance, check_mode=False, force=False):
    """
    Get SNMP Monitoring v1/2
    """
    return isamAppliance.invoke_get("Get FIPS Settings",
                                    "/fips_cfg")


def set(isamAppliance, fipsEnabled=True, tlsv10Enabled=True, tlsv11Enabled=False, check_mode=False, force=False):
    """
    Set FIPS mode
    """
    if force is True or _check(isamAppliance, fipsEnabled, tlsv10Enabled, tlsv11Enabled) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Set FIPS Mode",
                "/fips_cfg",
                {
                    "fipsEnabled": fipsEnabled,
                    "tlsv10Enabled": tlsv10Enabled,
                    "tlsv11Enabled": tlsv11Enabled
                })

    return isamAppliance.create_return_object()


def restart(isamAppliance, check_mode=False, force=False):
    """
    Restart after FIPS configuration changes
    :param isamAppliance:
    :param check_mode:
    :param force:
    :return:
    """
    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:
        return isamAppliance.invoke_put(
            "Restart after FIPS configuration change",
            "/fips_cfg/restart",
            {}
        )


def restart_and_wait(isamAppliance, wait_time=300, check_freq=5, check_mode=False, force=False):
    """
    Restart after FIPS configuration changes
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

        ret_obj = restart(isamAppliance)

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
                        "Server is not responding yet. Waited for {0} secs, next check in {1} secs.".format(sec,
                                                                                                            check_freq))

                if sec >= wait_time:
                    warnings.append(
                        "The FIPS restart not detected or completed, exiting... after {0} seconds".format(sec))
                    break

    return isamAppliance.create_return_object(warnings=warnings)


def _check(isamAppliance, fipsEnabled, tlsv10Enabled, tlsv11Enabled):
    ret_obj = get(isamAppliance)

    if ret_obj['data']['fipsEnabled'] != fipsEnabled:
        logger.info("fipsEnabled change to {0}".format(fipsEnabled))
        return False

    if ret_obj['data']['tlsv10Enabled'] != tlsv10Enabled:
        logger.info("TLS v1.0 change to {0}".format(tlsv10Enabled))
        return False

    if ret_obj['data']['tlsv11Enabled'] != tlsv11Enabled:
        logger.info("TLS v1.1 change to {0}".format(tlsv11Enabled))
        return False

    return True


def compare(isamAppliance1, isamAppliance2):
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
