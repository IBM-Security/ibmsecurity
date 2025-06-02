import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/lmi_auth"


def get(isvgAppliance, check_mode=False, force=False):
    """
    Retrieve LMI authentication configuration
    """
    return isvgAppliance.invoke_get("Retrieve LMI authentication configuration entries", "{0}".format(uri))


def search(isvgAppliance, name="LMI Authentication Registry", check_mode=False, force=False):
    """
    Search for existing LMI authentication configuration.
    """
    ret_obj = get(isvgAppliance)
    return_obj = isvgAppliance.create_return_object()

    for obj in ret_obj['data']:
        if 'name' in obj and obj['name'] == name:
            logger.info("Found lmi auth entry: {0}".format(obj['name']))
            return_obj['data'] = obj
            return_obj['rc'] = 0

    return return_obj


def add(isvgAppliance, hostName, port, dnLocation, userFilter, groupFilter, bindDN, bindPwd, useSSL, check_mode=False, force=False):
    """
    Updating LMI authentication configuration
    """
    if force is True:
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True)
        else:
            return isvgAppliance.invoke_post(
                "Configure LMI authentication", "{0}".format(uri),
                    {
                      "hostName": hostName,
                      "port": port,
                      "dnLocation": dnLocation,
                      "userFilter": userFilter,
                      "groupFilter": groupFilter,
                      "bindDN": bindDN,
                      "bindPwd": bindPwd,
                      "useSSL": useSSL,
                      "name":"LMI Authentication Registry",
                      "_isNew": True,
                      "action": "configure"
                    })

    return isvgAppliance.create_return_object(changed=False)


def delete(isvgAppliance, name="LMI Authentication Registry", check_mode=False, force=False):
    """
    Un-configure LMI authentication configuration
    """
    ret_obj = search(isvgAppliance, name)
    warnings = ret_obj["warnings"]

    if force is True or ret_obj['data'] != {}:
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            ret_obj['data'] = ret_obj['data']
            uuid = ret_obj['data']['uuid']
            return isvgAppliance.invoke_delete(
                "Un-configure LMI authentication", "{0}/{1}".format(uri, uuid), warnings=warnings)

    return isvgAppliance.create_return_object(warnings=warnings)


def update(isvgAppliance, hostName, port, dnLocation, userFilter, groupFilter, bindDN, bindPwd, useSSL, check_mode=False, force=False):
    """
    Updating LMI authentication configuration
    """
    ret_obj = get(isvgAppliance)
    warnings = ret_obj["warnings"]

    # JSON payload of interest is at first (and only) position of array
    ret_obj['data'] = ret_obj['data'][0]

    uuid = ret_obj['data']['uuid']

    needs_update = False

    # Create a simple json with just the attributes
    json_data = {
        "name": "LMI Authentication Registry",
        "uuid": uuid
    }

    if 'lastModified' in ret_obj['data']:
        del ret_obj['data']['lastModified']

    # mandatory attributes
    if hostName is not None:
        json_data['hostName'] = hostName
    elif 'hostName' in ret_obj['data']:
        if ret_obj['data']['hostName'] is not None:
            json_data['hostName'] = ret_obj['data']['hostName']
        else:
            del ret_obj['data']['hostName']
    if port is not None:
        json_data['port'] = port
    elif 'port' in ret_obj['data']:
        if ret_obj['data']['port'] is not None:
            json_data['port'] = ret_obj['data']['port']
        else:
            del ret_obj['data']['port']
    if dnLocation is not None:
        json_data['dnLocation'] = dnLocation
    elif 'dnLocation' in ret_obj['data']:
        if ret_obj['data']['dnLocation'] is not None:
            json_data['dnLocation'] = ret_obj['data']['dnLocation']
        else:
            del ret_obj['data']['dnLocation']
    if userFilter is not None:
        json_data['userFilter'] = userFilter
    elif 'userFilter' in ret_obj['data']:
        if ret_obj['data']['userFilter'] is not None:
            json_data['userFilter'] = ret_obj['data']['userFilter']
        else:
            del ret_obj['data']['userFilter']
    if groupFilter is not None:
        json_data['groupFilter'] = groupFilter
    elif 'groupFilter' in ret_obj['data']:
        if ret_obj['data']['groupFilter'] is not None:
            json_data['groupFilter'] = ret_obj['data']['groupFilter']
        else:
            del ret_obj['data']['groupFilter']
    if useSSL is not None:
        json_data['useSSL'] = useSSL
    elif 'useSSL' in ret_obj['data']:
        if ret_obj['data']['useSSL'] is not None:
            json_data['useSSL'] = ret_obj['data']['useSSL']
        else:
            del ret_obj['data']['useSSL']
    # optional attributes
    if bindDN is not None:
        json_data['bindDN'] = bindDN
    elif 'bindDN' in ret_obj['data']:
        if ret_obj['data']['bindDN'] is not None:
            json_data['bindDN'] = ret_obj['data']['bindDN']
        else:
            del ret_obj['data']['bindDN']
    if bindPwd is not None:
        json_data['bindPwd'] = bindPwd
    elif 'bindPwd' in ret_obj['data']:
        if ret_obj['data']['bindPwd'] is not None:
            json_data['bindPwd'] = ret_obj['data']['bindPwd']
        else:
            del ret_obj['data']['bindPwd']

    sorted_ret_obj = tools.json_sort(ret_obj['data'])
    sorted_json_data = tools.json_sort(json_data)
    logger.debug("Sorted Existing Data:{0}".format(sorted_ret_obj))
    logger.debug("Sorted Desired  Data:{0}".format(sorted_json_data))
    if sorted_ret_obj != sorted_json_data:
        json_data['_isNew'] = False
        json_data['action'] = "reconfigure"
        needs_update = True

    if force is True or needs_update is True:
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True)
        else:
            return isvgAppliance.invoke_put(
                "Update LMI authentication", "{0}/{1}".format(uri, uuid),
                json_data, warnings=warnings)

    return isvgAppliance.create_return_object(changed=False)


def set(isvgAppliance, hostName, port, dnLocation, userFilter, groupFilter, bindDN=None, bindPwd=None, useSSL=False, check_mode=False, force=False):
    """
    Creating or Modifying the LMI authentication configuration
    """
    name = "LMI Authentication Registry"
    if (search(isvgAppliance, name))['data'] == {}:
        # Force the add - we already know property does not exist
        logger.info("LMI auth entry {0} had no match, requesting to configure.".format(name))
        return add(isvgAppliance, hostName, port, dnLocation, userFilter, groupFilter, bindDN, bindPwd, useSSL, check_mode=check_mode, force=True)
    else:
        # Update request
        logger.info("LMI auth entry {0} exists, requesting to reconfigure.".format(name))
        return update(isvgAppliance, hostName, port, dnLocation, userFilter, groupFilter, bindDN, bindPwd, useSSL, check_mode=check_mode, force=force)
