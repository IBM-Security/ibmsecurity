import logging
import os.path
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)
uri = "/isam/authzserver"
requires_modules = None
requires_version = None


def get_all(isamAppliance, id, check_mode=False, force=False):
    """
    Retrieve the log file names of an existing instance

    """
    return isamAppliance.invoke_get("Retrieve the log file names of an existing instance",
                                    "{0}/{1}/logging/v1".format(uri, id),
                                    requires_modules=requires_modules, requires_version=requires_version)


def get(isamAppliance, id, file_id, size=None, start=None, options=None, check_mode=False, force=False):
    """
    Retrieve the log file snippet of an existing instance

    """
    return isamAppliance.invoke_get("Retrieve the log file snippet of an existing instance",
                                    "{0}/{1}/logging/{2}/v1{3}".format(uri, id, file_id,
                                                                       tools.create_query_string(size=size, start=start,
                                                                                                 options=options)),
                                    requires_modules=requires_modules, requires_version=requires_version)


def export_file(isamAppliance, id, file_id, filepath, check_mode=False, force=False):
    """
    Export the log file of an existing instance
    """

    if os.path.exists(filepath) is True:
        logger.info("File '{0}' already exists.  Skipping export.".format(filepath))
        warnings = ["File '{0}' already exists.  Skipping export.".format(filepath)]
        return isamAppliance.create_return_object(warnings=warnings)

    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:
        return isamAppliance.invoke_get_file(
            "Export the log file of an existing instance",
            "{0}/{1}/logging/{2}/v1?export".format(uri, id, file_id), filepath
        )

    return isamAppliance.create_return_object()


def delete(isamAppliance, id, file_id, check_mode=False, force=False):
    """
    Clear the log file of an existing instance
    """

    if force is True or _check(isamAppliance, id, file_id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Clear the log file of an existing instance",
                "{0}/{1}/logging/{2}/v1".format(uri, id, file_id))

    return isamAppliance.create_return_object()


def _check(isamAppliance, id, file_id):
    """
    Check to see if the file_id exists or not
    """
    ret_obj = get_all(isamAppliance, id)

    for obj in ret_obj['data']:
        if obj['id'] == file_id:
            logger.info("Found file_id '{0}'".format(file_id))
            return True

    return False
