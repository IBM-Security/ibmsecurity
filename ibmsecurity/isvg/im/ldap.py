import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/ldap_object"


def get(isvgAppliance, check_mode=False, force=False):
    """
    Retrieve identity user registry configuration
    """
    return isvgAppliance.invoke_get("Retrieve identity user registry configuration entries", "{0}".format(uri))


def search(isvgAppliance, name, check_mode=False, force=False):
    """
    Search for existing identity user registry configuration.
    """
    ret_obj = get(isvgAppliance)
    return_obj = isvgAppliance.create_return_object()

    for obj in ret_obj['data']:
        if 'name' in obj and obj['name'] == name:
            logger.info("Found db entry: {0}".format(obj['name']))
            return_obj['data'] = obj
            return_obj['rc'] = 0

    return return_obj


def add(isvgAppliance, hostName, port, bindDN, bindPwd, orgName, shortOrgName, dnLocation, existingLDAP, useSSL, check_mode=False, force=False):
    """
    Updating identity user registry configuration
    """
    if force is True:
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True)
        else:
            if existingLDAP == ['true']:
                # Reconfiguration does not update the database schema. It configures only the Identity Manager database details.
                action = "reconfigure"
            else:
                # Configuration updates the database schema, in addition it configures the Identity Manager database details.
                action = "configure"

            return isvgAppliance.invoke_post(
                "Configure identity data store", "{0}".format(uri),
                    {
                      "name": "Identity User Registry",
                      "hostName": hostName,
                      "port": port,
                      "bindDN": bindDN,
                      "bindPwd": bindPwd,
                      "orgName": orgName,
                      "shortOrgName": shortOrgName,
                      "dnLocation": dnLocation,
                      "action": action,
                      "useSSL": useSSL,
                      "_isNew": True,
                      "existingLDAP": existingLDAP
                    })

    return isvgAppliance.create_return_object(changed=False)


def delete(isvgAppliance, name, check_mode=False, force=False):
    """
    Un-configure identity data store
    """
    ret_obj = search(isvgAppliance, name)
    warnings = ret_obj['warnings']

    if force is True or ret_obj['data'] != {}:
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            uuid = ret_obj['data']['uuid']
            return isvgAppliance.invoke_delete(
                "Un-configure identity data store", "{0}/{1}".format(uri, uuid), warnings=warnings)

    return isvgAppliance.create_return_object(warnings=warnings)


def update(isvgAppliance, hostName, port, bindDN, bindPwd, orgName, shortOrgName, dnLocation, existingLDAP, useSSL, check_mode=False, force=False):
    """
    Updating identity data store
    """
    ret_obj = get(isvgAppliance)
    warnings = ret_obj['warnings']

    # JSON payload of interest is at first (and only) position of array
    ret_obj['data'] = ret_obj['data'][0]

    uuid = ret_obj['data']['uuid']

    needs_update = False

    # Create a simple json with just the attributes
    json_data = {
        "name": "Identity User Registry",
        "uuid": uuid
    }

    if 'action' in ret_obj['data']:
        del ret_obj['data']['action']
    if 'lastmodified' in ret_obj['data']:
        del ret_obj['data']['lastmodified']
    if 'certCheckSum' in ret_obj['data']:
        del ret_obj['data']['certCheckSum']

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
    if orgName is not None:
        json_data['orgName'] = orgName
    elif 'orgName' in ret_obj['data']:
        if ret_obj['data']['orgName'] is not None:
            json_data['orgName'] = ret_obj['data']['orgName']
        else:
            del ret_obj['data']['orgName']
    if shortOrgName is not None:
        json_data['shortOrgName'] = shortOrgName
    elif 'shortOrgName' in ret_obj['data']:
        if ret_obj['data']['shortOrgName'] is not None:
            json_data['shortOrgName'] = ret_obj['data']['shortOrgName']
        else:
            del ret_obj['data']['shortOrgName']
    if dnLocation is not None:
        json_data['dnLocation'] = dnLocation
    elif 'dnLocation' in ret_obj['data']:
        if ret_obj['data']['dnLocation'] is not None:
            json_data['dnLocation'] = ret_obj['data']['dnLocation']
        else:
            del ret_obj['data']['dnLocation']
    if useSSL is not None:
        json_data['useSSL'] = useSSL
    elif 'useSSL' in ret_obj['data']:
        if ret_obj['data']['useSSL'] is not None:
            json_data['useSSL'] = ret_obj['data']['useSSL']
        else:
            del ret_obj['data']['useSSL']

    sorted_ret_obj = tools.json_sort(ret_obj['data'])
    sorted_json_data = tools.json_sort(json_data)
    logger.debug("Sorted Existing Data:{0}".format(sorted_ret_obj))
    logger.debug("Sorted Desired  Data:{0}".format(sorted_json_data))
    if sorted_ret_obj != sorted_json_data:
        json_data['_isNew'] = False
        json_data['action'] = "reconfigure"
        if existingLDAP is not None:
            json_data['existingLDAP'] = existingLDAP
        needs_update = True

    if force is True or needs_update is True:
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True)
        else:
            return isvgAppliance.invoke_put(
                "Update identity data store", "{0}/{1}".format(uri, uuid),
                json_data, warnings=warnings)

    return isvgAppliance.create_return_object(changed=False)


def set(isvgAppliance, hostName, port, bindDN, bindPwd, orgName, shortOrgName, dnLocation, existingLDAP, useSSL=False, check_mode=False, force=False):
    """
    Creating or Modifying a identity user registry configuration
    """
    name = "Identity User Registry"
    if (search(isvgAppliance, name))['data'] == {}:
        # Force the add - we already know object does not exist
        logger.info("Identity user registry {0} had no match, requesting to configure.".format(name))
        return add(isvgAppliance, hostName, port, bindDN, bindPwd, orgName, shortOrgName, dnLocation, existingLDAP, useSSL, check_mode=check_mode, force=True)
    else:
        # Update request
        logger.info("Identity user registry {0} exists, requesting to reconfigure.".format(name))
        return update(isvgAppliance, hostName, port, bindDN, bindPwd, orgName, shortOrgName, dnLocation, existingLDAP, useSSL, check_mode=check_mode, force=force)
