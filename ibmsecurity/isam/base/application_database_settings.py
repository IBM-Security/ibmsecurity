import logging
import ibmsecurity.utilities.tools

try:
    basestring
except NameError:
    basestring = (str, bytes)

logger = logging.getLogger(__name__)

# URI for this module
uri = "/core/dca_updates_cfg"
requires_modules = None
requires_version = None


def get(isamAppliance, check_mode=False, force=False):
    """
    Get Application Database Settings
    """
    return isamAppliance.invoke_get("Get Application Database Settings", uri, requires_modules=requires_modules,
                                    requires_version=requires_version)


def set(isamAppliance, enableIprAutoUpdate=True, useProxy=False, proxyHost=None, proxyPort=None, useProxyAuth=False,
        proxyUser=None, proxyPwd=None, enableAutoUpdate=True, enableIprFeedback=False, enableWeblearn=False,
        includeIprInfo=False, check_mode=False, force=False):
    """
    Set Application Database Settings
    """
    update_required, json_data = _check(isamAppliance, enableIprAutoUpdate=enableIprAutoUpdate, useProxy=useProxy,
                                        proxyHost=proxyHost, proxyPort=proxyPort, useProxyAuth=useProxyAuth,
                                        proxyUser=proxyUser, proxyPwd=proxyPwd, enableAutoUpdate=enableAutoUpdate,
                                        enableIprFeedback=enableIprFeedback, enableWeblearn=enableWeblearn,
                                        includeIprInfo=includeIprInfo)

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put("Set Application Database Settings", uri, json_data,
                                            requires_modules=requires_modules,
                                            requires_version=requires_version)

    return isamAppliance.create_return_object()


def _check(isamAppliance, enableIprAutoUpdate, useProxy, proxyHost, proxyPort, useProxyAuth, proxyUser, proxyPwd,
           enableAutoUpdate, enableIprFeedback, enableWeblearn, includeIprInfo):
    update_required = False

    # compare will fail if port is provided as string
    if proxyPort is not None and isinstance(proxyPort, basestring):
        proxyPort = int(proxyPort)

    # Create input JSON
    json_data = {
        "config": {
            'enableAutoUpdate': enableAutoUpdate,
            'enableIprAutoUpdate': enableIprAutoUpdate,
            'enableIprFeedback': enableIprFeedback,
            'enableWeblearn': enableWeblearn,
            'includeIprInfo': includeIprInfo,
            'proxyHost': proxyHost,
            'proxyPort': proxyPort,
            'proxyPwd': proxyPwd,
            'proxyUser': proxyUser,
            'useProxy': useProxy,
            'useProxyAuth': useProxyAuth
        }
    }

    # Extract current settings
    ret_obj = get(isamAppliance)

    # Compare to establish idempotency
    sorted_json_data = ibmsecurity.utilities.tools.json_sort(json_data)
    logger.debug("Sorted input: {0}".format(sorted_json_data))
    sorted_ret_obj = ibmsecurity.utilities.tools.json_sort(ret_obj['data'])
    logger.debug("Sorted existing data: {0}".format(sorted_ret_obj))
    if sorted_ret_obj != sorted_json_data:
        logger.info("Changes detected, update needed.")
        update_required = True

    return update_required, json_data


def compare(isamAppliance1, isamAppliance2):
    """
    Compare Application Database Settings between two appliances
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
