import logging
import ibmsecurity.utilities.tools
import os.path

logger = logging.getLogger(__name__)

uri = "/isam/runtime_components"
requires_modules = ["wga"]
requires_version = "10.0.4"


def export_configuration_bundle(isamAppliance, filename="rte_config.zip",  check_mode=False, force=False):
    """
    Exporting the Runtime Environment configuration
        -filename is file system location to export the file (e.g. /tmp/rte_config.zip)
    """
    import os.path
    if force is True or os.path.exists(os.path.dirname(filename)) is False:
        if check_mode is True: # No point downloading a file if in check_mode
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_get_file(
                description="Exporting the Runtime Environment configuration",
                uri="{0}?action=export".format(uri),
                filename=filename,
                requires_version=requires_version)

    return isamAppliance.create_return_object()



