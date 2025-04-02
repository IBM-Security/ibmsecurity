import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get_all_app(isvgAppliance, check_mode=False, force=False):
    """
    Retrieving all application interfaces
    :rtype: (str, dict)
    """
    return isvgAppliance.invoke_get("Retrieving all application interfaces", "/application_interfaces")


def add(isvgAppliance, address, netmask, network_type, ipFqdn, gateway, interface="P.1", check_mode=False,
        force=False):
    """
    Adding an address to an application interface
    """
    if force is True or _check(isvgAppliance, address, netmask, network_type, ipFqdn, gateway, interface) is False:
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True)
        else:
            return isvgAppliance.invoke_post(
                "Configuring address for application interface",
                "/application_interfaces/" + interface + "/addresses",
                {
                    'address': address,
                    'netmask': netmask,
                    'type': network_type,
                    'ipFqdn': ipFqdn,
                    'gateway': gateway
                })

    return isvgAppliance.create_return_object()


def _check(isvgAppliance, address, netmask, network_type, ipFqdn, gateway, interface, check_mode=False,
        force=False):
    """
    Check whether application interface is configured
    """
    check_value = False

    ret_obj = get_all_app(isvgAppliance)

    for intf in ret_obj['data']:
        if intf['id'] == interface and intf['state'] == "up":
            logger.warning("Application interface already configured")
            check_value = True
            break

    return check_value
