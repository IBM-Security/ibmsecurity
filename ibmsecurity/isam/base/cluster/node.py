import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get_all(isamAppliance, check_mode=False, force=False):
    """
    List the current nodes in the cluster
    """
    return isamAppliance.invoke_get("List the current nodes in the cluster",
                                    "/isam/cluster/nodes/v1")


def get_id(isamAppliance, check_mode=False, force=False):
    """
    Retrieve the cluster identifier
    """
    return isamAppliance.invoke_get("Retrieve the cluster identifier",
                                    "/isam/cluster/id/v2")


def get_master(isamAppliance, check_mode=False, force=False):
    """
    Check if the node is the primary master
    """
    return isamAppliance.invoke_get("Check if the node is the primary master",
                                    "/isam/cluster/ismaster/v2")


def add(isamAppliance, signature_file, restricted=False, check_mode=False, force=False):
    """
    Add a node to the cluster
    """
    id = None
    if force is False:
        ret_obj = get_id(isamAppliance)
        id = ret_obj['data']['value']

    if force is True or _check(isamAppliance, id) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post_files(
                "Add a node to the cluster",
                "/isam/cluster/nodes/v1",
                [
                    {
                        'file_formfield': 'signature_file',
                        'filename': signature_file,
                        'mimetype': 'application/octet-stream'
                    }
                ],
                {'restricted': restricted})

    return isamAppliance.create_return_object()


def _check(isamAppliance, id):
    ret_obj = get_all(isamAppliance)

    for node in ret_obj['data']:
        if node['value'] == id:
            return True

    return False


def delete(isamAppliance, id, check_mode=False, force=False):
    """
    Remove a node from the cluster
    """
    if force is True or _check(isamAppliance, id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Remove a node from the cluster",
                "/isam/cluster/nodes/{0}/v1".format(id))

    return isamAppliance.create_return_object()


def compare(isamAppliance1, isamAppliance2):
    """
    Compare cluster nodes between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
