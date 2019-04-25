import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get(isamAppliance, directory_name, check_mode=False, force=False):
    """
    Retrieving the list of suffixes for a particular federated directory
    """
    return isamAppliance.invoke_get("Retrieving the list of suffixes for a particular federated directory",
                                    "/isam/runtime_components/federated_directories/{0}/suffix/v1".format(
                                        directory_name))


def add(isamAppliance, directory_name, suffix, use_ssl=False, client_cert_label=None,
        check_mode=False,
        force=False):
    """
    Create a new suffix in a particular federated directory
    """
    if force is True or _check(isamAppliance, directory_name, suffix) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post(
                "Create a new suffix in a particular federated directory",
                "/isam/runtime_components/federated_directories/{0}/suffix/v1".format(directory_name),
                {
                    'suffix': suffix
                })

    return isamAppliance.create_return_object()


def delete(isamAppliance, directory_name, suffix_name, check_mode=False, force=False):
    """
    Remove an existing suffix from a federated directory
    """
    if force is True or _check(isamAppliance, directory_name, suffix_name) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Remove an existing suffix from a federated directory",
                "/isam/runtime_components/federated_directories/{0}/suffix/{1}/v1".format(directory_name, suffix_name))

    return isamAppliance.create_return_object()


def _check(isamAppliance, directory_name, suffix):
    """
    Check if federated directory suffix exists - will return true if any match is found

    :param isamAppliance:
    :param directory_name:
    :param suffix:
    :return:
    """
    ret_obj = get(isamAppliance, directory_name)

    for suffix_obj in ret_obj['data']:
        if isinstance(suffix, list):  # Add passes a list
            for new_suffix in suffix:
                if new_suffix['id'] == suffix_obj['id']:
                    return True
        else:  # Update passes just suffix_name
            if suffix_obj['id'] == suffix:
                return True

    return False


def compare(isamAppliance1, isamAppliance2, directory_name):
    """
    Compare snmp objects between two appliances
    """
    ret_obj1 = get(isamAppliance1, directory_name)
    ret_obj2 = get(isamAppliance2, directory_name)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
