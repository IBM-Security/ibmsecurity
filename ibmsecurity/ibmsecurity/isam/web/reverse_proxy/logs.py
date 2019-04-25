import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/wga/reverseproxy_logging/instance"


def get_all(isamAppliance, instance_id, check_mode=False, force=False):
    """
    Retrieving the names of all common log files and file sizes
    """
    return isamAppliance.invoke_get("Retrieving the names of all common log files and file sizes",
                                    "{0}/{1}".format(uri, instance_id))


def get(isamAppliance, instance_id, file_id, options=None, size=None, start=None, check_mode=False, force=False):
    """
    Retrieving a snippet of a common log file
    """
    return isamAppliance.invoke_get("Retrieving a snippet of a common log file",
                                    "{0}/{1}/{2}{3}".format(uri, instance_id, file_id, tools.create_query_string(
                                        options=options, start=start, size=size)))


def delete(isamAppliance, instance_id, file_id, check_mode=False, force=False):
    """
    Clearing a common log file
    """
    if force is False:
        try:
            ret_obj = get(isamAppliance, instance_id, file_id, start=1, size=1)
            delete_required = True  # Exception thrown if the file is empty
        except:
            delete_required = False

    if force is True or delete_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Clearing a common log file",
                "{0}/{1}/{2}".format(uri, instance_id, file_id))

    return isamAppliance.create_return_object()


def export_file(isamAppliance, instance_id, file_id, filename, check_mode=False, force=False):
    """
    Exporting a common log file
    """
    import os.path

    if force is True or (os.path.exists(filename) is False):
        if check_mode is False:  # No point downloading a file if in check_mode
            return isamAppliance.invoke_get_file(
                "Exporting a common log file",
                "{0}/{1}/{2}?export=true".format(uri, instance_id, file_id),
                filename)

    return isamAppliance.create_return_object()
