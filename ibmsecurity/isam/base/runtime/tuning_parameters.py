import logging

logger = logging.getLogger(__name__)

requires_modules = ["mga", "federation"]

def get(isamAppliance, check_mode=False, force=False):
    """
    Get runtime tuning settings
    """
    return isamAppliance.invoke_get("Retrieving runtime tuning parameters",
                                    "/mga/runtime_tuning/v1",
                                    requires_modules=requires_modules)


def set(isamAppliance, option, value, check_mode=False, force=False):
    """
    Set a runtime tuning parameter
    """
    matches, exists = False, False
    if force is False:
        matches, exists = _check(isamAppliance, option, None)

    if force is True or matches is False:  # will add if not exists
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Setting a runtime tuning parameter",
                "/mga/runtime_tuning/{0}/v1".format(option),
                {
                    'value': value
                }, requires_modules=requires_modules)

    return isamAppliance.create_return_object()


def add_endpoint(isamAppliance, endpoint, port, secure, check_mode=False, force=False):
    """
    Add runtime endpoint
    """
    matches, exists = False, False
    if force is False:
        matches, exists = _check(isamAppliance, endpoint, None)

    if force is True or matches is False:  # will add if not exists
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post(
                "Add runtime endpoint",
                "/mga/runtime_tuning/endpoints/v1",
                {
                    'interface': endpoint,
                    'port': port,
                    'secure': secure
                }, requires_modules=requires_modules)

    return isamAppliance.create_return_object()


def set_endpoint(isamAppliance, endpoint, port, secure, check_mode=False, force=False):
    """
    Set runtime endpoint
    """
    matches, exists = False, False
    if force is False:
        matches, exists = _check(isamAppliance, endpoint, None)

    if force is True or matches is False:  # will add if not exists
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Set runtime endpoint",
                "/mga/runtime_tuning/endpoints/{0}/v1".format(endpoint),
                {
                    'port': port,
                    'secure': secure
                }, requires_modules=requires_modules)

    return isamAppliance.create_return_object()


def delete_endpoint(isamAppliance, endpoint, check_mode=False, force=False):
    """
    Delete runtime endpoint
    """
    matches, exists = False, False
    if force is False:
        matches, exists = _check(isamAppliance, endpoint, None)

    if force is True or matches is False:  # will add if not exists
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Delete runtime endpoint",
                "/mga/runtime_tuning/endpoints/{0}/v1".format(endpoint)
                , requires_modules=requires_modules)

    return isamAppliance.create_return_object()


def _check(isamAppliance, option, value):
    """
    Check if tuning parameter option exists and matches value
    """
    ret_obj = get(isamAppliance)

    matches = False
    exists = False
    try:
        if ret_obj['data'][option] == value:
            logger.info("Runtime tuning parameter [" + option + "] already exists with given value")
            matches = True
        else:
            logger.info("Runtime tuning parameter [" + option + "] already exists")
        exists = True
    except:
        logger.info("Runtime tuning parameter does not exist")

    return matches, exists


def reset(isamAppliance, option, check_mode=False, force=False):
    """
    Reset a tuning parameter
    """
    matches, exists = False, False

    if force is False:
        matches, exists = _check(isamAppliance, option, None)

    if force is True or exists is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Reset a runtime tuning parameter to default value",
                "/mga/runtime_tuning/{0}/v1".format(option),
                requires_modules=requires_modules)

    return isamAppliance.create_return_object()


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
