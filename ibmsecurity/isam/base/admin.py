import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the administrator settings
    """
    return isamAppliance.invoke_get("Retrieving the administrator settings", "/admin_cfg")


def set_pw(isamAppliance, oldPassword, newPassword, sessionTimeout="30", httpsPort=None, check_mode=False, force=False):
    """
    Set password for admin user (super user for appliance)
    
    Note: this function is being maintained for backward compatibility. Use set() going forward.
    """
    warnings = ["Password change requested - cannot query existing password for idempotency check."]
    if check_mode is True:
        return isamAppliance.create_return_object(changed=True, warnings=warnings)
    else:
        json_data = {
            "oldPassword": oldPassword,
            "newPassword": newPassword,
            "confirmPassword": newPassword,
            "sessionTimeout": sessionTimeout
        }
        if httpsPort is not None:
            if isamAppliance.facts["version"] < "9.0.1.0":
                warnings.append(
                    "Appliance at version: {0}, httpsPort not supported. Needs 9.0.1.0 or higher. Ignoring httpsPort for this call.")
            else:
                json_data['httpsPort'] = httpsPort
        else:
            if isamAppliance.facts["version"] < "9.0.1.0":
                pass  # Can safely ignore httpsPort
            else:
                warnings.append("Default httpsPort of 443 will be set on the appliance.")
        return isamAppliance.invoke_put("Setting admin password", "/core/admin_cfg", json_data, warnings=warnings)


def set(isamAppliance, oldPassword=None, newPassword=None, minHeapSize=None, maxHeapSize=None, sessionTimeout=30,
        httpPort=None, httpsPort=None, minThreads=None, maxThreads=None, maxPoolSize=None, lmiDebuggingEnabled=None,
        consoleLogLevel=None, acceptClientCerts=None, validateClientCertIdentity=None, excludeCsrfChecking=None,
        enableSSLv3=None, maxFiles=None, maxFileSize=None, check_mode=False, force=False):
    """
    Updating the administrator settings
    """
    warnings = []
    if force is False:
        update_required, warnings, json_data = _check(isamAppliance, oldPassword, newPassword, minHeapSize, maxHeapSize,
                                                      sessionTimeout, httpPort, httpsPort, minThreads, maxThreads,
                                                      maxPoolSize, lmiDebuggingEnabled, consoleLogLevel,
                                                      acceptClientCerts, validateClientCertIdentity,
                                                      excludeCsrfChecking, enableSSLv3, maxFiles, maxFileSize, warnings)

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_put(
                "Updating the administrator settings",
                "/core/admin_cfg", json_data, warnings=warnings)

    return isamAppliance.create_return_object(changed=False, warnings=warnings)


def _check(isamAppliance, oldPassword, newPassword, minHeapSize, maxHeapSize, sessionTimeout, httpPort, httpsPort,
           minThreads, maxThreads, maxPoolSize, lmiDebuggingEnabled, consoleLogLevel, acceptClientCerts,
           validateClientCertIdentity, excludeCsrfChecking, enableSSLv3, maxFiles, maxFileSize, warnings):
    """
    Check whether target key has already been set with the value
    :param isamAppliance:
    :param key:
    :param value:
    :return: True/False
    """
    ret_obj = get(isamAppliance)

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
    if isamAppliance.facts["version"] < "9.0.1.0":
        if minHeapSize is not None or maxHeapSize is not None or httpPort is not None or httpsPort is not None or \
                        minThreads is not None or maxThreads is not None or maxPoolSize is not None or \
                        lmiDebuggingEnabled is not None or consoleLogLevel is not None or \
                        acceptClientCerts is not None or validateClientCertIdentity is not None or \
                        excludeCsrfChecking is not None or enableSSLv3 is not None or maxFiles is not None or \
                        maxFileSize is not None:
            warnings.append(
                "Appliance at version: {0}, only oldPassword, newPassword, sessionTimeout are supported. Needs 9.0.1.0 or higher. Ignoring other attributes for this call.")
    else:
        if minHeapSize is not None:
            json_data["minHeapSize"] = int(minHeapSize)
        elif 'minHeapSize' in ret_obj['data']:
            del ret_obj['data']['minHeapSize']
        if maxHeapSize is not None:
            json_data["maxHeapSize"] = int(maxHeapSize)
        elif 'maxHeapSize' in ret_obj['data']:
            del ret_obj['data']['maxHeapSize']
        if httpPort is not None:
            json_data["httpPort"] = int(httpPort)
        elif 'httpPort' in ret_obj['data']:
            del ret_obj['data']['httpPort']
        if httpsPort is not None:
            json_data["httpsPort"] = int(httpsPort)
        elif 'httpsPort' in ret_obj['data']:
            del ret_obj['data']['httpsPort']
        if minThreads is not None:
            json_data["minThreads"] = int(minThreads)
        elif 'minThreads' in ret_obj['data']:
            del ret_obj['data']['minThreads']
        if maxThreads is not None:
            json_data["maxThreads"] = int(maxThreads)
        elif 'maxThreads' in ret_obj['data']:
            del ret_obj['data']['maxThreads']
        if maxPoolSize is not None:
            json_data["maxPoolSize"] = int(maxPoolSize)
        elif 'maxPoolSize' in ret_obj['data']:
            del ret_obj['data']['maxPoolSize']
        if lmiDebuggingEnabled is not None:
            json_data["lmiDebuggingEnabled"] = lmiDebuggingEnabled
        elif 'lmiDebuggingEnabled' in ret_obj['data']:
            del ret_obj['data']['lmiDebuggingEnabled']
        if consoleLogLevel is not None:
            json_data["consoleLogLevel"] = int(consoleLogLevel)
            if 'consoleLogLevel' in ret_obj['data'] and ret_obj['data']['consoleLogLevel'] == 'OFF':
                ret_obj['data']['consoleLogLevel'] = 0
        elif 'consoleLogLevel' in ret_obj['data']:
            del ret_obj['data']['consoleLogLevel']
        if acceptClientCerts is not None:
            json_data["acceptClientCerts"] = acceptClientCerts
        elif 'acceptClientCerts' in ret_obj['data']:
            del ret_obj['data']['acceptClientCerts']
        if validateClientCertIdentity is not None:
            json_data["validateClientCertIdentity"] = validateClientCertIdentity
        elif 'validateClientCertIdentity' in ret_obj['data']:
            del ret_obj['data']['validateClientCertIdentity']
        if excludeCsrfChecking is not None:
            json_data["excludeCsrfChecking"] = excludeCsrfChecking
        elif 'excludeCsrfChecking' in ret_obj['data']:
            del ret_obj['data']['excludeCsrfChecking']
        if enableSSLv3 is not None:
            json_data["enableSSLv3"] = enableSSLv3
        elif 'enableSSLv3' in ret_obj['data']:
            del ret_obj['data']['enableSSLv3']
        if maxFiles is not None:
            json_data["maxFiles"] = int(maxFiles)
        elif 'maxFiles' in ret_obj['data']:
            del ret_obj['data']['maxFiles']
        if maxFileSize is not None:
            json_data["maxFileSize"] = int(maxFileSize)
        elif 'maxFileSize' in ret_obj['data']:
            del ret_obj['data']['maxFileSize']

    if ibmsecurity.utilities.tools.json_sort(json_data) != ibmsecurity.utilities.tools.json_sort(ret_obj['data']):
        logger.debug("Admin Settings are found to be different. See following JSON for difference.")
        logger.debug("New JSON: {0}".format(ibmsecurity.utilities.tools.json_sort(json_data)))
        logger.debug("Old JSON: {0}".format(ibmsecurity.utilities.tools.json_sort(ret_obj['data'])))
        # Ensure users know how REST API handles httpsPort default value
        if httpsPort is None and isamAppliance.facts["version"] >= "9.0.1.0":
            warnings.append("Default httpsPort of 443 will be set on the appliance.")
        return True, warnings, json_data
    else:  # No changes required
        return False, warnings, json_data


def compare(isamAppliance1, isamAppliance2):
    """
    Compare advanced tuning parameters between two appliances
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2)
