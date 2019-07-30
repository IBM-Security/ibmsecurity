import logging
from ibmsecurity.utilities.tools import json_sort

logger = logging.getLogger(__name__)

# URI for this module
uri = "/iam/access/v8/alias_settings"
requires_modules = ["federation"]
requires_version = "9.0.6.0"


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieve alias associations
    """
    return isamAppliance.invoke_get("Retrieve alias associations", "{0}".format(uri),
                                    requires_modules=requires_modules,
                                    requires_version=requires_version)


def update(isamAppliance, aliasDBType, properties=None, check_mode=False, force=False):
    """
    Update the alias settings
    """
    ret_obj = get(isamAppliance)
    update_required = False

    if ret_obj['data']['aliasDBType'] == aliasDBType:
        if 'properties' in ret_obj['data']:
            props = ret_obj['data']['properties']
            sorted_props = json_sort(props)
            sorted_properties = json_sort(properties)
            if sorted_props != sorted_properties:
                update_required = True
    else:
        update_required = True

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Update the alias settings",
                "{0}".format(uri),
                {
                    'aliasDBType': aliasDBType,
                    'properties': properties
                },
                requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object()
