import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieving all interfaces
    :rtype: (str, dict)
    """
    return isamAppliance.invoke_get("Retrieving all interfaces", "/net/ifaces")


def get(isamAppliance, uuid, check_mode=False, force=False):
    """
    Retrieving a single interface
    """
    return isamAppliance.invoke_get("Retrieving a single interface", "/net/ifaces/" + uuid)


def _get_ipv4_addresses(isamAppliance, label, vlanId=None):
    """
    Retrieving ipv4 addresses for an interface label
    """
    ret_obj = get_all(isamAppliance)
    i = None

    for intfc in ret_obj['data']['interfaces']:
        if intfc['label'] == label and intfc['vlanId'] == vlanId:
            i = intfc
            break

    ipv4_addresses = []
    if i is not None:
        for ads in i['ipv4']['addresses']:
            ipv4_addresses.append(ads['address'])

    return ipv4_addresses


def get_ipv4_addresses(isamAppliance, label, vlanId=None, check_mode=False, force=False):
    """
    Retrieving ipv4 addresses for an interface label
    """
    ret_obj = isamAppliance.create_return_object()
    ret_obj['data'] = _get_ipv4_addresses(isamAppliance, label, vlanId)

    return ret_obj


def get_ipv6_addresses(isamAppliance, label, vlanId=None, check_mode=False, force=False):
    """
    Retrieving ipv6 addresses for an interface label
    """
    ret_obj = get_all(isamAppliance)
    i = None

    for intfc in ret_obj['data']['interfaces']:
        if intfc['label'] == label and intfc['vlanId'] == vlanId:
            i = intfc
            break

    ipv6_addresses = []
    if i is not None:
        for adds in i['ipv6']['addresses']:
            ipv6_addresses.append(adds['address'])

    ret_obj = isamAppliance.create_return_object()
    ret_obj['data'] = ipv6_addresses

    return ret_obj


def _get_interface(isamAppliance, label, vlanId=None, check_mode=False, force=False):
    """
    Retrieving a uuid for given interface label
    """
    ret_obj = get_all(isamAppliance)

    for intfc in ret_obj['data']['interfaces']:
        if intfc['label'] == label and intfc['vlanId'] == vlanId:
            return intfc

    return None


def search(isamAppliance, label=None, vlanId=None, address=None, check_mode=False, force=False):
    """
    Search UUID for given label/vlanid
    """
    ret_obj = isamAppliance.create_return_object()
    if label is not None:
        intf = _get_interface(isamAppliance, label, vlanId, check_mode, force)
        ret_obj['data'] = intf['uuid']
        return ret_obj
    elif address is not None:
        objs = get_all(isamAppliance)
        for intfc in objs['data']['interfaces']:
            for adds in intfc['ipv4']['addresses']:
                if adds['address'] == address:
                    ret_obj['data'] = adds['uuid']
                    return ret_obj

    return ret_obj


def _update_interface(isamAppliance, json_data):
    return isamAppliance.invoke_put("Updating a (VLAN) interface", "/net/ifaces/{0}".format(json_data['uuid']),
                                    json_data)


def compare(isamAppliance1, isamAppliance2, reverseproxy_id):
    """
    Compare interfaces between 2 appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    for intfc in ret_obj1['data']['interfaces']:
        del intfc['uuid']
        del intfc['bondedTo']
        for ipv4 in intfc['ipv4']['addresses']:
            del ipv4['uuid']
        for ipv6 in intfc['ipv6']['addresses']:
            del ipv6['uuid']
    for intfc in ret_obj2['data']['interfaces']:
        del intfc['uuid']
        del intfc['bondedTo']
        for ipv4 in intfc['ipv4']['addresses']:
            del ipv4['uuid']
            del ipv4['address']
        for ipv6 in intfc['ipv6']['addresses']:
            del ipv6['uuid']
            del ipv6['address']

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2,
                                                    deleted_keys=['uuid', 'bondedTo',
                                                                  'ipv4/addresses/uuid', 'ipv4/addresses/address',
                                                                  'ipv6/addresses/uuid', 'ipv6/addresses/address'])
