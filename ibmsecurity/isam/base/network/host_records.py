import logging
from ibmsecurity.appliance.ibmappliance import IBMError
from ibmsecurity.utilities.tools import json_compare

logger = logging.getLogger(__name__)

requires_model = "Appliance"

try:
    basestring
except NameError:
    basestring = (str, bytes)


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the list of host IP addresses
    """
    return isamAppliance.invoke_get("Retrieving the list of host IP addresses",
                                    "/isam/host_records", requires_model=requires_model)


def get(isamAppliance, addr, check_mode=False, force=False):
    """
    Retrieving the list of host names associated with a host IP address
    """
    return isamAppliance.invoke_get("Retrieving the list of host names associated with a host IP address {0}".format(addr),
                                    "/isam/host_records/{0}/hostnames".format(addr), requires_model=requires_model)


def set(isamAppliance, addr, hostnames, check_mode=False, force=False):
    """
    Creates or updates specified address with supplied hostnames.

    :param isamAppliance:
    :param addr:          String, addr of host record to update
    :param hostnames:     Array, hostnames to be added
    :param check_mode:
    :param force:
    :return:
    """

    # Make sure if only one hostname is entered that it is an array
    if isinstance(hostnames, basestring):
        hostnames = [hostnames]

    ret_obj = isamAppliance.create_return_object()
    exists = False
    hostnames_remaining = hostnames
    addr_exists = True

    if force is False:
        exists, hostnames_remaining, addr_exists, warnings = _check(isamAppliance, addr, hostnames)
        ret_obj['warnings'] = warnings

    if force or exists is False:
        if check_mode is True:
            ret_obj['changed'] = True
        else:
            if addr_exists:
                # Call update for each hostname
                for name in hostnames_remaining:
                    # Forcing because we've already checked that the hostnames don't exist
                    # TODO: determine how best to return this, since it makes multiple requests
                    update(isamAppliance, addr, name, check_mode, force=True)
                    ret_obj['changed'] = True
            else:
                # Forcing because we've already checked that the hostnames don't exist
                return add(isamAppliance, addr, hostnames_remaining, check_mode, force=True)

    return ret_obj


def add(isamAppliance, addr, hostnames, check_mode=False, force=False):
    """
    Creating a host record (IP address and host name)
    :param isamAppliance:
    :param addr:          String, addr of host record to update
    :param hostnames:     Array, hostnames to be added
    :param check_mode:
    :param force:
    :return:
    """

    # Make sure if only one hostname is entered that it is an array
    if isinstance(hostnames, basestring):
        hostnames = [hostnames]

    exists = False
    hostnames_remaining = hostnames
    addr_exists = True

    if force is False:
        exists, hostnames_remaining, addr_exists, warnings = _check(isamAppliance, addr, hostnames)

    if force or addr_exists is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            # Format POST response correctly
            hostnames_post = []
            for entry in hostnames_remaining:
                hostnames_post.append({'name': entry})

            return isamAppliance.invoke_post(
                "Creating a host record (IP address and host name)",
                "/isam/host_records",
                {
                    'addr': addr,
                    'hostnames': hostnames_post
                }, requires_model=requires_model)
    return isamAppliance.create_return_object(warnings=warnings)


def update(isamAppliance, addr, name, check_mode=False, force=False):
    """
    Adding a host name to a host IP address

    :param isamAppliance:
    :param addr:          String, addr of host record to update
    :param name:          String, hostname to add to addr
    :return:
    """

    exists = False
    hostnames_remaining = [name]
    addr_exists = True

    if force is False:
        exists, hostnames_remaining, addr_exists, warnings = _check(isamAppliance, addr, [name])
        if addr_exists is False:
            if warnings == []:
                raise IBMError("HTTP Return code: 404",
                               "Specified addr does not exist in the hosts file, cannot update.")
            else:
                return isamAppliance.create_return_object(warnings=warnings)

    if force or exists is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_post(
                "Adding a host name to a host IP address",
                "/isam/host_records/{0}/hostnames".format(addr),
                {'name': hostnames_remaining[0]},
                requires_model=requires_model
            )

    return isamAppliance.create_return_object(warnings=warnings)


def delete(isamAppliance, addr, name=None, check_mode=False, force=False):
    """
    Removing a host name from a host IP address
    :param isamAppliance:
    :param addr:          String, addr of host record to update
    :param name:          String, hostname to add to addr
    :param check_mode:
    :param force:
    :return:
    """

    exists = False
    addr_exists = True

    if force is False:
        exists, _, addr_exists, warnings = _check(isamAppliance, addr, [name])
        if addr_exists is False:
            return isamAppliance.create_return_object(warnings=warnings)

    if force or exists is True or name is None:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            if exists is True:
                # Delete specific entry
                return isamAppliance.invoke_delete(
                    "Removing a host name from a host IP address",
                    "/isam/host_records/{0}/hostnames/{1}".format(addr, name),
                    requires_model=requires_model
                )
            elif exists is False and name is None:
                # Delete all entries for address if no name given
                return isamAppliance.invoke_delete(
                    "Removing a host record (IP address and associated host names)",
                    "/isam/host_records/{0}".format(addr),
                    requires_model=requires_model
                )

    return isamAppliance.create_return_object(warnings=warnings)


def _check(isamAppliance, addr, hostnames=[]):
    """
    Check addr has all hostnames set
    """
    exists = False
    addr_exists = False

    # Make sure addr exists in host records

    ret_obj = get_all(isamAppliance)
    warnings = ret_obj['warnings']

    for obj in ret_obj['data']:
        if obj['addr'] == addr:
            addr_exists = True
            if len(hostnames) > 0:
                for entry in obj['hostnames']:
                    if entry['name'] in hostnames:
                        hostnames.remove(entry['name'])
                        logger.debug("Host record exists, continuing checking")

    if addr_exists is False:
        logger.debug("Host record does not exist")
        return exists, hostnames, addr_exists, warnings
    else:
        if len(hostnames) < 1:
            exists = True
            logger.info("All host records exist")
        else:
            logger.info("Not all host records exist")

    return exists, hostnames, addr_exists, warnings


def compare(isamAppliance1, isamAppliance2):
    """
    Compare host records between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    # # Ignore differences between comments/uuid as they are immaterial
    # for param in ret_obj1['data']['tuningParameters']:
    #     del param['comment']
    #     del param['uuid']
    # for param in ret_obj2['data']['tuningParameters']:
    #     del param['comment']
    #     del param['uuid']

    return json_compare(ret_obj1, ret_obj2)
