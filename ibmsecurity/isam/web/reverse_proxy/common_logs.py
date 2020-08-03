import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/wga/reverseproxy_logging/common"
requires_model = "Appliance"


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the names of all common log files and file sizes
    """
    return isamAppliance.invoke_get("Retrieving the names of all common log files and file sizes",
                                    uri, requires_model=requires_model)


def get(isamAppliance, file_id, options=None, size=None, start=None, check_mode=False, force=False):
    """
    Retrieving a snippet of a common log file
    """
    return isamAppliance.invoke_get("Retrieving a snippet of a common log file",
                                    "{0}/{1}{2}".format(uri, file_id, tools.create_query_string(
                                        options=options, start=start, size=size)), requires_model=requires_model)


def delete(isamAppliance, file_id, check_mode=False, force=False):
    """
    Clearing a common log file
    """
    ret_obj = {'warnings': ''}

    try:
        ret_obj = get(isamAppliance, file_id, start=1, size=1)
        delete_required = True  # Exception thrown if the file is empty

        # Check for Docker
        warnings = ret_obj['warnings']
        if warnings and 'Docker' in warnings[0]:
            return isamAppliance.create_return_object(warnings=ret_obj['warnings'])
    except:
        delete_required = False

    if force is True or delete_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=ret_obj['warnings'])
        else:
            return isamAppliance.invoke_delete(
                "Clearing a common log file",
                "{0}/{1}".format(uri, file_id), requires_model=requires_model)

    return isamAppliance.create_return_object(warnings=ret_obj['warnings'])


def export_file(isamAppliance, file_id, filename, check_mode=False, force=False):
    """
    Exporting a common log file
    """
    import os.path
    ret_obj = {'warnings': ''}

    if force is True or (os.path.exists(filename) is False):
        if check_mode is False:  # No point downloading a file if in check_mode
            return isamAppliance.invoke_get_file(
                "Exporting a common log file",
                "{0}/{1}?export".format(uri, file_id),
                filename, requires_model=requires_model)

    return isamAppliance.create_return_object(warnings=ret_obj['warnings'])
