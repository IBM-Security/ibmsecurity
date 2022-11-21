import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get(isvgAppliance, ip_addr, check_mode=False, force=False):
    """
    Get hostnames for a host record
    """
    return isvgAppliance.invoke_get("Retrieving hostnames for a host record",
                                    "/host_records/" + ip_addr + "/hostnames")


def add(isvgAppliance, hostname, ip_addr, check_mode=False, force=False):
    """
    Add hostname to host record
    """
    if force is True or _check(isvgAppliance, hostname, ip_addr) is False:
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True)
        else:
            return isvgAppliance.invoke_post(
                "Adding hostname to host record",
                "/host_records/" + ip_addr + "/hostnames",
                {
                    'name': hostname
                })

    return isvgAppliance.create_return_object()


def delete(isvgAppliance, hostname, ip_addr, check_mode=False, force=False):
    """
    Delete a hostname from a host record
    """
    if force is True or _check(isvgAppliance, hostname, ip_addr) is True:
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True)
        else:
            return isvgAppliance.invoke_delete(
                "Removing hostname",
                "/host_records/" + ip_addr + "/hostnames/" + hostname)

    return isvgAppliance.create_return_object()


def _check(isvgAppliance, hostname, ip_addr, check_mode=False, force=False):
    """
    Check whether hostname has been defined
    """
    ret_obj = get(isvgAppliance, ip_addr)

    for names in ret_obj['data']:
        if names['name'] == hostname:
            logger.info("Hostname record exists")
            return True

    return False
