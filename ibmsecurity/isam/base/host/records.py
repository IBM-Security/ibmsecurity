import logging
from ibmsecurity.utilities.tools import json_sort, json_compare

logger = logging.getLogger(__name__)
uri = "/isam/host_records"
requires_modules = None
requires_version = None


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the list of host IP addresses
    """
    return isamAppliance.invoke_get(
        "Retrieving the list of host IP addresses",
        uri,
        requires_modules=requires_modules,
        requires_version=requires_version,
    )


def get(isamAppliance, host_address, check_mode=False, force=False):
    """
    Retrieving the list of host names associated with a host IP address
    """
    return isamAppliance.invoke_get(
        "Retrieving the list of host names associated with a host IP address",
        f"{uri}/{host_address}/hostnames",
        requires_modules=requires_modules,
        requires_version=requires_version,
    )


def set(isamAppliance, addr, hostnames, check_mode=False, force=False):
    """
    Setting a host record (IP address and host name)

    Sample JSON:
    {"addr":"127.0.0.2","hostnames":[{"name":"test1.ibm.com"}, {"name":"test2.ibm.com"}]}
    """
    add_required = False
    delete_required = False
    if force is False:
        # Check if record exists
        if _check(isamAppliance, addr) is True:
            ret_obj = get(isamAppliance, host_address=addr)
            # Check if hostnames match (case sensitive check)
            if json_sort(ret_obj["data"]) != json_sort(hostnames):
                delete_required = True
                add_required = True
        else:
            add_required = True

    if force is True or delete_required is True:
        # No need to check if record exists - force delete
        delete(isamAppliance, host_address=addr, check_mode=check_mode, force=True)

    if force is True or add_required is True:
        # No need to check for add - force add
        return add(
            isamAppliance,
            addr=addr,
            hostnames=hostnames,
            check_mode=check_mode,
            force=True,
        )

    return isamAppliance.create_return_object()


def add(isamAppliance, addr, hostnames, check_mode=False, force=False):
    """
    Creating a host record (IP address and host name)

    Sample JSON:
    {"addr":"127.0.0.2","hostnames":[{"name":"test1.ibm.com"}, {"name":"test2.ibm.com"}]}
    """
    if force is True or _check(isamAppliance, addr) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post(
                "Creating a host record (IP address and host name)",
                uri,
                {"addr": addr, "hostnames": hostnames},
                requires_modules=requires_modules,
                requires_version=requires_version,
            )

    return isamAppliance.create_return_object()


def delete(isamAppliance, host_address, check_mode=False, force=False):
    """
    Removing a host record (IP address and associated host names)
    """
    if force is True or _check(isamAppliance, host_address) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Removing a host record (IP address and associated host names)",
                f"{uri}/{host_address}",
                requires_modules=requires_modules,
                requires_version=requires_version,
            )

    return isamAppliance.create_return_object()


def _check(isamAppliance, addr, check_mode=False, force=False):
    """
    check whether addr has been defined
    """
    ret_obj = get_all(isamAppliance)

    for hosts in ret_obj["data"]:
        if hosts["addr"] == addr:
            return True

    return False


def compare(isamAppliance1, isamAppliance2):
    """
    Compare Host Records between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    return json_compare(ret_obj1, ret_obj2, deleted_keys=[])
