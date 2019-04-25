import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get(isdsAppliance, check_mode=False, force=False):
    """
    Retrieving the administrator settings
    """
    return isdsAppliance.invoke_get("Retrieving the administrator settings", "/admin_cfg")


def set_pw(isdsAppliance, newPassword, oldPassword, sessionTimeout="30", check_mode=False, force=False):
    """
    Set password for admin user (super user for appliance)
    """
    warnings = ["Password change requested - cannot query existing password for idempotency check."]
    if check_mode is True:
        return isdsAppliance.create_return_object(changed=True, warnings=warnings)
    else:
        json_data = {
            "oldPassword": oldPassword,
            "newPassword": newPassword,
            "confirmPassword": newPassword,
            "sessionTimeout": sessionTimeout
        }

        return isdsAppliance.invoke_put("Setting admin password", "/admin_cfg", json_data, warnings=warnings)


def set(isdsAppliance, oldPassword=None, newPassword=None, sessionTimeout=30, check_mode=False, force=False):
    """
    Updating the administrator settings
    """
    warnings = []
    if force is False:
        update_required, warnings, json_data = _check(isdsAppliance, oldPassword, newPassword, sessionTimeout, warnings)

    if force is True or update_required is True:
        if check_mode is True:
            return isdsAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isdsAppliance.invoke_put(
                "Updating the administrator settings",
                "/admin_cfg", json_data, warnings=warnings)

    return isdsAppliance.create_return_object(changed=False, warnings=warnings)


def _check(isdsAppliance, oldPassword, newPassword, sessionTimeout, warnings):
    """
    Check whether target key has already been set with the value
    :param isdsAppliance:
    :param key:
    :param value:
    :return: True/False
    """
    ret_obj = get(isdsAppliance)

    json_data = {
        "sessionTimeout": sessionTimeout
    }
    if oldPassword is not None:
        json_data["oldPassword"] = oldPassword
        if newPassword is None:
            warnings.append("Please provide new password, when old password is specified.")
    if newPassword is not None:
        warnings.append("Password change requested - cannot query existing password for idempotency check.")
        json_data["newPassword"] = newPassword
        json_data["confirmPassword"] = newPassword
        if oldPassword is None:
            warnings.append("Please provide old password, when new password is specified.")

    if ibmsecurity.utilities.tools.json_sort(json_data) != ibmsecurity.utilities.tools.json_sort(ret_obj['data']):
        logger.debug("Admin Settings are found to be different. See following JSON for difference.")
        logger.debug("New JSON: {0}".format(ibmsecurity.utilities.tools.json_sort(json_data)))
        logger.debug("Old JSON: {0}".format(ibmsecurity.utilities.tools.json_sort(ret_obj['data'])))
        return True, warnings, json_data
    else:  # No changes required
        return False, warnings, json_data


def compare(isdsAppliance1, isdsAppliance2):
    """
    Compare advanced tuning parameters between two appliances
    """
    ret_obj1 = get(isdsAppliance1)
    ret_obj2 = get(isdsAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2)
