import logging

logger = logging.getLogger(__name__)


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieve runtime component replicaiton status
    """
    return isamAppliance.invoke_get("Retrieving web runtime component replication status",
                                    "/isam/runtime_components?cluster=true")


def set(isamAppliance, replicating, check_mode=False, force=False):
    """
    Set runtime component replication status
    """
    if force is True or _check(isamAppliance) != replicating:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put("Updating web runtime component replication status",
                                            "/isam/runtime_components?cluster=true",
                                            {
                                                'replicating': replicating
                                            })

    return isamAppliance.create_return_object()


def _check(isamAppliance):
    """
    Check the replicating status
    :param isamAppliance:
    :return:
    """
    ret_obj = get(isamAppliance)

    return ret_obj['data']['replicating']
