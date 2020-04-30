import logging

logger = logging.getLogger(__name__)


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieve the cluster manager log file names
    """
    return isamAppliance.invoke_get("Retrieve the cluster manager log file names",
                                    "/isam/cluster/logging/v1")


def get(isamAppliance, file_id, size=100, start=None, options=None, check_mode=False, force=False):
    """
    Retrieve a log file snippet
    """
    return isamAppliance.invoke_get("Retrieve a log file snippet",
                                    "/isam/cluster/logging/{0}/v1".format(file_id))


def _check(isamAppliance, file_id):
    ret_obj = get(isamAppliance, file_id)

    if ret_obj['data']['contents'] == '':
        return False
    else:
        return True


def delete(isamAppliance, file_id, check_mode=False, force=False):
    """
    Clear a log file
    """
    if force is True or _check(isamAppliance, file_id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Clear a log file",
                "/isam/cluster/logging/{0}/v1".format(file_id))

    return isamAppliance.create_return_object()


def export_file(isamAppliance, file_id, filename, check_mode=False, force=False):
    """
    Export a cluster manager log file
    """
    import os.path

    if force is True or os.path.exists(filename) is False:
        if check_mode is False:  # No point downloading a file if in check_mode
            return isamAppliance.invoke_get_file(
                "Export a cluster manager log file",
                "/isam/cluster/logging/{0}/v1?export".format(file_id),
                filename)

    return isamAppliance.create_return_object()
