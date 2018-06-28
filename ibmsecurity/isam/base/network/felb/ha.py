import ibmsecurity.utilities.tools
import logging

logger = logging.getLogger(__name__)

module_uri = "/isam/felb/configuration/ha"
requires_module = None
requires_version = None


<<<<<<< HEAD
def disable(isamAppliance, check_mode=False, force=False):
=======
def delete(isamAppliance, check_mode=False, force=False):
>>>>>>> upstream/master
    """
    Disabling HA
    """
    if force is True or _check_disable(isamAppliance) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete("Disabling HA", "{0}".format(module_uri),
                                               requires_version=requires_version,
                                               requires_modules=requires_module)
    else:
        return isamAppliance.create_return_object()


<<<<<<< HEAD
def enable(isamAppliance, is_primary, interface, remote, port, health_check_interval,
           health_check_timeout, check_mode=False, force=False):
=======
def add(isamAppliance, is_primary, interface, remote, port, health_check_interval,
        health_check_timeout, check_mode=False, force=False):
>>>>>>> upstream/master
    """
    Enabling HA
    """
    if force is True or _check_enable(isamAppliance, is_primary, interface, remote, port, health_check_interval,
                                      health_check_timeout) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post("Enabling HA", "{0}".format(module_uri),
                                             {
                                                 "is_primary": is_primary,
                                                 "interface": interface,
                                                 "remote": remote,
                                                 "port": port,
                                                 "health_check_interval": health_check_interval,
                                                 "health_check_timeout": health_check_timeout
                                             }, requires_version=requires_version, requires_modules=requires_module)
    else:
        return isamAppliance.create_return_object()


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieving HA configuration
    """
    return isamAppliance.invoke_get("Retrieving HA configuration", "{0}".format(module_uri),
                                    requires_version=requires_version, requires_modules=requires_module)


def update(isamAppliance, is_primary, interface, remote, port, health_check_interval,
           health_check_timeout, check_mode=False, force=False):
<<<<<<< HEAD
    """
    Updating HA configuration
    """
    # Call to check function to see if configuration already exist
    update_required = _check_enable(isamAppliance, is_primary=is_primary, interface=interface, remote=remote,
                                    port=port, health_check_interval=health_check_interval,
                                    health_check_timeout=health_check_timeout)

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put("Updating HA configuration", module_uri,
                                            {
                                                "is_primary": is_primary,
                                                "interface": interface,
                                                "remote": remote,
                                                "port": port,
                                                "health_check_interval": health_check_interval,
                                                "health_check_timeout": health_check_timeout

                                            }, requires_modules=requires_module, requires_version=requires_version)
    else:
        return isamAppliance.create_return_object()

=======
    update_required = _check(isamAppliance, is_primary=is_primary, interface=interface, remote=remote,
                             port=port, health_check_interval=health_check_interval,
                             health_check_timeout=health_check_timeout)
    if force is True or update_required is True:
        return isamAppliance.invoke_put("Updating High Availability", module_uri,
                                        {
                                            "is_primary": is_primary,
                                            "interface": interface,
                                            "remote": remote,
                                            "port": port,
                                            "health_check_interval": health_check_interval,
                                            "health_check_timeout": health_check_timeout

                                        }, requires_modules=requires_module, requires_version=requires_version)
    elif check_mode is True:
        return isamAppliance.create_return_object(changed=False)
>>>>>>> upstream/master

def set(isamAppliance, is_primary, interface, remote, port, health_check_interval,
        health_check_timeout, check_mode=False, force=False):
    """
    determines if add or update is used.
    """
    check_obj = get(isamAppliance)

<<<<<<< HEAD
    if check_mode['data']['enabled'] is False:
        enable(isamAppliance, is_primary, interface, remote, port, health_check_interval,
               health_check_timeout, check_mode, force)

    else:
        update(isamAppliance, is_primary, interface, remote, port, health_check_interval,
               health_check_timeout, check_mode, force)


def _check_enable(isamAppliance, is_primary, interface, remote, port, health_check_interval,
                  health_check_timeout):
=======
def _check(isamAppliance, is_primary, interface, remote, port, health_check_interval,
           health_check_timeout, check_mode=False, force=False):
>>>>>>> upstream/master
    """
    idempotency test for each parameter
    """
    ret_obj = get(isamAppliance)
    if ret_obj['data']['enabled'] != True:
        return True
    elif ret_obj['data']['is_primary'] != is_primary:
        return True
    elif ret_obj['data']['interface'] != interface:
        return True
    elif ret_obj['data']['remote'] != remote:
        return True
    elif ret_obj['data']['port'] != port:
        return True
    elif ret_obj['data']['health_check_interval'] != health_check_interval:
        return True
    elif ret_obj['data']['health_check_timeout'] != health_check_timeout:
        return True
    else:
        return False
<<<<<<< HEAD


def _check_disable(isamAppliance):
    """
    Checks delete function for idempotency
    """
    check_obj = get(isamAppliance)

    if check_obj['data']['enabled'] == True:
        return True
    else:
        return False


def compare(isamAppliance1, isamAppliance2):
    """
    Compare cluster configuration between two appliances
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
=======
>>>>>>> upstream/master
