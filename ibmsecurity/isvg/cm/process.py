import logging
from ibmsecurity.utilities import tools
from ibmsecurity.isvg import notifications

logger = logging.getLogger(__name__)

uri = "/widgets/server"

def get(isvgAppliance, check_mode=False, force=False):
    """
    Get Cluster Manager server status
    """
    return isvgAppliance.invoke_get("Retrieving Cluster Manager server status", uri)


def execute(isvgAppliance, operation="restart", check_mode=False, force=False):
    """
    Execute an operation (start, stop or restart) on Cluster Manager server
    """
    check_value, warnings = _check(isvgAppliance, operation)

    if force is True or check_value is True:
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isvgAppliance.invoke_post(
                "Executing an operation on Cluster Manager server", uri + "/" + operation + "/clustermanager",
                {
                    'operation': operation
                }, warnings=warnings)

    return isvgAppliance.create_return_object(warnings=warnings)


def _check(isvgAppliance, operation):
    """
    Check if operation needs to be applied to process
    """
    ret_obj = notifications.get(isvgAppliance)
    warnings = ret_obj['warnings']

    if ret_obj['rc'] == 0 and len(ret_obj['data']) > 0 and 'items' in ret_obj['data']:
        for item in ret_obj['data']['items']:
            # code not tested yet with the right message id
            if 'message' in item and item['message'] == 'identity_was_server_restart_reqd' and operation == "restart":
                logger.info("Cluster Manager server requires a restart")
                return True,warnings
    else:
        logger.info(
            "Executing {0} on Cluster Manager server not required or will not work. Use force if needed.".format(
                operation))
        return False,warnings

    return False,warnings
