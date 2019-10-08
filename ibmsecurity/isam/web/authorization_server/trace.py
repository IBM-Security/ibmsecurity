import logging
import os.path
from ibmsecurity.utilities import tools
from ibmsecurity.utilities.tools import json_sort

logger = logging.getLogger(__name__)
uri = "/isam/authzserver"
requires_modules = None
requires_version = None


def get_all(isamAppliance, id, check_mode=False, force=False):
    """
    Retrieve the trace components and settings of an existing instance

    """
    return isamAppliance.invoke_get("Retrieve the trace components and settings of an existing instance",
                                    "{0}/{1}/tracing/v1".format(uri, id),
                                    requires_modules=requires_modules, requires_version=requires_version)


def get_list(isamAppliance, id, trace_id, check_mode=False, force=False):
    """
    List trace files for a trace component

    """
    return isamAppliance.invoke_get("List trace files for a trace component",
                                    "{0}/{1}/tracing/{2}/trace_files/v1".format(uri, id, trace_id),
                                    requires_modules=requires_modules, requires_version=requires_version)


def get(isamAppliance, id, trace_id, trace_file_id, size=None, start=None, options=None, check_mode=False, force=False):
    """
    Retrieve the trace file snippet for a trace component

    """
    return isamAppliance.invoke_get("Retrieve the trace file snippet for a trace component",
                                    "{0}/{1}/tracing/{2}/trace_files/{3}/v1{4}".format(uri, id, trace_id, trace_file_id,
                                                                                       tools.create_query_string(
                                                                                           size=size, start=start,
                                                                                           options=options)),
                                    requires_modules=requires_modules, requires_version=requires_version)


def export_file(isamAppliance, id, trace_id, trace_file_id, filepath, check_mode=False, force=False):
    """
    Export the trace file for a trace component
    """

    if os.path.exists(filepath) is True:
        logger.info("File '{0}' already exists.  Skipping export.".format(filepath))
        warnings = ["File '{0}' already exists.  Skipping export.".format(filepath)]
        return isamAppliance.create_return_object(warnings=warnings)

    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:
        return isamAppliance.invoke_get_file(
            "Export the trace file for a trace component",
            "{0}/{1}/tracing/{2}/trace_files/{3}/v1?export".format(uri, id, trace_id, trace_file_id), filepath
        )

    return isamAppliance.create_return_object()


def update(isamAppliance, id, trace_id, level, flush_interval, rollover_size, max_rollover_files, compress,
           check_mode=False, force=False):
    """
    Update the settings for a trace component
    """

    if force is True or _check_id(isamAppliance, id, trace_id, level, flush_interval, rollover_size, max_rollover_files,
                                  compress) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Update the settings for a trace component",
                "{0}/{1}/tracing/{2}/v1".format(uri, id, trace_id),
                {
                    'level': level,
                    'flush_interval': flush_interval,
                    'rollover_size': rollover_size,
                    'max_rollover_files': max_rollover_files,
                    'compress': compress
                }
            )

    return isamAppliance.create_return_object()


def delete(isamAppliance, id, trace_id, trace_file_id, check_mode=False, force=False):
    """
    Delete Trace File for a trace component
    """

    if force is True or _check(isamAppliance, id, trace_id, trace_file_id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Delete Trace File for a trace component",
                "{0}/{1}/tracing/{2}/trace_files/{3}/v1".format(uri, id, trace_id, trace_file_id))

    return isamAppliance.create_return_object()


def _check_id(isamAppliance, id, trace_id, level, flush_interval, rollover_size, max_rollover_files, compress):
    """
    Check to see if the file_id exists or not
    """
    ret_obj = get_all(isamAppliance, id)
    new_obj = {
        'id': trace_id,
        'level': level,
        'flush_interval': flush_interval,
        'rollover_size': rollover_size,
        'max_rollover_files': max_rollover_files,
        'compress': compress
    }

    sorted_new_obj = json_sort(new_obj)
    for obj in ret_obj['data']:
        del obj['file_size']
        sorted_obj = json_sort(obj)
        if sorted_obj == sorted_new_obj:
            return True

    return False


def _check(isamAppliance, id, trace_id, trace_file_id):
    """
    Check to see if the file_id exists or not
    """
    ret_obj = get_all(isamAppliance, id)

    for obj in ret_obj['data']:
        if obj['id'] == trace_id:
            filelist = get_list(isamAppliance, id, trace_id)
            for list_obj in filelist['data']:
                if list_obj['id'] == trace_file_id:
                    logger.info("Found trace_id {0} trace_file_id '{1}'".format(trace_id, trace_file_id))
                    return True

    return False
