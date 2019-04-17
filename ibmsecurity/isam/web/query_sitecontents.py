import logging
import os.path

from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)
uri = "/wga/query_sitecontents"
requires_modules = ["wga"]
requires_version = None


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieving all query site contents file names
    """
    return isamAppliance.invoke_get("Retrieving all query site contents file names",
                                    "{0}".format(uri),
                                    requires_modules=requires_modules, requires_version=requires_version)


def get(isamAppliance, file_id, check_mode=False, force=False):
    """
    Retrieving the contents of a query site contents file
    """
    return isamAppliance.invoke_get("Retrieving the contents of a query site contents file",
                                    "{0}/{1}".format(uri, file_id),
                                    requires_modules=requires_modules, requires_version=requires_version)


def export_file(isamAppliance, file_id, filename, check_mode=False, force=False):
    """
    Exporting a query site contents file

    """

    if os.path.exists(filename) is True:
        logger.info("File '{0}' already exists.  Skipping export.".format(filename))
        return isamAppliance.create_return_object()

    filefound = False

    ret_obj = get_all(isamAppliance)
    for obj in ret_obj['data']:
        if obj['id'] == file_id:
            filefound = True

    if force is True or filefound is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:

            return isamAppliance.invoke_get_file(
                "Exporting a query site contents file",
                "{0}/{1}?export".format(uri, file_id), filename,
                requires_modules=requires_modules, requires_version=requires_version
            )
    return isamAppliance.create_return_object()
