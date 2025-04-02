import logging
import time
from ibmsecurity.isvg import notifications

logger = logging.getLogger(__name__)


def restart(isvgAppliance, check_mode=False, force=False):
    """
    Restart LMI
    """
    operation = "restart"
    check_value, warnings = _check(isvgAppliance, operation)

    if force is True or check_value is True:
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isvgAppliance.invoke_post(
                "Executing an operation on LMI", "/restarts/restart_server",
                {
                    'operation': operation
                }, warnings=warnings)


def _check(isvgAppliance, operation):
    """
    Check if operation needs to be applied to LMI
    """
    ret_obj = notifications.get(isvgAppliance)
    warnings = ret_obj['warnings']

    if 'items' in ret_obj['data']:
        for item in ret_obj['data']['items']:
            if 'message' in item and item['message'] == 'lmi_restart_reqd' and operation == "restart":
                logger.info("Identity Manager server requires a restart")
                return True,warnings
    else:
        logger.info(
            "Executing {0} on LMI not required or will not work. Use force if needed.".format(
                operation))
        return False,warnings

    return False,warnings
