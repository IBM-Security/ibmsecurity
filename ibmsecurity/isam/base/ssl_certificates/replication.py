import logging

logger = logging.getLogger(__name__)
requires_model="Appliance"


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the SSL certificate cluster replication status
    """
    return isamAppliance.invoke_get("Retrieving the SSL certificate cluster replication status",
                                    "/isam/ssl_certificates/?cluster=true", requires_model=requires_model)


def set(isamAppliance, replicating, check_mode=False, force=False):
    """
    Setting the SSL certificate cluster replication state
    """

    check_obj = _check(isamAppliance, replicating)
    if force is True or check_obj['value'] is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=check_obj['warnings'])
        else:
            return isamAppliance.invoke_put("Setting the SSL certificate cluster replication state",
                                            "/isam/ssl_certificates/v1",
                                            {
                                                'replicating': replicating
                                            }, requires_model=requires_model)

    return isamAppliance.create_return_object(warnings=check_obj['warnings'])


def _check(isamAppliance, replicating):
    """
    Check the replicating status
    :param isamAppliance:
    :return:
    """

    check_obj = {'value': False, 'warnings':""}
    ret_obj = get(isamAppliance)
    check_obj['warnings']=ret_obj['warnings']

    if ret_obj['data'] != {}:
        if ret_obj['data']['replicating'] != replicating:
            check_obj['value'] = True
            return check_obj
        else:
            check_obj['value'] = False
            return check_obj

    return check_obj
