import logging
import os.path
from ibmsecurity.utilities import tools
from ibmsecurity.utilities.tools import json_sort

logger = logging.getLogger(__name__)
uri = "/isam/authzserver"
requires_modules = None
requires_version = None
requires_model = "Appliance"


def get_all(isamAppliance, id, check_mode=False, force=False):
    """
    Retrieve the trace components and settings of an existing instance

    """
    return isamAppliance.invoke_get("Retrieve the trace components and settings of an existing instance",
                                    "{0}/{1}/tracing/v1".format(uri, id),
                                    requires_modules=requires_modules, requires_version=requires_version,
                                    requires_model=requires_model)


def get_list(isamAppliance, id, trace_id, check_mode=False, force=False):
    """
    List trace files for a trace component

    """
    return isamAppliance.invoke_get("List trace files for a trace component",
                                    "{0}/{1}/tracing/{2}/trace_files/v1".format(uri, id, trace_id),
                                    requires_modules=requires_modules, requires_version=requires_version,
                                    requires_model=requires_model)


def get(isamAppliance, id, trace_id, trace_file_id, size=None, start=None, options=None, check_mode=False, force=False):
    """
    Retrieve the trace file snippet for a trace component

    """
    return isamAppliance.invoke_get("Retrieve the trace file snippet for a trace component",
                                    "{0}/{1}/tracing/{2}/trace_files/{3}/v1{4}".format(uri, id, trace_id, trace_file_id,
                                                                                       tools.create_query_string(
                                                                                           size=size, start=start,
                                                                                           options=options)),
                                    requires_modules=requires_modules, requires_version=requires_version,
                                    requires_model=requires_model)


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
            "{0}/{1}/tracing/{2}/trace_files/{3}/v1?export".format(uri, id, trace_id, trace_file_id),
            filepath, requires_model=requires_model)


def update(isamAppliance, id, trace_id, level, flush_interval, rollover_size, max_rollover_files, compress,
           check_mode=False, force=False):
    """
    Update the settings for a trace component
    """
    id_exists, warnings = _check_id(isamAppliance, id, trace_id, level, flush_interval,
                                    rollover_size, max_rollover_files, compress)

    if not warnings:
        if force is True or id_exists is False:
            if check_mode is True:
                return isamAppliance.create_return_object(changed=True, warnings=warnings)
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
                    },
                    requires_model=requires_model
                )

    return isamAppliance.create_return_object(warnings=warnings)


def delete(isamAppliance, id, trace_id, trace_file_id, check_mode=False, force=False):
    """
    Delete Trace File for a trace component
    """

    id_exists, warnings = _check(isamAppliance, id, trace_id, trace_file_id)

    if not warnings:
        if force is True or id_exists is True:
            if check_mode is True:
                return isamAppliance.create_return_object(changed=True, warnings=warnings)
            else:
                return isamAppliance.invoke_delete(
                    "Delete Trace File for a trace component",
                    "{0}/{1}/tracing/{2}/trace_files/{3}/v1".format(uri, id, trace_id, trace_file_id),
                    requires_model=requires_model)

    return isamAppliance.create_return_object(warnings=warnings)


def _check_id(isamAppliance, id, trace_id, level, flush_interval, rollover_size, max_rollover_files, compress):
    """
    Check to see if the file_id exists or not
    """
    ret_obj = get_all(isamAppliance, id)
    id_exists, warnings = False, ret_obj['warnings']

    new_obj = {
        'id': trace_id,
        'level': level,
        'flush_interval': flush_interval,
        'rollover_size': rollover_size,
        'max_rollover_files': max_rollover_files,
        'compress': compress
    }

    sorted_new_obj = json_sort(new_obj)

    if not warnings:
        for obj in ret_obj['data']:
            del obj['file_size']
            sorted_obj = json_sort(obj)
            if sorted_obj == sorted_new_obj:
                id_exists = True

    return id_exists, warnings


def _check(isamAppliance, id, trace_id, trace_file_id):
    """
    Check to see if the file_id exists or not
    """
    ret_obj = get_all(isamAppliance, id)
    id_exists, warnings = False, ret_obj['warnings']

    if not warnings:
        for obj in ret_obj['data']:
            if obj['id'] == trace_id:
                filelist = get_list(isamAppliance, id, trace_id)
                for list_obj in filelist['data']:
                    if list_obj['id'] == trace_file_id:
                        logger.info("Found trace_id {0} trace_file_id '{1}'".format(trace_id, trace_file_id))
                        id_exists = True

    return id_exists, warnings
