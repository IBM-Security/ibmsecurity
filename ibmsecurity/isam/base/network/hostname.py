import logging

logger = logging.getLogger(__name__)

requires_model = "Appliance"


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the general configuration
    """
    return isamAppliance.invoke_get("Retrieving the general configuration", "/net/general", requires_model=requires_model)


def set(isamAppliance, hostname, check_mode=False, force=False):
    """
    Updating the general configuration
    """
    check_obj, warnings = _check(isamAppliance, hostname)

    if force is True or check_obj is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_put("Updating the general configuration", "/net/general",
                                            {
                                                'hostName': hostname
                                            }, requires_model=requires_model)

    return isamAppliance.create_return_object(warnings=warnings)


def _check(isamAppliance, hostname):
    ret_obj = get(isamAppliance)
    warnings = ret_obj['warnings']
    if 'hostName' in ret_obj['data']:
        if ret_obj['data']['hostName'] == hostname:
            return True, warnings
        else:
            return False, warnings
    else:
        return True, warnings
