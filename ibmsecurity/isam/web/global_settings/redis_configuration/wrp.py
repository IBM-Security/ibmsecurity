import logging
import ibmsecurity

import ibmsecurity.isam.web.reverse_proxy.instance

from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

uri = "/wga/redis_config/wrp"
requires_modules = ["wga"]
requires_version = "10.0.1"


def get(isamAppliance, name, check_mode=False, force=False):
    """
    Retrieve the Redis collections configured for a specific Web Reverse Proxy
    """
    return isamAppliance.invoke_get("Retrieve the Redis collections configured for a specific Web",
                                    "{0}/{1}".format(uri, name),
                                    requires_modules=requires_modules, requires_version=requires_version)


def update(isamAppliance, name, input_data=[], check_mode=False, force=False):
    """
    Update the Redis collections which are used by a Web Reverse Proxy
    """

    exist, warnings = _check_exist(isamAppliance, name)
    if exist is True:
        same_contents, warnings = _check_contents(isamAppliance=isamAppliance, name=name, input_data=input_data)
    else:
        return isamAppliance.create_return_object(warnings=warnings)

    if force is True or same_contents is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Update the Redis collections which are used by a Web Reverse Proxy",
                "{0}/{1}".format(uri, name),
                input_data,
                requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object(warnings=warnings)


def _check_exist(isamAppliance, name):
    ret_obj = ibmsecurity.isam.web.reverse_proxy.instance.get(isamAppliance)

    for rp in ret_obj['data']:
        if rp['id'] == name:
            return True, ret_obj['warnings']

    return False, ret_obj['warnings']


def _check_contents(isamAppliance, name, input_data):
    ret_obj = get(isamAppliance, name)

    if ret_obj['data'] == input_data:
        return True, ret_obj['warnings']
    else:
        return False, ret_obj['warnings']


def compare(isamAppliance1, isamAppliance2, name1, name2=None):
    if name2 is None or name1 == '':
        name2 = name1
    ret_obj1 = get(isamAppliance1, name1)
    ret_obj2 = get(isamAppliance2, name2)

    return tools.json_compare(ret_obj1, ret_obj2)
