import logging

logger = logging.getLogger(__name__)


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the SSL certificate cluster replication status
    """
    return isamAppliance.invoke_get("Retrieving the SSL certificate cluster replication status",
                                    "/isam/ssl_certificates/?cluster=true")


def set(isamAppliance, replicating, check_mode=False, force=False):
    """
    Setting the SSL certificate cluster replication state
    """
    if force is True or _check(isamAppliance) != replicating:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put("Setting the SSL certificate cluster replication state",
                                            "/isam/ssl_certificates/v1",
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
