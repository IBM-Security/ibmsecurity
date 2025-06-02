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

    Note: Pass an array of values if needed to set a set of values for given key
    """
    ret_obj = isamAppliance.create_return_object()
    ret_obj['data'] = []
    rc, uuid = False, []
    # Force the value to be an array if not already so
    if not isinstance(value, list):
        value = [value]
    (rc, uuid) = _check(isamAppliance, key, value)

    # See if change detected or are being forced to do so
    if rc is False or force is True:
        if check_mode is True:
            ret_obj['changed'] = True
        else:
            # Remove any existing values...
            if len(uuid) > 0:
                _del(isamAppliance, uuid)
            # Add all new/modified values
            for v in value:
                r = isamAppliance.invoke_post(
                    "Adding advanced tuning parameter",
                    "/core/adv_params",
                    {
                        '_isNew': True,
                        'comment': comment,
                        'key': key,
                        'value': v
                    })
                ret_obj['changed'] = ret_obj['changed'] or r['changed']
                ret_obj['data'].append(r['data'])
                ret_obj['warnings'].extend(r['warnings'])
                ret_obj['rc'] += r['rc']

    return ret_obj


def _check(isamAppliance, key, value=None):
    ret_obj = get(isamAppliance)

    rc = False
    uuid = []
    exist_value_list = []
    for param in ret_obj['data']['tuningParameters']:
        if param['key'] == key:
            exist_value_list.append(str(param['value']))
            uuid.append(param['uuid'])
            logger.info(f"Advanced tuning parameter key: {key} and value: {value} exists")

    # value being none - means called from delete function
    if value is not None:
        given_value_list = []
        for v in value:
            given_value_list.append(str(v))
        rc = ibmsecurity.utilities.tools.json_sort(exist_value_list) == ibmsecurity.utilities.tools.json_sort(
            given_value_list)
        logger.info(
            f"Advanced tuning parameter: {key} has existing values: {exist_value_list}, and given values: {given_value_list} - match status: {rc}")

    return rc, uuid


def delete(isamAppliance, key, check_mode=False, force=False):
    """
    Delete advanced tuning parameter
    """
    ret_obj = isamAppliance.create_return_object()
    (rc, uuid) = _check(isamAppliance, key)

    if len(uuid) > 0:
        if check_mode is True:
            ret_obj['changed'] = True
        else:
            ret_obj = _del(isamAppliance, uuid)

    return ret_obj


def _del(isamAppliance, uuid):
    """
    Remove all UUIDs - should be everything pertaining to an advanced tuning parameter "key"

    :param isamAppliance:
    :param uuid:
    :return:
    """
    ret_obj = isamAppliance.create_return_object()
    ret_obj['data'] = []

    for u in uuid:
        r = isamAppliance.invoke_delete(
            "Deleting existing advanced tuning parameter",
            f"/core/adv_params/{u}")
        ret_obj['changed'] = ret_obj['changed'] or r['changed']
        ret_obj['data'].append(r['data'])
        ret_obj['warnings'].extend(r['warnings'])
        ret_obj['rc'] += r['rc']

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
