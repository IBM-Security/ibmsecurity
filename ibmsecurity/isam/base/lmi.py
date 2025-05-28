import logging
import time
from ibmsecurity.appliance.ibmappliance import IBMError

logger = logging.getLogger(__name__)


def restart(isamAppliance, check_mode=False, force=False):
    """
    Restart LMI
    """
    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:
        return isamAppliance.invoke_post("Restarting LMI", "/restarts/restart_server", {})


def get(isamAppliance, check_mode=False, force=False):
    """
    Get LMI Status
    """
    # Be sure to ignore server error
    return isamAppliance.invoke_get("Get LMI Status", "/lmi", ignore_error=True)


def await_startup(isamAppliance, wait_time=300, check_freq=5, start_time=None, check_mode=False, force=False):
    """
    Wait for appliance to bootup or LMI to restart
    Checking lmi responding is best option from REST API perspective

    # Frequency (in seconds) when routine will check if server is up
    # check_freq (seconds)

    # Ideally start_time should be taken before restart request is send to LMI
    # start_time (REST API standard)

    # Time to wait for appliance/lmi to respond and have a different start time
    # wait_time (seconds)

    # Note: This function will not work unless first steps are completed.
    """
    # Get the current start_time if not provided
    if start_time is None:
        ret_obj = get(isamAppliance)
        start_time = ret_obj['data'][0]['start_time']

    sec = 0
    warnings = []

    # Now check if it is up and running
    while 1:
        ret_obj = get(isamAppliance)

        if ret_obj['rc'] == 0 and isinstance(ret_obj['data'], list) and len(ret_obj['data']) > 0 and 'start_time' in \
                ret_obj['data'][0] and ret_obj['data'][0]['start_time'] != start_time:
            logger.info("Server is responding and has a different start time!")
            return isamAppliance.create_return_object(warnings=warnings)
        else:
            time.sleep(check_freq)
            sec += check_freq
            logger.debug(
                f"Server is not responding yet. Waited for {sec} secs, next check in {check_freq} secs.")

        if sec >= wait_time:
            warnings.append(f"The LMI restart not detected or completed, exiting... after {sec} seconds")
            break

    return isamAppliance.create_return_object(warnings=warnings)


def restart_and_wait(isamAppliance, wait_time=300, check_freq=5, check_mode=False, force=False):
    ret_obj = get(isamAppliance)
    _start_time = ret_obj['data'][0]['start_time']

    restart(isamAppliance, check_mode, force)

    return await_startup(isamAppliance, wait_time=wait_time, check_freq=check_freq, start_time=_start_time,
                         check_mode=False, force=False)
