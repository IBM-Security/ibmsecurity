import ibmsecurity.utilities.tools
import logging

module_uri = "/isam/felb/configuration/ssl"
required_module = None
required_version = None

logger = logging.getLogger(__name__)


def enable(isamAppliance, keyfile, check_mode=False, force=False):
    """
    Creates ssl configuration
    """
    if force is True or _check_enable(isamAppliance, keyfile) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post("Creating SSL configuration", module_uri,
                                             {
                                                 "keyfile": keyfile
                                             }, requires_version=required_version, requires_modules=required_module)

    return isamAppliance.create_return_object()


def disable(isamAppliance, check_mode=False, force=False):
    """
    Deletes ssl configuration
    """
    if force is True or _check_disable(isamAppliance) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete("Disabling SSL", module_uri,
                                               requires_version=required_version, requires_modules=required_module)
    else:
        return isamAppliance.create_return_object()


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieves ssl configuration
    """
    return isamAppliance.invoke_get("Retrieving SSL configuration", module_uri,
                                    requires_version=required_version, requires_modules=required_module)


def update(isamAppliance, keyfile, check_mode=False, force=False):
    """
    Updating SSL configuration
    """
    # Call to check function to see if configuration already exist
    update_required = _check_enable(isamAppliance, keyfile)

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put("Updating SSL configuration", module_uri,
                                            {
                                                'keyfile': keyfile

                                            }, requires_modules=required_module, requires_version=required_version)

    return isamAppliance.create_return_object()


def _check_enable(isamAppliance, keyfile=None):
    """
    checks add function for idempotency
    """
    change_required = False
    check_obj = get(isamAppliance)
    # checks to see if ssl configuration exists
    try:
        if check_obj['data']['keyfile'] != keyfile:
            change_required = True
    except:
        change_required = True
    return change_required


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
