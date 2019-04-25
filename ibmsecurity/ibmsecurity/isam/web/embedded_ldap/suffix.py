import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieve existing suffixes.
    """
    return isamAppliance.invoke_get("Retrieving suffixes from embedded ldap",
                                    "/isam/embedded_ldap/suffixes/v1")


def add(isamAppliance, name, check_mode=False, force=False):
    """
    Add a suffix to embedded ldap
    """
    exists = False
    id = None

    if force is False:
        exists, id = _check(isamAppliance, name)

    if force is True or exists is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post(
                "Add suffix to embedded ldap",
                "/isam/embedded_ldap/suffixes/v1",
                {'name': name})

    return isamAppliance.create_return_object()


def delete(isamAppliance, name, check_mode=False, force=False):
    """
    Add a suffix to embedded ldap
    """
    exists = False
    id = None

    if force is False:
        exists, id = _check(isamAppliance, name)

    if force is True or exists is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Delete suffix from embedded ldap",
                "/isam/embedded_ldap/suffixes/{0}/v1".format(id))

    return isamAppliance.create_return_object()


def _check(isamAppliance, name):
    """
    Check if suffix exists
    """
    ret_obj = get(isamAppliance)

    for suffix in ret_obj['data']:
        if suffix['name'] == name:
            logger.info("Suffix found in embedded ldap: " + name)
            return True, suffix['id']

    logger.info("Suffix *not* found in embedded ldap: " + name)
    return False, None


def compare(isamAppliance1, isamAppliance2):
    """
    Compare suffixes in two appliances
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
