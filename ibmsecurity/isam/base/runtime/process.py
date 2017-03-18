import logging

logger = logging.getLogger(__name__)

uri = "/mga/runtime_profile/local/v1"
requires_modules = ["mga", "federation"]
requires_version = "8.0.0.0"


def get(isamAppliance, check_mode=False, force=False):
    """
    Get runtime status
    """
    return isamAppliance.invoke_get("Retrieving runtime status",
                                    "/mga/runtime_profile/v1",
                                    requires_modules=requires_modules, requires_version=requires_version)


def execute(isamAppliance, operation="restart", check_mode=False, force=False):
    """
    Execute an operation (start, stop or restart) on runtime
    """
    if force is True or _check(isamAppliance, operation) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Executing an operation on runtime", uri,
                {
                    'operation': operation
                }, requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()


def _check(isamAppliance, operation):
    """
    Check if operation needs to be applied to process
    """
    ret_obj = get(isamAppliance)

    if ret_obj['data']['restart_required'] is True and operation == "restart":
        logger.info("Liberty Runtime process requires a restart")
        return True
    elif ret_obj['data']['return_code'] == 0 and operation == "stop":
        logger.info("Liberty Runtime process is running and can be stopped")
        return True
    elif ret_obj['data']['return_code'] == 1 and operation == "start":
        logger.info("Liberty Runtime process is not running and can be started")
        return True
    elif ret_obj['data']['reload_required'] is True and operation == "reload":
        logger.info("Liberty Runtime process requires reload")
        return True
    else:
        logger.info("Executing {0} on Liberty Runtime process not required or will not work. Use force if needed.".format(operation))
        return False
