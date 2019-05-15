import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get(isdsAppliance, check_mode=False, force=False):
    """
    Get host records
    """
    return isdsAppliance.invoke_get("Retrieving current host records",
                                    "/host_records")


def set(isdsAppliance, hostname, ip_addr, check_mode=False, force=False):
    """
    Add host records
    """
    if force is True or _check(isdsAppliance, hostname, ip_addr) is False:
        if check_mode is True:
            return isdsAppliance.create_return_object(changed=True)
        else:
            return isdsAppliance.invoke_post(
                "Setting host record",
                "/host_records",
                {
                    'hostnames': [{"name": hostname}],
                    'addr': ip_addr
                })

    return isdsAppliance.create_return_object()


def delete(isdsAppliance, hostname, ip_addr, check_mode=False, force=False):
    """
    Delete a host record
    :param isdsAppliance:
    :param hostname:
    :param ip_addr:
    :param check_mode:
    :param force:
    :return:
    """
    if force is True or _check(isdsAppliance, hostname, ip_addr) is True:
        if check_mode is True:
            return isdsAppliance.create_return_object(changed=True)
        else:
            return isdsAppliance.invoke_delete(
                "Removing host record",
                "/host_records/" + ip_addr,
                {
                })
    return isdsAppliance.create_return_object()


def _check(isdsAppliance, hostname, ip_addr, check_mode=False, force=False):
    """
    check whether hostname has been defined
    :param isdsAppliance:
    :param hostname:
    :param ip_addr:
    :param check_mode:
    :param force:
    :return:
    """
    ret_obj = get(isdsAppliance)

    for hosts in ret_obj['data']:
        if hosts['addr'] == ip_addr:
            for names in hosts['hostnames']:
                if names['name'] == hostname:
                    logger.info("hostname record exists, skip")
                    return True

    return False
