import logging

logger = logging.getLogger(__name__)


def get(isamAppliance, check_mode=False, force=False):
    """
    Get runtime endpoints or listening interfaces
    """

    return isamAppliance.invoke_get("Retrieving runtime listening interfaces",
                                    "/mga/runtime_tuning/v1")


def set(isamAppliance, interface, port, secure, check_mode=False, force=False):
    """
    Set a runtime listening interface
    """
    ret_obj = isamAppliance.create_return_object()
    exists = False
    secure_existing = None
    if force is False:
        exists, secure_existing, id = _check(isamAppliance, interface, port)

    # Delete if interface has different secure setting
    if exists is True and secure_existing != secure:
        if check_mode is True:
            ret_obj['changed'] = True
        else:
            delete(isamAppliance, interface, port, check_mode, force)
        exists = False

    if force or exists is False:
        if check_mode is True:
            ret_obj['changed'] = True
        else:
            return isamAppliance.invoke_post(
                "Setting a runtime listening interface",
                "/mga/runtime_tuning/endpoints/v1",
                {
                    'interface': interface,
                    'port': port,
                    'secure': secure
                })

    return ret_obj

def set_by_label(isamAppliance, interface_label, interface_address, port, secure, check_mode=False, force=False):
    """
    Set a runtime listening interface by interface label and ip address
    """

    ret_obj = isamAppliance.create_return_object()
    exists = False
    secure_existing = None

    logger.info("Getting interface uuid from label {0}".format(interface_label))

    #get interface uuid
    ifaces = ibmsecurity.isam.base.network.interfaces.get_all(isamAppliance)
    iface = [i for i in ifaces['data']['interfaces'] if i['label'] == interface_label]

    #throw error if no interface is found
    if len(iface) == 0:
        ret_obj['changed'] = False
        ret_obj['rc'] = 1
        ret_obj['warnings'] = "No interface with this label found."
        return ret_obj

    iface = iface[0]


    #check for dhcp
    if iface['ipv4']['dhcp']['enabled']:
        interface = "{0}.dhcp.ipv4".format(iface['uuid'])
    else:
        #get address uuid
        address = [a for a in iface['ipv4']['addresses'] if a['address'] == interface_address]

        #throw error if no address is found
        if len(address) == 0:
            ret_obj['changed'] = False
            ret_obj['rc'] = 1
            ret_obj['warnings'] = "No IP-Address found"
            return ret_obj

        address = address[0]
        interface = "{0}.{1}".format(iface['uuid'], address['uuid'])


    logger.info("Found interface uuid from label: {0}".format(interface))


    if force is False:
        exists, secure_existing, id = _check(isamAppliance, interface, port)

    # Delete if interface has different secure setting
    if exists is True and secure_existing != secure:
        if check_mode is True:
            ret_obj['changed'] = True
        else:
            delete(isamAppliance, interface, port, check_mode, force)
        exists = False

    if force or exists is False:
        if check_mode is True:
            ret_obj['changed'] = True
        else:
            return isamAppliance.invoke_post(
                "Setting a runtime listening interface",
                "/mga/runtime_tuning/endpoints/v1",
                {
                    'interface': interface,
                    'port': port,
                    'secure': secure
                })

    return ret_obj


def _check(isamAppliance, interface, port):
    """
    Check listening interface for the runtime
    """
    ret_obj = get(isamAppliance)

    exists = False
    secure = False
    id = None
    try:
        for endpoint in ret_obj['data']['endpoints']:
            if endpoint['interface'] == interface and int(endpoint['port']) == int(port):
                logger.info("Runtime listening parameter already exists")
                exists = True
                secure = endpoint['secure']
                id = endpoint['id']
                break
            else:
                logger.debug("Runtime listening parameter does not match")
    except:
        logger.info("Runtime listening parameter does not exist")

    return exists, secure, id


def delete(isamAppliance, interface, port, check_mode=False, force=False):
    """
    Delete a runtime listening interface
    """
    exists = False
    id = None
    if force is False:
        exists, secure, id = _check(isamAppliance, interface, port)

    if force is True or exists is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Delete a runtime listening interface",
                "/mga/runtime_tuning/endpoints/{0}/v1".format(id))

    return isamAppliance.create_return_object()


def compare(isamAppliance1, isamAppliance2):
    """
    Compare runtime listening interface
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    try:
        endpoint1 = ret_obj1['data']['endpoints']
        for endpoint in endpoint1:
            if endpoint['id'] != 'local-interface' and endpoint['id'] != 'all-application-interfaces':
                del endpoint['id']
                del endpoint['interface']
    except:
        pass

    try:
        endpoint2 = ret_obj2['data']['endpoints']
        for endpoint in endpoint2:
            if endpoint['id'] != 'local-interface' and endpoint['id'] != 'all-application-interfaces':
                del endpoint['id']
                del endpoint['interface']
    except:
        pass

    import ibmsecurity.utilities.tools
    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['id', 'interface'])
