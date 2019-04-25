import logging

logger = logging.getLogger(__name__)


def get(isamAppliance, id, check_mode=False, force=False):
    """
    Retrieve the value of a property in the cluster configuration
    """
    return isamAppliance.invoke_get("Retrieve the value of a property in the cluster configuration",
                                    "/isam/cluster/property/{0}/v2".format(id))


def add(isamAppliance, id, value, check_mode=False, force=False):
    """
    Create a new property in the cluster configuration
    """
    if force is True or _check(isamAppliance, id) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post(
                "Create a new property in the cluster configuration",
                "/isam/cluster/property/v2",
                {
                    "id": id,
                    "value": value
                })

    return isamAppliance.create_return_object()


def update(isamAppliance, id, value, check_mode=False, force=False):
    """
    Update the value of a property in the cluster configuration
    """
    if force is True or _check(isamAppliance, id, value) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Update the value of a property in the cluster configuration",
                "/isam/cluster/property/{0}/v2".format(id),
                {
                    "value": value
                })

    return isamAppliance.create_return_object()


def _check(isamAppliance, id, value=None):
    ret_obj = None
    try:
        ret_obj = get(isamAppliance, id)
    except:
        pass

    if ret_obj is None:
        return False
    else:
        if value is not None and value != ret_obj['data']['value']:
            return False

    return True


def delete(isamAppliance, id, check_mode=False, force=False):
    """
    Delete a property from the cluster configuration
    """
    if force is True or _check(isamAppliance, id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Delete a property from the cluster configuration",
                "/isam/cluster/property/{0}/v2".format(id))

    return isamAppliance.create_return_object()
