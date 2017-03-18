import logging
import time
from ibmsecurity.appliance.ibmappliance import IBMError

logger = logging.getLogger(__name__)


def restart(isamAppliance, check_mode=False, force=False):
    """
    Restart LMI
    """
    return isamAppliance.invoke_post("Restarting LMI",
                                     "/restarts/restart_server",
                                     {})


def get(isamAppliance, check_mode=False, force=False):
    """
    Get LMI Status
    """
    # Be sure to ignore server error
    return isamAppliance.invoke_get("Get LMI Status", "/lmi", True)


def await_startup(isamAppliance, wait_time=300, check_mode=False, force=False):
    """
    Wait for appliance to bootup
    Checking lmi responding is best option from REST API perspective
    """

    # Wait for a minute to ensure appliance has stopped responding
    sec = 60
    # Frequency (in seconds) when routine will check if server is up
    check_freq = 20

    # Wait a bit to make sure appliance has shutdown, before checking...
    time.sleep(sec)

    # Now check if it is up and running
    while 1:
        ret_obj = get(isamAppliance)

        if ret_obj['rc'] == 0:
            logger.info("Server is responding!")
            return isamAppliance.create_return_object()
        else:
            time.sleep(check_freq)
            sec += check_freq

        if sec >= wait_time:
            logger.error("The LMI is not responding, exiting... after {0} seconds".format(wait_time))
            raise IBMError("HTTP Return code: 999", "Waited for LMI to respond (typically after a reboot), timed out.")

    return isamAppliance.create_return_object(rc=999)
