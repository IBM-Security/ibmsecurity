import logging
import ibmsecurity.utilities.tools
import ibmsecurity.isam.base.network.interfaces

logger = logging.getLogger(__name__)


def add(isamAppliance, label, address, maskOrPrefix, overrideSubnetChecking=False, vlanId=None, allowManagement=False,
        enabled=True, check_mode=False,
        force=False):
    """
    Adding an IPv4 address to an interface
    """
    add_needed = True
    ret_obj = {}
    warnings = []
    if force is False:
        ret_obj, warnings = ibmsecurity.isam.base.network.interfaces._get_interface(isamAppliance, label, vlanId)
        if ret_obj is not None:
            del ret_obj['objType']
            del ret_obj['type']
            for addr in ret_obj['ipv4']['addresses']:
                if addr['address'] == address:
                    add_needed = False
        else:
            warnings.append("Interface {0} not found, Add is not supported.".format(label))
            return isamAppliance.create_return_object(changed=False, warnings=warnings)

    if add_needed is True:
        ret_obj['ipv4']['overrideSubnetChecking'] = overrideSubnetChecking
    if force is True or add_needed is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            addr = {
                '_isNew': True,
                'objType': 'ipv4Address',
                'uuid': None,
                'address': address,
                'maskOrPrefix': maskOrPrefix,
                'allowManagement': allowManagement,
                'enabledAddress': True,
                'enabled': enabled
            }
            ret_obj['ipv4']['addresses'].append(addr)
            return ibmsecurity.isam.base.network.interfaces._update_interface(isamAppliance, ret_obj)

    return isamAppliance.create_return_object()


def delete(isamAppliance, label, address, vlanId=None, check_mode=False, force=False):
    """
    Deleting an IPv4 address from an interface
    """
    delete_needed = False
    ret_obj = {}
    warnings = []
    if force is False:
        ret_obj, warnings = ibmsecurity.isam.base.network.interfaces._get_interface(isamAppliance, label, vlanId)
        if ret_obj is not None:
            for addr in ret_obj['ipv4']['addresses']:
                if addr['address'] == address:
                    delete_needed = True
                    ret_obj['ipv4']['addresses'].remove(addr)
                    break
        else:
            warnings.append("Interface {0} not found, Delete is not supported.".format(label))
            return isamAppliance.create_return_object(changed=False, warnings=warnings)

    if force is True or delete_needed is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return ibmsecurity.isam.base.network.interfaces._update_interface(isamAppliance, ret_obj)

    return isamAppliance.create_return_object()


def update(isamAppliance, label, address, new_address, maskOrPrefix, vlanId=None, allowManagement=False, enabled=True,
           overrideSubnetChecking=False, check_mode=False, force=False):
    """
    Updating an IPv4 address on an interface
    """
    update_needed = False
    ret_obj = {}
    warnings = []
    if force is False:
        ret_obj, warnings = ibmsecurity.isam.base.network.interfaces._get_interface(isamAppliance, label, vlanId)
        if ret_obj is not None:
            for addr in ret_obj['ipv4']['addresses']:
                if addr['address'] == address:
                    upd_addr = {
                        'uuid': addr['uuid'],
                        'address': new_address,
                        'maskOrPrefix': maskOrPrefix,
                        'allowManagement': allowManagement,
                        'enabled': enabled
                    }
                    update_needed = not (
                            ibmsecurity.utilities.tools.json_sort(addr) == ibmsecurity.utilities.tools.json_sort(
                        upd_addr))
                    if (update_needed is True):
                        ret_obj['ipv4']['addresses'].remove(addr)
                        ret_obj['ipv4']['addresses'].append(upd_addr)
                        ret_obj['ipv4']['overrideSubnetChecking'] = overrideSubnetChecking
                    break
        else:
            warnings.append("Interface {0} not found, Update is not supported.".format(label))
            return isamAppliance.create_return_object(changed=False, warnings=warnings)

    if force is True or update_needed is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return ibmsecurity.isam.base.network.interfaces._update_interface(isamAppliance, ret_obj)

    return isamAppliance.create_return_object()


def set_dhcp(isamAppliance, label, vlanId=None, enabled=False, allowManagement=False, providesDefaultRoute=False,
             routeMetric=None, check_mode=False, force=False):
    """
    Updating IPv4 dhcp on an interface
    """
    update_needed = False
    ret_obj = {}
    warnings = []
    if force is False:
        ret_obj, warnings = ibmsecurity.isam.base.network.interfaces._get_interface(isamAppliance, label, vlanId)
        if ret_obj is not None:
            upd_dhcp = {
                'enabled': enabled,
                'allowManagement': allowManagement,
                'providesDefaultRoute': providesDefaultRoute,
                'routeMetric': routeMetric
            }
            update_needed = not (
                    ibmsecurity.utilities.tools.json_sort(
                        ret_obj['ipv4']['dhcp']) == ibmsecurity.utilities.tools.json_sort(
                upd_dhcp))
            if (update_needed is True):
                ret_obj['ipv4']['dhcp'] = upd_dhcp
        else:
            warnings.append("Interface {0} not found, Set dhcp is not supported.".format(label))
            return isamAppliance.create_return_object(changed=False, warnings=warnings)

    if force is True or update_needed is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return ibmsecurity.isam.base.network.interfaces._update_interface(isamAppliance, ret_obj)

    return isamAppliance.create_return_object()


def search(isamAppliance, address, check_mode=False, force=False):
    """
    Retrieving uuid for an ipv4 address
    """
    ret_obj = ibmsecurity.isam.base.network.interfaces.get_all(isamAppliance)
    ipv4_address_uuid = None

    for intfc in ret_obj['data']['interfaces']:
        for adds in intfc['ipv4']['addresses']:
            if adds['address'] == address:
                ipv4_address_uuid = adds['uuid']
                break

    ret_obj = isamAppliance.create_return_object()
    ret_obj['data'] = ipv4_address_uuid

    return ret_obj
