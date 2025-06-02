import logging
import ibmsecurity.utilities.tools as _tools

logger = logging.getLogger(__name__)
requires_modules = ["mga", "federation"]
requires_model = "Appliance"


def get(isamAppliance, check_mode=False, force=False):
    """
    Get runtime tuning settings
    """
    return isamAppliance.invoke_get("Retrieving runtime tuning parameters",
                                    "/mga/runtime_tuning/v1",
                                    requires_modules=requires_modules,
                                    requires_model=requires_model)


def set(isamAppliance, option=None, value=None, values=None, ignore_endpoints=True, check_mode=False, force=False):
    """
    Set a runtime tuning parameter
    option and value are mutually exclusive with values
    Set multiple runtime tuning parameters at once (if values is not none)
    """
    warnings = []
    matches, exists = False, False
    if values is not None:
        # Use the multi option.  Ignore option/value in this case
        return _setMultipleValues(isamAppliance, values, ignore_endpoints, check_mode, force)

    if not force:
        matches, exists, warnings = _check(isamAppliance, option, value)

    if not exists:
        warnings.append(f"Tuning Parameter {option} was not found. set() request will attempt anyway.")

    if force is True or matches is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_put(
                "Setting a runtime tuning parameter",
                f"/mga/runtime_tuning/{option}/v1",
                {
                    'value': value
                }, requires_modules=requires_modules, requires_model=requires_model)

    return isamAppliance.create_return_object(warnings=warnings)


def _setMultipleValues(isamAppliance, values=None,  ignore_endpoints=True, check_mode=False, force=False):
    """
    Ignore_endpoints does not take the endpoint configuration into account.
    This is typically set using the specific endpoint configurations.
    """
    currentRuntimeParameters = get(isamAppliance)
    warnings = []
    logger.debug("Setting multiple values for runtime tuning parameters")
    if ignore_endpoints:
        logger.info("Ignoring endpoint configuration in comparison")
        warnings.append("Ignoring endpoint configuration in comparison")
        currentRuntimeParameters.pop("endpoints", None)
        values.pop("endpoints", None)
    if force or not _tools.json_equals(currentRuntimeParameters, values):
        if check_mode:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_put(
                "Setting multiple runtime tuning parameters",
                "/mga/runtime_tuning/v1",
                values,
                requires_modules=requires_modules, requires_model=requires_model)

    return isamAppliance.create_return_object(warnings=warnings)


def _check(isamAppliance, option, value):
    """
    Check if tuning parameter option exists and matches value
    """
    ret_obj = get(isamAppliance)
    warnings = ret_obj['warnings']

    matches = False
    exists = False
    try:
        if str(ret_obj['data'][option]) == str(value):
            logger.info(f"Tuning parameter {option}/{value} already set.")
            matches = True
        else:
            logger.info(
                f"Tuning parameter {option} value does not match {ret_obj['data'][option]} != {value}.")
        exists = True
    except Exception:
        logger.info("Runtime tuning parameter does not exist")

    return matches, exists, warnings


def reset(isamAppliance, option, check_mode=False, force=False):
    """
    Reset a tuning parameter
    """
    warnings = []
    matches, exists = False, False

    if force is False:
        matches, exists, warnings = _check(isamAppliance, option, None)

    if force is True or exists:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_delete(
                "Reset a runtime tuning parameter to default value",
                f"/mga/runtime_tuning/{option}/v1",
                requires_modules=requires_modules, requires_model=requires_model)
    elif exists is False and warnings == []:
        warnings.append(f"Tuning Parameter {option} was not found. Skipping reset() request.")

    return isamAppliance.create_return_object(warnings=warnings)


def compare(isamAppliance1, isamAppliance2):
    """
    Compare runtime tuning parameters between two appliances
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    # Ignore differences between endpoints or listening interfaces (compared separately)
    del ret_obj1['data']['endpoints']
    del ret_obj2['data']['endpoints']

    import ibmsecurity.utilities.tools
    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['endpoints'])
