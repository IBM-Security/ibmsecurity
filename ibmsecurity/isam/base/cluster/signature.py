import logging

logger = logging.getLogger(__name__)

requires_model="Appliance"

def export(isamAppliance, filename, check_mode=False, force=False):
    """
    Retrieve the cluster signature file
    """
    import os.path

    if force is True or os.path.exists(filename) is False:
        if check_mode is False:  # No point downloading a file if in check_mode
            return isamAppliance.invoke_get_file(
                "Retrieve the cluster signature file",
                "/isam/cluster/signature/v1",
                filename, requires_model=requires_model)

    return isamAppliance.create_return_object()
