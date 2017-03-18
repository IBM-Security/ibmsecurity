import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get_application_interfaces(isamAppliance, check_mode=False, force=False):
    """
    Retrieve a list of application interfaces
    """
    return isamAppliance.invoke_get("Retrieve a list of application interfaces",
                                    "/isam/wga_templates/interfaces.json")


def get_ip_addresses(isamAppliance, check_mode=False, force=False):
    """
    Listing IP addresses for all interfaces
    """
    return isamAppliance.invoke_get("Listing IP addresses for all interfaces",
                                    "/isam/wga_templates/ipaddress")

def get_next_http_port(isamAppliance, ip_address, check_mode=False, force=False):
    """
    Find the next available HTTP port for an interface
    """
    return isamAppliance.invoke_get("Find the next available HTTP port for an interface",
                                    "/isam/wga_templates/httpport/{0}".format(ip_address))

def get_next_https_port(isamAppliance, ip_address, check_mode=False, force=False):
    """
    Find the next available HTTPS port for an interface
    """
    return isamAppliance.invoke_get("Find the next available HTTPS port for an interface",
                                    "/isam/wga_templates/httpsport/{0}".format(ip_address))
