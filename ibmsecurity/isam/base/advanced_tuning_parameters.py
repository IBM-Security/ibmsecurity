import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get(isamAppliance, check_mode=False, force=False):
    """
    Get advanced tuning parameters
    """
    return isamAppliance.invoke_get("Get advanced tuning parameters",
                                    "/core/adv_params")


def set(isamAppliance, key, value, comment="", check_mode=False, force=False):
    """
    Set advanced tuning parameter
    """
    ret_obj = isamAppliance.create_return_object()
    rc, uuid = False, ""
    if not force:
        (rc, uuid) = _check(isamAppliance, key, value)

    if rc is False and uuid != "":
        if check_mode is True:
            ret_obj['changed'] = True
        else:
            ret_obj = isamAppliance.invoke_put(
                "Modifying existing advanced tuning parameter",
                "/core/adv_params/{0}".format(uuid),
                {
                    '_isNew': False,
                    'comment': comment,
                    'key': key,
                    'uuid': uuid,
                    'value': value
                })
    else:
        if force is True or (rc is False and uuid == ""):
            if check_mode is True:
                ret_obj['changed'] = True
            else:
                ret_obj = isamAppliance.invoke_post(
                    "Adding advanced tuning parameter",
                    "/core/adv_params",
                    {
                        '_isNew': True,
                        'comment': comment,
                        'key': key,
                        'value': value
                    })

    return ret_obj


def _check(isamAppliance, key, value):
    ret_obj = get(isamAppliance)

    rc = False
    uuid = ""
    for param in ret_obj['data']['tuningParameters']:
        if param['key'] == key:
            logger.info("Advanced tuning parameter [" + key + "] already exists")
            uuid = param['uuid']
            if str(param['value']) == str(value):
                logger.info("Advanced tuning parameter: {0} already exists with value: {1}".format(key, value))
                rc = True
            break

    return rc, uuid


def delete(isamAppliance, key, check_mode=False, force=False):
    """
    Delete advanced tuning parameter
    """
    ret_obj = isamAppliance.create_return_object()
    (rc, uuid) = _check(isamAppliance, key, "")

    if uuid != "":
        if check_mode is True:
            ret_obj['changed'] = True
        else:
            ret_obj = isamAppliance.invoke_delete(
                "Deleting existing advanced tuning parameter",
                "/core/adv_params/{0}".format(uuid))

    return ret_obj


def compare(isamAppliance1, isamAppliance2):
    """
    Compare advanced tuning parameters between two appliances
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    # Ignore differences between comments/uuid as they are immaterial
    for param in ret_obj1['data']['tuningParameters']:
        del param['comment']
        del param['uuid']
    for param in ret_obj2['data']['tuningParameters']:
        del param['comment']
        del param['uuid']

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['comment', 'uuid'])
