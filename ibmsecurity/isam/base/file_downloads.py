import logging

logger = logging.getLogger(__name__)


def get(isamAppliance, file_path='/', recursive=True, check_mode=False, force=False):
    """
    Retrieving the contents of a directory from the file downloads area
    """
    return isamAppliance.invoke_get("Retrieving the contents of a directory from the file downloads area",
                                    f"/isam/downloads/{file_path}/?recursive={recursive}")


def export_file(isamAppliance, file_path, filename, check_mode=False, force=False):
    """
    Downloading a file from the file downloads area
    """
    import os.path

    if force is True or os.path.exists(filename) is False:
        if check_mode is False:  # No point downloading a file if in check_mode
            # NOTE: this call requires no headers
            return isamAppliance.invoke_get_file(
                "Downloading a file from the file downloads area",
                f"/isam/downloads/{file_path}?type=File&browser=&",
                filename, True)

    return isamAppliance.create_return_object()
