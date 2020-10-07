import logging

logger = logging.getLogger(__name__)
requires_modules = ["mga", "federation"]
requires_model = "Appliance"

def get(isamAppliance, check_mode=False, force=False):
    """
    Get runtime tuning settings
    """
    return isamAppliance.invoke_get("Retrieving runtime tuning parameters",
                                    "/mga/runtime_tuning/v1",
                                    requires_modules=requires_modules,requires_model=requires_model)


def set(isamAppliance, option, value, check_mode=False, force=False):

#    ret_obj = get(isamAppliance)
#    for key, val in ret_obj.items():
#        if key == 'warnings' and val != []:
#            if "Docker" in val[0]:
#                return isamAppliance.create_return_object(warnings=ret_obj['warnings'])
    """
    Set a runtime tuning parameter
    """
    warnings = []
    matches, exists = False, False
    if force is False:
        matches, exists, warnings = _check(isamAppliance, option, value)

    if exists is False:
        warnings.append("Tuning Parameter {0} was not found. set() request will attempt anyway.".format(option))

    if force is True or matches is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True,warnings=warnings)
        else:
            return isamAppliance.invoke_put(
                "Setting a runtime tuning parameter",
                "/mga/runtime_tuning/{0}/v1".format(option),
                {
                    'value': value
                }, requires_modules=requires_modules,requires_model=requires_model)

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
            logger.info("Tuning parameter {0}/{1} already set.".format(option, value))
            matches = True
        else:
            logger.info(
                "Tuning parameter {0} value does not match {1} != {2}.".format(option, ret_obj['data'][option], value))
        exists = True
    except:
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

    if force is True or exists is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True,warnings=warnings)
        else:
            return isamAppliance.invoke_delete(
                "Reset a runtime tuning parameter to default value",
                "/mga/runtime_tuning/{0}/v1".format(option),
                requires_modules=requires_modules,requires_model=requires_model)
    elif exists is False and warnings == []:
        warnings.append("Tuning Parameter {0} was not found. Skipping reset() request.".format(option))

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
