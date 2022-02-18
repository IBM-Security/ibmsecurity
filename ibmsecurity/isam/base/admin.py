import logging
import ibmsecurity.utilities.tools
import json

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
            if ibmsecurity.utilities.tools.version_compare(isamAppliance.facts["version"], "9.0.1.0") < 0:
                warnings.append(
                    "Appliance at version: {0}, httpsPort not supported. Needs 9.0.1.0 or higher. Ignoring httpsPort for this call.")
            else:
                json_data['httpsPort'] = httpsPort
        else:
            if ibmsecurity.utilities.tools.version_compare(isamAppliance.facts["version"], "9.0.1.0") < 0:
                pass  # Can safely ignore httpsPort
            else:
                warnings.append("Default httpsPort of 443 will be set on the appliance.")
        return isamAppliance.invoke_put("Setting admin password", "/core/admin_cfg", json_data, warnings=warnings)


def set(isamAppliance, oldPassword=None, newPassword=None, minHeapSize=None, maxHeapSize=None, sessionTimeout=30,
        httpPort=None, httpsPort=None, minThreads=None, maxThreads=None, maxPoolSize=None, lmiDebuggingEnabled=None,
        consoleLogLevel=None, acceptClientCerts=None, validateClientCertIdentity=None, excludeCsrfChecking=None,
        enableSSLv3=None, maxFiles=None, maxFileSize=None, enabledTLS=None, sshdPort=None, sessionCachePurge=None,
        sessionInactivityTimeout=None, sshdClientAliveInterval=None, swapFileSize=None, httpProxy=None,
        enabledServerProtocols=None, loginHeader=None, loginMessage=None, pendingChangesLifetime=None,
        baSessionTimeout=None, httpsProxy=None, accessLogFormat=None, lmiMessageTimeout=None, validVerifyDomains=None,
        check_mode=False, force=False):
    """
    Updating the administrator settings
    """
    warnings = []
    if force is False:
        update_required, warnings, json_data = _check(isamAppliance, oldPassword, newPassword, minHeapSize, maxHeapSize,
                                                      sessionTimeout, httpPort, httpsPort, minThreads, maxThreads,
                                                      maxPoolSize, lmiDebuggingEnabled, consoleLogLevel,
                                                      acceptClientCerts, validateClientCertIdentity,
                                                      excludeCsrfChecking, enableSSLv3, maxFiles, maxFileSize,
                                                      enabledTLS, sshdPort, sessionCachePurge, sessionInactivityTimeout,
                                                      sshdClientAliveInterval, swapFileSize, httpProxy,
                                                      enabledServerProtocols, loginHeader, loginMessage, pendingChangesLifetime,
                                                      baSessionTimeout, httpsProxy, accessLogFormat,
                                                      lmiMessageTimeout, validVerifyDomains,
                                                      warnings)

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_put(
                "Updating the administrator settings",
                "/core/admin_cfg", json_data, warnings=warnings)

    return isamAppliance.create_return_object(changed=False, warnings=warnings)


def _check(isamAppliance, oldPassword, newPassword, minHeapSize, maxHeapSize,
           sessionTimeout, httpPort, httpsPort, minThreads, maxThreads,
           maxPoolSize, lmiDebuggingEnabled, consoleLogLevel,
           acceptClientCerts, validateClientCertIdentity,
           excludeCsrfChecking, enableSSLv3, maxFiles, maxFileSize,
           enabledTLS, sshdPort, sessionCachePurge, sessionInactivityTimeout,
           sshdClientAliveInterval, swapFileSize, httpProxy,
           enabledServerProtocols, loginHeader, loginMessage, pendingChangesLifetime,
           baSessionTimeout, httpsProxy, accessLogFormat,
           lmiMessageTimeout, validVerifyDomains,
           warnings):
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
    if ibmsecurity.utilities.tools.version_compare(isamAppliance.facts["version"], "9.0.1.0") < 0:
        if minHeapSize is not None or maxHeapSize is not None or httpPort is not None or httpsPort is not None or \
                minThreads is not None or maxThreads is not None or maxPoolSize is not None or \
                lmiDebuggingEnabled is not None or consoleLogLevel is not None or \
                acceptClientCerts is not None or validateClientCertIdentity is not None or \
                excludeCsrfChecking is not None or enableSSLv3 is not None or maxFiles is not None or \
                maxFileSize is not None or enabledTLS is not None or sshdPort is not None or \
                enabledServerProtocols is not None:
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
            json_data["consoleLogLevel"] = consoleLogLevel
            if 'consoleLogLevel' in ret_obj['data'] and ret_obj['data']['consoleLogLevel'] == 'OFF':
                ret_obj['data']['consoleLogLevel'] = 'OFF'
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
            if ibmsecurity.utilities.tools.version_compare(isamAppliance.facts["version"], "10.0.3.0") >= 0:
                warnings.append(
                    "Appliance at version: {0}, enableSSLv3: {1} is not supported. Needs max. 10.0.2.0. Ignoring for this call.".format(
                        isamAppliance.facts["version"], enableSSLv3))
            else:
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
        if sshdPort is not None:
            if ibmsecurity.utilities.tools.version_compare(isamAppliance.facts["version"], "9.0.3.0") < 0:
                warnings.append(
                    "Appliance at version: {0}, sshdPort: {1} is not supported. Needs 9.0.3.0 or higher. Ignoring sshdPort for this call.".format(
                        isamAppliance.facts["version"], sshdPort))
            else:
                json_data["sshdPort"] = int(sshdPort)
        elif 'sshdPort' in ret_obj['data']:
            del ret_obj['data']['sshdPort']
        if enabledTLS is not None:
            if ibmsecurity.utilities.tools.version_compare(isamAppliance.facts["version"], "9.0.4.0") < 0:
                warnings.append(
                    "Appliance at version: {0}, enabledTLS: {1} is not supported. Needs 9.0.4.0 or higher. Ignoring enabledTLS for this call.".format(
                        isamAppliance.facts["version"], enabledTLS))
            else:
                json_data["enabledTLS"] = enabledTLS
        elif 'enabledTLS' in ret_obj['data']:
            del ret_obj['data']['enabledTLS']
        if sessionCachePurge is not None:
            if ibmsecurity.utilities.tools.version_compare(isamAppliance.facts["version"], "9.0.5.0") < 0:
                warnings.append(
                    "Appliance at version: {0}, sessionCachePurge: {1} is not supported. Needs 9.0.5.0 or higher. Ignoring sessionCachePurge for this call.".format(
                        isamAppliance.facts["version"], sessionCachePurge))
            else:
                json_data["sessionCachePurge"] = int(sessionCachePurge)
        elif 'sessionCachePurge' in ret_obj['data']:
            del ret_obj['data']['sessionCachePurge']
        if sessionInactivityTimeout is not None:
            if ibmsecurity.utilities.tools.version_compare(isamAppliance.facts["version"], "9.0.5.0") < 0:
                warnings.append(
                    "Appliance at version: {0}, sessionInactivityTimeout: {1} is not supported. Needs 9.0.5.0 or higher. Ignoring sessionInactivityTimeout for this call.".format(
                        isamAppliance.facts["version"], sessionInactivityTimeout))
            else:
                json_data["sessionInactivityTimeout"] = int(sessionInactivityTimeout)
        elif 'sessionInactivityTimeout' in ret_obj['data']:
            del ret_obj['data']['sessionInactivityTimeout']
        if sshdClientAliveInterval is not None:
            if ibmsecurity.utilities.tools.version_compare(isamAppliance.facts["version"], "9.0.5.0") < 0:
                warnings.append(
                    "Appliance at version: {0}, sshdClientAliveInterval: {1} is not supported. Needs 9.0.5.0 or higher. Ignoring sshdClientAliveInterval for this call.".format(
                        isamAppliance.facts["version"], sshdClientAliveInterval))
            else:
                json_data["sshdClientAliveInterval"] = int(sshdClientAliveInterval)
        elif 'sshdClientAliveInterval' in ret_obj['data']:
            del ret_obj['data']['sshdClientAliveInterval']
        if swapFileSize is not None:
            if ibmsecurity.utilities.tools.version_compare(isamAppliance.facts["version"], "9.0.5.0") < 0:
                warnings.append(
                    "Appliance at version: {0}, swapFileSize: {1} is not supported. Needs 9.0.5.0 or higher. Ignoring swapFileSize for this call.".format(
                        isamAppliance.facts["version"], swapFileSize))
            else:
                json_data["swapFileSize"] = swapFileSize
        elif 'swapFileSize' in ret_obj['data']:
            del ret_obj['data']['swapFileSize']
        if httpProxy is not None:
            if ibmsecurity.utilities.tools.version_compare(isamAppliance.facts["version"], "9.0.5.0") < 0:
                warnings.append(
                    "Appliance at version: {0}, httpProxy: {1} is not supported. Needs 9.0.5.0 or higher. Ignoring httpProxy for this call.".format(
                        isamAppliance.facts["version"], httpProxy))
            else:
                json_data["httpProxy"] = httpProxy
        elif 'httpProxy' in ret_obj['data']:
            del ret_obj['data']['httpProxy']
        if enabledServerProtocols is not None:
            if ibmsecurity.utilities.tools.version_compare(isamAppliance.facts["version"], "9.0.7.0") < 0:
                warnings.append(
                    "Appliance at version: {0}, enabledServerProtocols: {1} is not supported. Needs 9.0.7.0 or higher. Ignoring enabledServerProtocols for this call.".format(
                        isamAppliance.facts["version"], enabledServerProtocols))
            else:
                json_data["enabledServerProtocols"] = enabledServerProtocols
        elif 'enabledServerProtocols' in ret_obj['data']:
            del ret_obj['data']['enabledServerProtocols']
        if loginHeader is not None:
            if ibmsecurity.utilities.tools.version_compare(isamAppliance.facts["version"], "9.0.7.0") < 0:
                warnings.append(
                    "Appliance at version: {0}, loginHeader: {1} is not supported. Needs 9.0.7.0 or higher. Ignoring loginHeader for this call.".format(
                        isamAppliance.facts["version"], loginHeader))
            else:
                json_data["loginHeader"] = loginHeader
        elif 'loginHeader' in ret_obj['data']:
            del ret_obj['data']['loginHeader']
        if loginMessage is not None:
            if ibmsecurity.utilities.tools.version_compare(isamAppliance.facts["version"], "9.0.7.0") < 0:
                warnings.append(
                    "Appliance at version: {0}, loginMessage: {1} is not supported. Needs 9.0.7.0 or higher. Ignoring loginMessage for this call.".format(
                        isamAppliance.facts["version"], loginMessage))
            else:
                json_data["loginMessage"] = loginMessage
        elif 'loginMessage' in ret_obj['data']:
            del ret_obj['data']['loginMessage']
        if pendingChangesLifetime is not None:
            if ibmsecurity.utilities.tools.version_compare(isamAppliance.facts["version"], "9.0.7.0") < 0:
                warnings.append(
                    "Appliance at version: {0}, pendingChangesLifetime: {1} is not supported. Needs 9.0.7.0 or higher. Ignoring pendingChangesLifetime for this call.".format(
                        isamAppliance.facts["version"], pendingChangesLifetime))
            else:
                json_data["pendingChangesLifetime"] = pendingChangesLifetime
        elif 'pendingChangesLifetime' in ret_obj['data']:
            del ret_obj['data']['pendingChangesLifetime']
        if httpsProxy is not None:
            if ibmsecurity.utilities.tools.version_compare(isamAppliance.facts["version"], "9.0.7.0") < 0:
                warnings.append("Appliance at version: {0}, httpsProxy: {1} is not supported. Needs 9.0.7.0 or higher. Ignoring for this call.".format(
                    isamAppliance.facts["version"], httpsProxy))
            else:
                json_data["httpsProxy"] = httpsProxy
        elif 'httpsProxy' in ret_obj['data']:
            del ret_obj['data']['httpsProxy']
        #10.0.2 or something.  Also, when Python 3?
        # baSessionTimeout, httpsProxy, accessLogFormat, lmiMessageTimeout, validVerifyDomains,
        if baSessionTimeout is not None:
            if ibmsecurity.utilities.tools.version_compare(isamAppliance.facts["version"], "10.0.2.0") < 0:
                warnings.append("Appliance at version: {0}, baSessionTimeout: {1} is not supported. Needs 10.0.2.0 or higher. Ignoring for this call.".format(
                    isamAppliance.facts["version"], baSessionTimeout))
            else:
                json_data["baSessionTimeout"] = int(baSessionTimeout)
        elif 'baSessionTimeout' in ret_obj['data']:
            del ret_obj['data']['baSessionTimeout']
        if accessLogFormat is not None:
            if ibmsecurity.utilities.tools.version_compare(isamAppliance.facts["version"], "10.0.0.0") < 0:
                warnings.append("Appliance at version: {0}, accessLogFormat: {1} is not supported. Needs 10.0.0.0 or higher. Ignoring for this call.".format(
                    isamAppliance.facts["version"], accessLogFormat))
            else:
                json_data["accessLogFormat"] = accessLogFormat
        elif 'accessLogFormat' in ret_obj['data']:
            del ret_obj['data']['accessLogFormat']
        if lmiMessageTimeout is not None:
            if ibmsecurity.utilities.tools.version_compare(isamAppliance.facts["version"], "10.0.2.0") < 0:
                warnings.append("Appliance at version: {0}, lmiMessageTimeout: {1} is not supported. Needs 10.0.2.0 or higher. Ignoring for this call.".format(
                    isamAppliance.facts["version"], lmiMessageTimeout))
            else:
                json_data["lmiMessageTimeout"] = int(lmiMessageTimeout)
        elif 'lmiMessageTimeout' in ret_obj['data']:
            del ret_obj['data']['lmiMessageTimeout']
        if validVerifyDomains is not None:
            if ibmsecurity.utilities.tools.version_compare(isamAppliance.facts["version"], "10.0.2.0") < 0:
                warnings.append("Appliance at version: {0}, validVerifyDomains: {1} is not supported. Needs 10.0.2.0 or higher. Ignoring for this call.".format(
                    isamAppliance.facts["version"], validVerifyDomains))
            else:
                json_data["validVerifyDomains"] = validVerifyDomains
        elif 'validVerifyDomains' in ret_obj['data']:
            del ret_obj['data']['validVerifyDomains']
    sorted_ret_obj = json.dumps(ret_obj['data'], skipkeys=True, sort_keys=True)
    sorted_json_data = json.dumps(json_data, skipkeys=True, sort_keys=True)
    logger.debug("Sorted Existing Data:{0}".format(sorted_ret_obj))
    logger.debug("Sorted Desired  Data:{0}".format(sorted_json_data))
    if sorted_ret_obj != sorted_json_data:
        logger.debug("Admin Settings are found to be different. See above JSON for difference.")
        # Ensure users know how REST API handles httpsPort default value
        if httpsPort is None and ibmsecurity.utilities.tools.version_compare(isamAppliance.facts["version"],
                                                                             "9.0.1.0") >= 0:
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
