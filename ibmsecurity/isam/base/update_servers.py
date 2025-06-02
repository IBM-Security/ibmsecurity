import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/core/update_servers"
requires_modules = None
requires_version = None


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Get all Update Servers
    """
    return isamAppliance.invoke_get("Get Update Servers", uri, requires_modules=requires_modules,
                                    requires_version=requires_version)


def get(isamAppliance, name, check_mode=False, force=False):
    """
    Retrieve a specific update server
    """
    ret_obj = search(isamAppliance, name=name, check_mode=check_mode, force=force)
    us_id = ret_obj['data']

    if us_id == {}:
        logger.info(f"Update Server {name} had no match, skipping retrieval.")
        return isamAppliance.create_return_object()
    else:
        return _get(isamAppliance, us_id)


def _get(isamAppliance, us_id):
    return isamAppliance.invoke_get("Retrieve a specific update server",
                                    f"{uri}/{us_id}")


def search(isamAppliance, name, force=False, check_mode=False):
    """
    Search update server by name
    """
    ret_obj = get_all(isamAppliance)
    return_obj = isamAppliance.create_return_object()

    for obj in ret_obj['data']['luServers']:
        if obj['name'] == name:
            logger.info(f"Found Update Server {name} id: {obj['uuid']}")
            return_obj['data'] = obj['uuid']
            return_obj['rc'] = 0

    return return_obj


def set(isamAppliance, priority, name, enabled, hostName, port, trustLevel, useProxy=False, useProxyAuth=False,
        cert=None, proxyHost=None, proxyPort=None, proxyUser=None, proxyPwd=None, new_name=None, check_mode=False,
        force=False):
    """
    Creating or Modifying a update server
    """
    if (search(isamAppliance, name=name))['data'] == {}:
        # Force the add - we already know update server does not exist
        logger.info(f"Update Server {name} had no match, requesting to add new one.")
        return add(isamAppliance, priority, name, enabled, hostName, port, trustLevel, useProxy,
                   useProxyAuth, cert, proxyHost, proxyPort, proxyUser, proxyPwd, check_mode, True)
    else:
        # Update request
        logger.info(f"Update Server {name} exists, requesting to update.")
        return update(isamAppliance, priority, name, enabled, hostName, port, trustLevel, useProxy, useProxyAuth, cert,
                      proxyHost, proxyPort, proxyUser, proxyPwd, new_name, check_mode, force)


def add(isamAppliance, priority, name, enabled, hostName, port, trustLevel, useProxy=False, useProxyAuth=False, cert="",
        proxyHost=None, proxyPort=None, proxyUser=None, proxyPwd=None, check_mode=False, force=False):
    """
    Add a Update Server
    """
    if force is True or search(isamAppliance, name=name) == {}:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            json_data = {"priority": priority,
                         "name": name,
                         "enabled": enabled,
                         "hostName": hostName,
                         "port": port,
                         "trustLevel": trustLevel,
                         "useProxy": useProxy,
                         "useProxyAuth": useProxyAuth,
                         "_isNew": True,
                         "cert": cert,
                         "proxyHost": proxyHost,
                         "proxyPort": proxyPort,
                         "proxyUser": proxyUser,
                         "proxyPwd": proxyPwd}

            return isamAppliance.invoke_post("Add a Update Server", uri, json_data, requires_modules=requires_modules,
                                             requires_version=requires_version)

    return isamAppliance.create_return_object()


def update(isamAppliance, priority, name, enabled, hostName, port, trustLevel, useProxy=False, useProxyAuth=False,
           cert="", proxyHost=None, proxyPort=None, proxyUser=None, proxyPwd=None, new_name=None, check_mode=False,
           force=False):
    """
    Update an update server's details.
    """
    us_id, update_required, json_data = _check(isamAppliance, priority, name, enabled, hostName, port, trustLevel,
                                               useProxy, useProxyAuth, cert, proxyHost, proxyPort, proxyUser, proxyPwd,
                                               new_name)

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put("Update an update server", f"{uri}/{us_id}", json_data,
                                            requires_modules=requires_modules,
                                            requires_version=requires_version)

    return isamAppliance.create_return_object()


def _check(isamAppliance, priority, name, enabled, hostName, port, trustLevel, useProxy, useProxyAuth,
           cert, proxyHost, proxyPort, proxyUser, proxyPwd, new_name):
    update_required = False
    json_data = {"priority": priority,
                 "name": name,
                 "enabled": enabled,
                 "hostName": hostName,
                 "port": port,
                 "trustLevel": trustLevel,
                 "useProxy": useProxy,
                 "useProxyAuth": useProxyAuth,
                 "cert": cert,
                 "proxyHost": proxyHost,
                 "proxyPort": proxyPort,
                 "proxyUser": proxyUser,
                 "proxyPwd": proxyPwd}
    ret_obj = get(isamAppliance, name)
    if ret_obj['data'] == {}:
        logger.warning("Update Server not found, returning no update required.")
        return None, update_required, json_data
    else:
        us_id = ret_obj['data']['uuid']
        if new_name is not None:
            json_data['name'] = new_name
        else:
            json_data['name'] = name
        del ret_obj['data']['uuid']
        sorted_json_data = ibmsecurity.utilities.tools.json_sort(json_data)
        logger.debug(f"Sorted input: {sorted_json_data}")
        sorted_ret_obj = ibmsecurity.utilities.tools.json_sort(ret_obj['data'])
        logger.debug(f"Sorted existing data: {sorted_ret_obj}")
        if sorted_ret_obj != sorted_json_data:
            logger.info("Changes detected, update needed.")
            update_required = True

    return us_id, update_required, json_data


def enable(isamAppliance, name, enabled, check_mode=False, force=False):
    """
    Update an update server's details.
    """
    warnings = []
    ret_obj = get(isamAppliance=isamAppliance, name=name)

    if ret_obj['data'] == {}:
        warnings.append(f"Update Server {name} not found.")
    elif force is True or enabled != ret_obj['data']['enabled']:
        logger.debug("Enable flag needs to be updated!")
        return update(isamAppliance, priority=ret_obj['data']['priority'], name=name, enabled=enabled,
                      hostName=ret_obj['data']['hostName'], port=ret_obj['data']['port'],
                      trustLevel=ret_obj['data']['trustLevel'], useProxy=ret_obj['data']['useProxy'],
                      useProxyAuth=ret_obj['data']['useProxyAuth'], cert=ret_obj['data']['cert'],
                      proxyHost=ret_obj['data']['proxyHost'], proxyPort=ret_obj['data']['proxyPort'],
                      proxyUser=ret_obj['data']['proxyUser'], proxyPwd=ret_obj['data']['proxyPwd'],
                      check_mode=check_mode,
                      force=True)

    return isamAppliance.create_return_object(warnings=warnings)


def delete(isamAppliance, name, check_mode=False, force=False):
    """
    Delete an Update Server
    """
    ret_obj = search(isamAppliance, name=name)

    if ret_obj['data'] != {}:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete("Delete an Update Server", f"{uri}/{ret_obj['data']}")
    else:
        logger.info(f"Update Server: {name} not found, delete skipped.")

    return isamAppliance.create_return_object()


def compare(isamAppliance1, isamAppliance2):
    """
    Compare Update Servers between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    for obj in ret_obj1['data']:
        del obj['uuid']
    for obj in ret_obj2['data']:
        del obj['uuid']

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['uuid'])
