import logging

logger = logging.getLogger(__name__)

uri = "/mga/template_files"


def export_file(isamAppliance, filename, check_mode=False, force=False):
    """
    Export all Runtime Template Files
    """
    import os.path

    if force is True or os.path.exists(filename) is False:
        if check_mode is False:  # No point downloading a file if in check_mode
            return isamAppliance.invoke_get_file(
                "Export all Runtime Template Files",
                "{0}/?export".format(uri),
                filename)

    return isamAppliance.create_return_object()


def import_file(isamAppliance, filename, check_mode=False, force=False):
    """
    Replace all Runtime Template Files
    """
    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:
        return isamAppliance.invoke_post_files(
            "Replace all Runtime Template Files",
            uri,
            [
                {
                    'file_formfield': 'file',
                    'filename': filename,
                    'mimetype': 'application/octet-stream'
                }
            ],
            {
                "force": force
            })
