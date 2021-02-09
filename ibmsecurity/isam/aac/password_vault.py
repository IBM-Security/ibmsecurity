import logging
from ibmsecurity.utilities import tools
from io import open

logger = logging.getLogger(__name__)

# URI for this module
uri = "/mga/password_vault/"
requires_modules = ["federation", "mga"]
requires_version = "10.0.0"


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the password vault configuration
    """
    return isamAppliance.invoke_get("Retrieving the password vault configuration",
                                    "{0}".format(uri),
                                    requires_modules=requires_modules, requires_version=requires_version)


def update(isamAppliance, enabled, data_location, resources, admin_group, public_key=None, check_mode=False,
           force=False):
    """
    Update a specified Risk Profile
    """

    json_data = {
        'admin_group': admin_group,
        'data_location': data_location,
        'enabled': enabled,
        'public_key': public_key,
        'resources': resources
    }
    update_required, warnings = _check(isamAppliance, json_data, public_key)

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Update a specified Risk Profile",
                "{0}".format(uri), json_data)

    return isamAppliance.create_return_object(warnings=warnings)


def _check(isamAppliance, json_data, public_key):
    ret_obj = get(isamAppliance)
    sorted_json1 = tools.json_sort(ret_obj['data'])

    if public_key is None:
        if 'public_key' in ret_obj['data']:
            json_data['public_key'] = ret_obj['data']['public_key']
        else:
            return False, ret_obj['warnings']

    sorted_json2 = tools.json_sort(json_data)

    if sorted_json1 == sorted_json2:
        return False, ret_obj['warnings']
    else:
        return True, ret_obj['warnings']
