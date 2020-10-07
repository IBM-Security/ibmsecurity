import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

uri = "/mga/runtime_profile/local/v1"
requires_modules = ["mga", "federation"]
requires_version = "8.0.0.0"
requires_model = "Appliance"

def get(isamAppliance, check_mode=False, force=False):
    """
    Get runtime status
    """
    return isamAppliance.invoke_get("Retrieving runtime status",
                                    "/mga/runtime_profile/v1",
                                    requires_modules=requires_modules, requires_version=requires_version,requires_model=requires_model)


def execute(isamAppliance, operation="restart", check_mode=False, force=False):
    """
    Execute an operation (start, stop or restart) on runtime
    """
    check_value, warnings = _check(isamAppliance,operation)

    # Reload function is new to ISAM v9.0.2.0
    if operation == "reload" and tools.version_compare(isamAppliance.facts["version"], "9.0.2.0") < 0:
        warnings.append(
            "Appliance is at version {0}, reload requires atleast v9.0.2.0".format(isamAppliance.facts['version']))
        return isamAppliance.create_return_object(warnings=warnings)

    if force is True or check_value is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_put(
                "Executing an operation on runtime", uri,
                {
                    'operation': operation
                }, requires_modules=requires_modules, requires_version=requires_version, warnings=warnings)

    return isamAppliance.create_return_object(warnings=warnings)


def _check(isamAppliance, operation):
    """
    Check if operation needs to be applied to process
    """
    ret_obj = get(isamAppliance)
    warnings = ret_obj['warnings']

    if 'restart_required' in ret_obj['data'] and ret_obj['data']['restart_required'] is True and operation == "restart":
        logger.info("Liberty Runtime process requires a restart")
        return True,warnings
    elif 'return_code' in ret_obj['data'] and ret_obj['data']['return_code'] == 0 and operation == "stop":
        logger.info("Liberty Runtime process is running and can be stopped")
        return True,warnings
    elif 'return_code' in ret_obj['data'] and ret_obj['data']['return_code'] == 1 and operation == "start":
        logger.info("Liberty Runtime process is not running and can be started")
        return True,warnings
    elif 'reload_required' in ret_obj['data'] and ret_obj['data']['reload_required'] is True and operation == "reload":
        logger.info("Liberty Runtime process requires reload")
        return True,warnings
    else:
        logger.info(
            "Executing {0} on Liberty Runtime process not required or will not work. Use force if needed.".format(
                operation))
        return False,warnings
