import logging

logger = logging.getLogger(__name__)
requires_model = "Appliance"

requires_model = "Appliance"


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieve the cluster manager log file names
    """
    return isamAppliance.invoke_get("Retrieve the cluster manager log file names",
                                    "/isam/cluster/logging/v1", requires_model=requires_model)


def get(isamAppliance, file_id, size=100, start=None, options=None, check_mode=False, force=False):
    """
    Retrieve a log file snippet
    """
    return isamAppliance.invoke_get("Retrieve a log file snippet",
                                    f"/isam/cluster/logging/{file_id}/v1", requires_model=requires_model)


def _check(isamAppliance, file_id):
    check_obj = {'vale': False, 'warnings': ""}

    ret_obj = get(isamAppliance, file_id)

    file_exists, warnings = False, ret_obj['warnings']

    if warnings ==[] and ret_obj['data']['contents'] != '':
        file_exists = True
    return file_exists, warnings


def delete(isamAppliance, file_id, check_mode=False, force=False):
    """
    Clear a log file
    """
    file_exists, warnings = _check(isamAppliance, file_id)

    if force is True or file_exists is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_delete(
                "Clear a log file",
                f"/isam/cluster/logging/{file_id}/v1", requires_model=requires_model)

    return isamAppliance.create_return_object(warnings=warnings)


def export_file(isamAppliance, file_id, filename, check_mode=False, force=False):
    """
    Export a cluster manager log file
    """
    import os.path

    if force is True or os.path.exists(filename) is False:
        if check_mode is False:  # No point downloading a file if in check_mode
            return isamAppliance.invoke_get_file(
                "Export a cluster manager log file",
                f"/isam/cluster/logging/{file_id}/v1?export",
                filename, requires_model=requires_model)

    return isamAppliance.create_return_object()
