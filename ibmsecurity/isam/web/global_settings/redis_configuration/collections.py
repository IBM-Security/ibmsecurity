import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

uri = "/wga/redis_config/collections"
requires_modules = ["wga"]
requires_version = "10.0.1"


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieve the list of configured Redis collections
    """
    return isamAppliance.invoke_get("Retrieve the list of configured Redis collections",
                                    "{0}".format(uri),
                                    requires_modules=requires_modules, requires_version=requires_version)


def get(isamAppliance, name, check_mode=False, force=False):
    """
    Retrieve the list of configured Redis collections
    """
    return isamAppliance.invoke_get("Retrieve the list of configured Redis collections",
                                    "{0}/{1}".format(uri, name),
                                    requires_modules=requires_modules, requires_version=requires_version)


def add(isamAppliance, name, max_pooled_connections=50, idle_timeout=10, connect_timeout=5,
        io_timeout=30, health_check_interval=15, servers=[], cross_domain_support=None, matching_hosts=None,
        check_mode=False, force=False):
    """
    Create the configuration for a new collection of Redis servers
    """

    exist, warnings = _check_exist(isamAppliance, name)

    if force is True or exist is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            json_data = {
                "name": name,
                "max-pooled-connections": max_pooled_connections,
                "idle-timeout": idle_timeout,
                "connect-timeout": connect_timeout,
                "io-timeout": io_timeout,
                "health-check-interval": health_check_interval,
                "servers": servers
            }

            if matching_hosts != None:
                json_data['matching-hosts'] = matching_hosts

            if cross_domain_support != None:
                json_data['cross-domain-support'] = cross_domain_support

            return isamAppliance.invoke_post(
                "Create the configuration for a new collection of Redis servers",
                "{0}".format(uri),
                json_data,
                requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object(warnings=warnings)


def update(isamAppliance, name, max_pooled_connections=50, idle_timeout=10, connect_timeout=5,
           io_timeout=30, health_check_interval=15, servers=None, cross_domain_support=None, matching_hosts=None,
           check_mode=False, force=False):
    """
    Update the configuration of a collection of Redis servers
    """

    exist, warnings = _check_exist(isamAppliance, name)
    if exist is True:
        same_contents, warnings, json_data = _check_contents(isamAppliance=isamAppliance, name=name,
                                                             max_pooled_connections=max_pooled_connections,
                                                             idle_timeout=idle_timeout, connect_timeout=connect_timeout,
                                                             io_timeout=io_timeout,
                                                             health_check_interval=health_check_interval,
                                                             servers=servers, cross_domain_support=cross_domain_support,
                                                             matching_hosts=matching_hosts)
    else:
        return isamAppliance.create_return_object(warnings=warnings)

    if force is True or same_contents is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            if 'servers' not in json_data:
                json_data['servers'] = []
            return isamAppliance.invoke_put(
                "Update the configuration of a collection of Redis servers",
                "{0}/{1}".format(uri, name),
                json_data,
                requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object(warnings=warnings)


def set(isamAppliance, name, max_pooled_connections=50, idle_timeout=10, connect_timeout=5,
        io_timeout=30, health_check_interval=15, servers=None, cross_domain_support=None, matching_hosts=None,
        check_mode=False, force=False):
    exist, warnings = _check_exist(isamAppliance, name)
    if exist is True:
        return update(isamAppliance=isamAppliance, name=name, max_pooled_connections=max_pooled_connections,
                      idle_timeout=idle_timeout, connect_timeout=connect_timeout, io_timeout=io_timeout,
                      health_check_interval=health_check_interval, servers=servers,
                      cross_domain_support=cross_domain_support, matching_hosts=matching_hosts, check_mode=check_mode,
                      force=force)
    else:
        if servers is None:
            servers = []
        return add(isamAppliance=isamAppliance, name=name, max_pooled_connections=max_pooled_connections,
                   idle_timeout=idle_timeout, connect_timeout=connect_timeout, io_timeout=io_timeout,
                   health_check_interval=health_check_interval, servers=servers,
                   cross_domain_support=cross_domain_support, matching_hosts=matching_hosts, check_mode=check_mode,
                   force=force)


def delete(isamAppliance, name, check_mode=False, force=False):
    """
    Delete the configuration for a collection of Redis servers
    """
    exists, warnings = _check_exist(isamAppliance, name)

    if force is True or exists is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Delete the configuration for a collection of Redis servers",
                "{0}/{1}".format(uri, name),
                requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object(warnings=warnings)


def _check_exist(isamAppliance, name):
    ret_obj = get_all(isamAppliance)

    for obj in ret_obj['data']:
        if obj['name'] == name:
            return True, ret_obj['warnings']

    return False, ret_obj['warnings']


def _check_contents(isamAppliance, name, max_pooled_connections, idle_timeout, connect_timeout, io_timeout,
                    health_check_interval, servers, cross_domain_support, matching_hosts):
    ret_obj = get(isamAppliance, name)
    current_content = ret_obj['data']
    warnings = ret_obj['warnings']

    json_data = {
        'name': name,
        'max-pooled-connections': max_pooled_connections,
        'idle-timeout': idle_timeout,
        'connect-timeout': connect_timeout,
        'io-timeout': io_timeout,
        'health-check-interval': health_check_interval
    }
    if servers is not None:
        json_data['servers'] = servers

    if cross_domain_support is not None:
        json_data['cross-domain-support'] = cross_domain_support

    if matching_hosts is not None:
        json_data['matching-hosts'] = matching_hosts

    sorted_obj1 = tools.json_sort(json_data)
    logger.debug("Sorted sorted_obj1: {0}".format(sorted_obj1))
    sorted_obj2 = tools.json_sort(current_content)
    logger.debug("Sorted sorted_obj2: {0}".format(sorted_obj2))

    if sorted_obj1 != sorted_obj2:
        logger.info("Changes detected, update needed.")
        return False, warnings, json_data
    else:
        return True, warnings, json_data


def compare(isamAppliance1, isamAppliance2):
    """
    Compare redis configurations between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    return tools.json_compare(ret_obj1, ret_obj2)
