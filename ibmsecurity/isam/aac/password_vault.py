import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/mga/password_vault/"
requires_modules = ["federation", "mga"]
requires_version = "10.0.1"


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the password vault configuration
    """
    return isamAppliance.invoke_get("Retrieving the password vault configuration",
                                    f"{uri}",
                                    requires_modules=requires_modules,
                                    requires_version=requires_version)


def update(isamAppliance,
           enabled,
           data_location,
           resources,
           admin_group,
           public_key='',
           check_mode=False,
           force=False):
    """
    Update a password vault configuration
    """

    json_data = {
        'admin_group': admin_group,
        'data_location': data_location,
        'enabled': enabled,
        'resources': resources,
        'public_key': public_key
    }
    update_required, warnings = _check(isamAppliance, json_data)

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True,
                                                      warnings=warnings)
        else:
            return isamAppliance.invoke_put(
                "Update a specified Password vault entry",
                f"{uri}",
                json_data,
                warnings=warnings,
                requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object(warnings=warnings)


def _check(isamAppliance, json_data):
    ret_obj = get(isamAppliance)
    sorted_json1 = tools.json_sort(ret_obj['data'])
    sorted_json2 = tools.json_sort(json_data)

    if sorted_json1 == sorted_json2:
        return False, ret_obj['warnings']
    else:
        return True, ret_obj['warnings']
