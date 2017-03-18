import logging
import ibmsecurity.utilities.tools
import os.path

logger = logging.getLogger(__name__)


def get(isamAppliance, resource_id, check_mode=False, force=False):
    """
    Retrieving a runtime configuration file
    """
    return isamAppliance.invoke_get("Retrieving a runtime configuration file",
                                    "/isam/advanced_configuration/{0}".format(resource_id))


def export_file(isamAppliance, resource_id, filename, check_mode=False, force=False):
    """
    Exporting a runtime configuration file
    """
    if force is True or os.path.exists(filename) is False:
        if check_mode is False:
            return isamAppliance.invoke_get_file(
                "Exporting a runtime configuration file",
                "/isam/advanced_configuration/{0}?export".format(resource_id), filename)

    return isamAppliance.create_return_object()


def revert(isamAppliance, resource_id, check_mode=False, force=False):
    """
    Reverting a previously updated runtime configuration file
    """
    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:
        return isamAppliance.invoke_put(
            "Reverting a previously updated runtime configuration file",
            "/isam/advanced_configuration/{0}".format(resource_id),
            {
                'operation': 'revert'
            })


def update(isamAppliance, resource_id, file_contents, check_mode=False, force=False):
    """
    Updating a runtime configuration file
    """
    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:
        return isamAppliance.invoke_put(
            "Updating a runtime configuration file",
            "/isam/advanced_configuration/{0}".format(resource_id),
            {
                'file_contents': file_contents
            })


def compare(isamAppliance1, isamAppliance2, resource_id):
    """
    Compare stanzas within resource between two appliances
    """
    ret_obj1 = get(isamAppliance1, resource_id)
    ret_obj2 = get(isamAppliance2, resource_id)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1=ret_obj1, ret_obj2=ret_obj2, deleted_keys=[])
