import logging

logger = logging.getLogger(__name__)

uri = "/isam/cluster/hvdb"

requires_model="Appliance"

def export(isamAppliance, filename, type='db2', check_mode=False, force=False):
    """
    Export the Runtime database
    """
    import os.path

    if force is True or os.path.exists(filename) is False:
        if check_mode is False:  # No point downloading a file if in check_mode
            return isamAppliance.invoke_get_file("Export the Runtime database", f"{uri}/v1?type={type}",
                                                 filename, requires_model=requires_model)

    return isamAppliance.create_return_object()
