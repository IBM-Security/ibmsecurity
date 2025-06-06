import logging
import ibmsecurity.utilities.tools as _tools
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
            if _tools.version_compare(isamAppliance.facts['version'], "9.0.1.0") < 0:
                warnings.append(
                    "Appliance at version: {0}, httpsPort not supported. Needs 9.0.1.0 or higher. Ignoring httpsPort for this call.")
            else:
                json_data['httpsPort'] = httpsPort
        else:
            if _tools.version_compare(isamAppliance.facts['version'], "9.0.1.0") < 0:
                pass  # Can safely ignore httpsPort
            else:
                warnings.append("Default httpsPort of 443 will be set on the appliance.")
        return isamAppliance.invoke_put("Setting admin password", "/core/admin_cfg", json_data, warnings=warnings)


def set(isamAppliance,
        oldPassword=None,
        newPassword=None,
        minHeapSize=None,
        maxHeapSize=None,
        sessionTimeout=30,
        sessionInactivityTimeout=None,
        sessionCachePurge=None,
        baSessionTimeout=None,
        httpPort=None,
        httpsPort=None,
        sshdPort=None,
        sshdClientAliveInterval=None,
        sshdPasswordAuthentication=None,
        swapFileSize=None,
        minThreads=None,
        maxThreads=None,
        maxPoolSize=None,
        lmiDebuggingEnabled=None,
        consoleLogLevel=None,
        acceptClientCerts=None,
        validateClientCertIdentity=None,
        excludeCsrfChecking=None,
        enabledServerProtocols=None,
        enabledTLS=None,
        enableSSLv3=None,
        maxFiles=None,
        maxFileSize=None,
        httpProxy=None,
        httpsProxy=None,
        loginHeader=None,
        loginMessage=None,
        pendingChangesLifetime=None,
        accessLogFormat=None,
        lmiMessageTimeout=None,
        validVerifyDomains=None,
        jsVersion=None,
        check_mode=False, force=False):
    """
    Updating the administrator settings
    """
    warnings = []

    update_required, warnings, json_data = _check(isamAppliance,
                                                  warnings=warnings,
                                                  oldPassword=oldPassword,
                                                  newPassword=newPassword,
                                                  minHeapSize=minHeapSize,
                                                  maxHeapSize=maxHeapSize,
                                                  sessionTimeout=sessionTimeout,
                                                  sessionInactivityTimeout=sessionInactivityTimeout,
                                                  sessionCachePurge=sessionCachePurge,
                                                  baSessionTimeout=baSessionTimeout,
                                                  httpPort=httpPort,
                                                  httpsPort=httpsPort,
                                                  sshdPort=sshdPort,
                                                  sshdClientAliveInterval=sshdClientAliveInterval,
                                                  sshdPasswordAuthentication=sshdPasswordAuthentication,
                                                  swapFileSize=swapFileSize,
                                                  minThreads=minThreads,
                                                  maxThreads=maxThreads,
                                                  maxPoolSize=maxPoolSize,
                                                  lmiDebuggingEnabled=lmiDebuggingEnabled,
                                                  consoleLogLevel=consoleLogLevel,
                                                  acceptClientCerts=acceptClientCerts,
                                                  validateClientCertIdentity=validateClientCertIdentity,
                                                  excludeCsrfChecking=excludeCsrfChecking,
                                                  enabledServerProtocols=enabledServerProtocols,
                                                  enabledTLS=enabledTLS,
                                                  enableSSLv3=enableSSLv3,
                                                  maxFiles=maxFiles,
                                                  maxFileSize=maxFileSize,
                                                  httpProxy=httpProxy,
                                                  httpsProxy=httpsProxy,
                                                  loginHeader=loginHeader,
                                                  loginMessage=loginMessage,
                                                  pendingChangesLifetime=pendingChangesLifetime,
                                                  accessLogFormat=accessLogFormat,
                                                  lmiMessageTimeout=lmiMessageTimeout,
                                                  validVerifyDomains=validVerifyDomains,
                                                  jsVersion=jsVersion
                                                  )

    if force or update_required:
        if check_mode:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_put(
                "Updating the administrator settings",
                "/core/admin_cfg", json_data, warnings=warnings)

    return isamAppliance.create_return_object(changed=False, warnings=warnings)


def _check(isamAppliance,
           warnings=[],
           **kwargs
           ):
    """
    Check whether target key has already been set with the value
    :param isamAppliance:
    :param key:
    :param value:
    :return: True/False
    """
    ret_obj = get(isamAppliance)

    json_data = {}
    for k, v in kwargs.items():
        iviaVersion = isamAppliance.facts['version']
        if v is None:
            # Skip None inputs
            continue
        if k == "force":
            # force = v
            continue
        if k == "check_mode":
            # check_mode = v
            continue
        if k not in ret_obj['data']:
            # add as empty string, if it's not there. I know this is true for jsVersion, and probably also for other stuff
            ret_obj['data'][k] = ""
        if k == "newPassword":
            json_data["confirmPassword"] = v
        if k in ["minHeapSize", "maxHeapSize", "httpPort", "httpsPort", "minThreads", "maxThreads", "maxPoolSize", "maxFiles", "maxFileSize", "sshdPort", "sessionCachePurge", "sessionInactivityTimeout", "sshdClientAliveInterval", "baSessionTimeout"]:
            # int values
            if k == "sshdPort" and _tools.version_compare(iviaVersion, "9.0.3.0") < 0:
                warnings.append(f"Appliance at version: {iviaVersion}, sshdPort: {v} is not supported. Needs 9.0.3.0 or higher. Ignoring sshdPort for this call.")
                continue
            if k in ["sessionCachePurge", "sessionInactivityTimeout", "sshdClientAliveInterval"] and _tools.version_compare(iviaVersion, "9.0.5.0") < 0:
                warnings.append(f"Appliance at version: {iviaVersion}, {k}: {v} is not supported. Needs 9.0.5.0 or higher. Ignoring.")
                continue
            if k in ["baSessionTimeout"] and _tools.version_compare(iviaVersion, "10.0.2.0") < 0:
                warnings.append(
                    f"Appliance at version: {iviaVersion}, {k}: {v} is not supported. Needs 10.0.2.0 or higher. Ignoring.")
                continue
            json_data[k] = int(v)
            continue
        if k == "enableSSLv3":
            if _tools.version_compare(iviaVersion, "10.0.3.0") >= 0:
                warnings.append(f"Appliance at version: {iviaVersion}, enableSSLv3: {v} is not supported. Needs max. 10.0.2.0. Ignoring for this call.")
                continue
        if k == "consoleLogLevel":
            if 'consoleLogLevel' in ret_obj['data'] and ret_obj['data']['consoleLogLevel'] == 'OFF':
                ret_obj['data']['consoleLogLevel'] = 'OFF'
        if k == "enabledTLS":
            if _tools.version_compare(iviaVersion, "9.0.4.0") < 0:
                warnings.append(f"Appliance at version: {iviaVersion}, enabledTLS: {v} is not supported. Needs 9.0.4.0 or higher. Ignoring enabledTLS for this call.")
                continue
        if k in ["swapFileSize", "httpProxy"]:
            if _tools.version_compare(iviaVersion, "9.0.5.0") < 0:
                warnings.append(f"Appliance at version: {iviaVersion}, {k}: {v} is not supported. Needs 9.0.5.0 or higher. Ignoring.")
                continue
        if k in ["enabledServerProtocols", "loginHeader", "loginMessage", "pendingChangesLifetime", "httpsProxy"]:
            if _tools.version_compare(iviaVersion, "9.0.7.0") < 0:
                warnings.append(
                    f"Appliance at version: {iviaVersion}, {k}: {v} is not supported. Needs 9.0.7.0 or higher. Ignoring.")
                continue
        if k in ["accessLogFormat"]:
            if _tools.version_compare(iviaVersion, "10.0.0.0") < 0:
                warnings.append(f"Appliance at version: {iviaVersion}, {k}: {v} is not supported. Needs 10.0.0.0 or higher. Ignoring.")
                continue
        if k in ["lmiMessageTimeout", "validVerifyDomains"]:
            if _tools.version_compare(iviaVersion, "10.0.2.0") < 0:
                warnings.append(f"Appliance at version: {iviaVersion}, {k}: {v} is not supported. Needs 10.0.0.0 or higher. Ignoring.")
                continue
        if k == "jsVersion":
            if _tools.version_compare(iviaVersion, "10.0.9.0") < 0:
                warnings.append(f"Appliance at version: {iviaVersion}, {k}: {v} is not supported. Needs 10.0.9.0 or higher. Ignoring.")
                continue

        # Add to the json_data dict
        json_data[k] = v

    if not _tools.json_equals(ret_obj, json_data):
        logger.debug("Admin Settings are found to be different. See above JSON for difference.")
        return True, warnings, json_data
    else:  # No changes required
        return False, warnings, json_data


def compare(isamAppliance1, isamAppliance2):
    """
    Compare advanced tuning parameters between two appliances
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    return _tools.json_compare(ret_obj1, ret_obj2)
