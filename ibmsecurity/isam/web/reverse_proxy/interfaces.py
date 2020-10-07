import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)
requires_model = "Appliance"

def get_application_interfaces(isamAppliance, check_mode=False, force=False):
    """
    Retrieve a list of application interfaces
    """
    return isamAppliance.invoke_get("Retrieve a list of application interfaces",
                                    "/isam/wga_templates/interfaces.json",requires_model=requires_model)


def get_ip_addresses(isamAppliance, check_mode=False, force=False):
    """
    Listing IP addresses for all interfaces
    """
    return isamAppliance.invoke_get("Listing IP addresses for all interfaces",
                                    "/isam/wga_templates/ipaddress",requires_model=requires_model)


def get_next_http_port(isamAppliance, ip_address, check_mode=False, force=False):
    """
    Find the next available HTTP port for an interface
    """
    if ibmsecurity.utilities.tools.version_compare(isamAppliance.facts["version"], "8.0.0.0") < 0:
        get_uri = "/isam/wga_templates/httpport/{0}".format(ip_address)
    else:
        get_uri = "/isam/wga_templates/httpport?ip_addr={0}".format(ip_address)

    return isamAppliance.invoke_get("Find the next available HTTP port for an interface", get_uri,requires_model=requires_model)


def get_next_https_port(isamAppliance, ip_address, check_mode=False, force=False):
    """
    Find the next available HTTPS port for an interface
    """
    if ibmsecurity.utilities.tools.version_compare(isamAppliance.facts["version"], "8.0.0.0") < 0:
        get_uri = "/isam/wga_templates/httpsport/{0}".format(ip_address)
    else:
        get_uri = "/isam/wga_templates/httpsport?ip_addr={0}".format(ip_address)

    return isamAppliance.invoke_get("Find the next available HTTPS port for an interface", get_uri,requires_model=requires_model)


def get_defaults(isamAppliance, check_mode=False, force=False):
    """
    Get defaults
    """
    return isamAppliance.invoke_get("Get defaults", "/isam/wga_templates/defaults",requires_model=requires_model)
