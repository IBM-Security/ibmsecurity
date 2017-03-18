import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)

def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the administrator settings
    """
    return isamAppliance.invoke_get("Retrieving the administrator settings", "/admin_cfg")


def set_pw(isamAppliance, oldPassword, newPassword, sessionTimeout="30", check_mode=False, force=False):
    """
    Set password for admin user (super user for appliance)
    """
    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:
        return isamAppliance.invoke_put("Setting admin password", "/core/admin_cfg",
                                        {
                                            "oldPassword": oldPassword,
                                            "newPassword": newPassword,
                                            "confirmPassword": newPassword,
                                            "sessionTimeout": sessionTimeout
                                        })


def set(isamAppliance, key, value, check_mode=False, force=False):
    """
    Set admin parameters
    :param isamAppliance:
    :param key
    :param value
        "validateClientCertIdentity":false,
        "lmiDebuggingEnabled":false,
        "consoleLogLevel":"OFF",
        "minThreads":-1,
        "sessionTimeout":720,
        "maxFileSize":20,
        "enableSSLv3":false,
        "acceptClientCerts":true,
        "maxThreads":-1,
        "httpsPort":443,
        "maxPoolSize":100,
        "maxFiles":2
    :param check_mode:
    :param force:
    :return:
    """

    if force is True or _check(isamAppliance, key, value) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Modifying admin_cfg parameter",
                "/core/admin_cfg",
                {
                    key: value
                })

    return isamAppliance.create_return_object(changed=False)


def _check(isamAppliance, key, value):
    """
    Check whether target key has already been set with the value
    :param isamAppliance:
    :param key:
    :param value:
    :return: True/False
    """

    ret_obj = get(isamAppliance)

    rc = False

    numKeys = [ "minThreads","sessionTimeout", "maxFileSize","maxThreads", "httpsPort", "maxPoolSize", "maxFiles"]

    if key in ret_obj['data']:
        if key in numKeys:
            if ret_obj['data'][key] == int(value):
                logger.info("admin parameter [" + key + "] already has the value [" + value + "]")
                rc = True
        else:
            if ret_obj['data'][key] == value:
                logger.info("admin parameter [" + key + "] already has the value [" + value + "]")
                rc = True

    return rc


def compare(isamAppliance1, isamAppliance2):
    """
    Compare advanced tuning parameters between two appliances
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2)
