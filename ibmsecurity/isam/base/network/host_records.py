import logging
from ibmsecurity.appliance.ibmappliance import IBMError
from ibmsecurity.utilities.tools import json_compare

logger = logging.getLogger(__name__)

try:
    basestring
except NameError:
    basestring = (str, bytes)


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Get all current host records
    """
    return isamAppliance.invoke_get("Retrieving current host records",
                                    "/isam/host_records")


def get(isamAppliance, addr, check_mode=False, force=False):
    """
    Get hostnames for specific addr
    """
    return isamAppliance.invoke_get("Retrieving host records for {0}".format(addr),
                                    "/isam/host_records/{0}/hostnames".format(addr))


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
        exists, hostnames_remaining, addr_exists = _check(isamAppliance, addr, hostnames)

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
    Creates a new host record for addr with hostnames
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
        exists, hostnames_remaining, addr_exists = _check(isamAppliance, addr, hostnames)

    if force or exists is False:
        if check_mode is True:
            ret_obj['changed'] = True
        else:
            # Format POST response correctly
            hostnames_post = []
            for entry in hostnames_remaining:
                hostnames_post.append({'name': entry})

            return isamAppliance.invoke_post(
                "Creating new host record",
                "/isam/host_records",
                {
                    'addr': addr,
                    'hostnames': hostnames_post
                })
    return ret_obj


def update(isamAppliance, addr, name, check_mode=False, force=False):
    """
    Update an existing addr with a new hostname

    :param isamAppliance:
    :param addr:          String, addr of host record to update
    :param name:          String, hostname to add to addr
    :return:
    """
    ret_obj = isamAppliance.create_return_object()
    exists = False
    hostnames_remaining = [name]
    addr_exists = True

    if force is False:
        exists, hostnames_remaining, addr_exists = _check(isamAppliance, addr, [name])
        if addr_exists is False:
            raise IBMError("HTTP Return code: 404", "Specified addr does not exist in the hosts file, cannot update.")

    if force or exists is False:
        if check_mode is True:
            ret_obj['changed'] = True
        else:
            return isamAppliance.invoke_post(
                "Update existing host record",
                "/isam/host_records/{0}/hostnames".format(addr),
                {'name': hostnames_remaining[0]}
            )

    return ret_obj


def delete(isamAppliance, addr, name=None, check_mode=False, force=False):
    """

    :param isamAppliance:
    :param addr:          String, addr of host record to update
    :param name:          String, hostname to add to addr
    :param check_mode:
    :param force:
    :return:
    """

    ret_obj = isamAppliance.create_return_object()
    exists = False
    addr_exists = True

    if force is False:
        exists, _, addr_exists = _check(isamAppliance, addr, [name])
        if addr_exists is False:
            ret_obj['changed'] = False
            return ret_obj

    if force or exists is True or name is None:
        if check_mode is True:
            ret_obj['changed'] = True
        else:
            if exists is True:
                # Delete specific entry
                return isamAppliance.invoke_delete(
                    "Update existing host record",
                    "/isam/host_records/{0}/hostnames/{1}".format(addr, name)
                )
            elif exists is False and name is None:
                # Delete all entries for address if no name given
                return isamAppliance.invoke_delete(
                    "Update existing host record",
                    "/isam/host_records/{0}".format(addr)
                )

    return ret_obj


def _check(isamAppliance, addr, hostnames=[]):
    """
    Check addr has all hostnames set
    """
    exists = False
    addr_exists = True

    # Make sure addr exists in host records
    try:
        ret_obj = get(isamAppliance, addr)
    except:
        addr_exists = False
        return exists, hostnames, addr_exists

    if len(hostnames) > 0:
        for entry in ret_obj['data']:
            if entry['name'] in hostnames:
                hostnames.remove(entry['name'])
                logger.debug("Host record exists, continuing checking")

    if len(hostnames) < 1:
        exists = True
        logger.info("All host records exist")
    else:
        logger.info("Not all host records exist")

    return exists, hostnames, addr_exists


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
