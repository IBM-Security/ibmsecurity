import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)
requires_model = "Appliance"

# URI for this module
uri = "/wga/reverseproxy"
requires_model = "Appliance"

def get_all(isamAppliance, instance_id, check_mode=False, force=False):
    """
    Retrieving all trace components and details - Reverse Proxy
    """
    try:
        return isamAppliance.invoke_get("Retrieving all trace components - Reverse Proxy",
                                        "{0}/{1}/tracing".format(uri, instance_id), requires_model=requires_model)
    except:
        # Return empty array - exception thrown if list has no entries or does not exist
        ret_obj = isamAppliance.create_return_object()
        ret_obj['data'] = {}
        return ret_obj


def get_all_logs(isamAppliance, instance_id, component_id, check_mode=False, force=False):
    """
    Retrieving all trace log files for a component - Reverse Proxy
    """
    return isamAppliance.invoke_get("Retrieving all trace log files for a component - Reverse Proxy",
                                    "{0}/{1}/tracing/{2}/trace_files".format(uri,
                                                                             instance_id,
                                                                             component_id),requires_model=requires_model)


def get(isamAppliance, instance_id, component_id, file_id, options=None, size=None, start=None, check_mode=False,
        force=False):
    """
    Retrieving snippet of a trace log file for a component - Reverse Proxy
    """
    return isamAppliance.invoke_get("Retrieving snippet of a trace log file - Reverse Proxy",
                                    "{0}/{1}/tracing/{2}/trace_files/{3}".format(uri,
                                                                                 instance_id,
                                                                                 component_id,
                                                                                 file_id,
                                                                                 tools.create_query_string(
                                                                                     options=options, start=start,
                                                                                     size=size)),requires_model=requires_model)


def export_file(isamAppliance, instance_id, component_id, file_id, filename, check_mode=False, force=False):
    """
    Exporting a trace log file for a component - Reverse Proxy
    """
    import os.path

    if force is True or (os.path.exists(filename) is False):
        if check_mode is False:  # No point downloading a file if in check_mode
            return isamAppliance.invoke_get_file("Exporting a Reverse Proxy trace log file.",
                                                 "{0}/{1}/tracing/{2}/trace_files/{3}?export".format(uri,
                                                                                                     instance_id,
                                                                                                     component_id,
                                                                                                     file_id), filename,requires_model=requires_model)

    return isamAppliance.create_return_object()


def set(isamAppliance, instance_id, component_id, level, flush_interval,
        rollover_size, max_rollover_files, compress, check_mode=False, force=False):
    """
    Modify the trace settings for a component
    """
    warnings = _check(isamAppliance,instance_id)

    if check_mode is True:
        return isamAppliance.create_return_object(changed=True,warnings=warnings)
    else:
        return isamAppliance.invoke_put(
            "Modify trace settings for a component",
            "{0}/{1}/tracing/{2}".format(uri,
                                         instance_id,
                                         component_id),
            {
                'level': level,
                'flush_interval': flush_interval,
                'rollover_size': rollover_size,
                'max_rollover_files': max_rollover_files,
                'compress': compress
            },requires_model=requires_model)


def delete(isamAppliance, instance_id, component_id, file_id, check_mode=False, force=False):
    """
    Deleting a trace log file or rollover file for a component - Reverse Proxy
    """
    warnings = _check(isamAppliance,instance_id)

    if force is False:
        try:
            ret_obj = get(isamAppliance, instance_id, component_id, file_id)
            delete_required = True  # Exception thrown if the file is empty
        except:
            delete_required = False

    if force is True or delete_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True,warnings=warnings)
        else:
            return isamAppliance.invoke_delete(
                "Deleting a trace log file",
                "{0}/{1}/tracing/{2}/trace_files/{3}".format(uri,
                                                             instance_id,
                                                             component_id,
                                                             file_id),requires_model=requires_model)

    return isamAppliance.create_return_object(warnings=warnings)


def delete_all(isamAppliance, instance_id, component_id, check_mode=False, force=False):
    """
    Deleting all trace files and rollover files for a component - Reverse Proxy
    """
    warnings = _check(isamAppliance,instance_id)

    if force is False:
        try:
            ret_obj = get_all_logs(isamAppliance, instance_id, component_id)
            delete_required = True  # Exception thrown if the file is empty
        except:
            delete_required = False

    if force is True or delete_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True,warnings=warnings)
        else:
            return isamAppliance.invoke_delete(
                "Deleting all trace log files",
                "{0}/{1}/tracing/{2}/trace_files".format(uri,
                                                         instance_id,
                                                         component_id),requires_model=requires_model)

    return isamAppliance.create_return_object(warnings=warnings)


def delete_multiple_files(isamAppliance, instance_id, component_id, files, check_mode=False, force=False):
    """
    Deleting multiple trace files for a component
    """
    delete_required = False
    files_to_delete = []

    ret_obj = get_all_logs(isamAppliance, instance_id, component_id)
    check_value,warnings = _check(isamAppliance,instance_id)

    if check_value is True:
        for obj1 in files:
            for obj2 in ret_obj['data']:
                if obj1['name'] == obj2['id']:
                    files_to_delete.append(obj1)
                    delete_required = True

    if force is True or delete_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True,warnings=warnings)
        else:
            if len(files_to_delete) == 1:
                return delete(isamAppliance, instance_id, component_id, files_to_delete[0]['name'])
            else:
                return isamAppliance.invoke_put(
                    "Deleting multiple trace files for a component",
                    "{0}/{1}/tracing/{2}/trace_files/?action=delete".format(uri, instance_id, component_id),
                    {
                        'files': files_to_delete
                    }
                ,requires_model=requires_model)

    return isamAppliance.create_return_object(warnings=warnings)

def _check(isamAppliance,instance_id):
    """
    Check if it's appliance or not
    :param isamAppliance:
    :return: true|false, warnings message
    """
    ret_obj = get_all(isamAppliance,instance_id)
    check_value, warnings=False, ret_obj['warnings']

    if warnings == []:
        check_value = True
        return check_value, warnings
    else:
        return check_value, warnings
