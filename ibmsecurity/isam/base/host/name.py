import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)
uri = "/isam/host_records"
requires_modules = None
requires_version = None


def add(isamAppliance, host_address, hostname, check_mode=False, force=False):
    """
    Adding a host name to a host IP address
    """
    if force is True or _check(isamAppliance, host_address, hostname) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post(
                "Adding a host name to a host IP address",
                "{0}/{1}/hostnames".format(uri, host_address),
                {
                    "name": hostname
                },
                requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()


def delete(isamAppliance, host_address, hostname, check_mode=False, force=False):
    """
    Removing a host name from a host IP address
    """
    if force is True or _check(isamAppliance, host_address, hostname) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Removing a host name from a host IP address",
                "{0}/{1}/hostnames/{2}".format(uri, host_address, hostname),
                requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()


def _check(isamAppliance, host_address, hostname):
    """
    Check whether existing host record contains a host name
    """
    import ibmsecurity.isam.base.host.records
    try:
        ret_obj = ibmsecurity.isam.base.host.records.get(isamAppliance, host_address=host_address)
    except:
        from ibmsecurity.appliance.ibmappliance import IBMError
        raise IBMError("999", "Unable to find host record with adress: {0}".format(host_address))

    for hosts in ret_obj['data']:
        if hosts['name'].lower() == str(hostname).lower():
            return True

    return False
