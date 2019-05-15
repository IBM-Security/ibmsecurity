import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get(isdsAppliance, ip_addr, check_mode=False, force=False):
    """
    Get hostnames for a host record
    """
    return isdsAppliance.invoke_get("Retrieving hostnames for a host record",
                                    "/host_records/" + ip_addr + "/hostnames")


def add(isdsAppliance, hostname, ip_addr, check_mode=False, force=False):
    """
    Add hostname to host record
    """
    if force is True or _check(isdsAppliance, hostname, ip_addr) is False:
        if check_mode is True:
            return isdsAppliance.create_return_object(changed=True)
        else:
            return isdsAppliance.invoke_post(
                "Adding hostname to host record",
                "/host_records/" + ip_addr + "/hostnames",
                {
                    'name': hostname
                })

    return isdsAppliance.create_return_object()


def delete(isdsAppliance, hostname, ip_addr, check_mode=False, force=False):
    """
    Delete a hostname from a host record
    """
    if force is True or _check(isdsAppliance, hostname, ip_addr) is True:
        if check_mode is True:
            return isdsAppliance.create_return_object(changed=True)
        else:
            return isdsAppliance.invoke_delete(
                "Removing hostname",
                "/host_records/" + ip_addr + "/hostnames/" + hostname)

    return isdsAppliance.create_return_object()


def _check(isdsAppliance, hostname, ip_addr, check_mode=False, force=False):
    """
    Check whether hostname has been defined
    """
    ret_obj = get(isdsAppliance, ip_addr)

    for names in ret_obj['data']:
        if names['name'] == hostname:
            logger.info("Hostname record exists")
            return True

    return False
