import logging
import os.path

from ibmsecurity.utilities.tools import json_sort

logger = logging.getLogger(__name__)
uri = "/wga/reverseproxy"
requires_modules = "wga"
requires_version = None
requires_model = "Appliance"

def get(isamAppliance, instance_id, check_mode=False, force=False):
    """
    Retrieving all transaction logging components and their details

    """
    return isamAppliance.invoke_get("Retrieving all transaction logging components and their details",
                                    "{0}/{1}/transaction_logging".format(uri, instance_id),
                                    requires_modules=requires_modules, requires_version=requires_version,requires_model=requires_model)


def get_files(isamAppliance, instance_id, component_id, check_mode=False, force=False):
    """
    Retrieving all transaction log files for a component

    """
    return isamAppliance.invoke_get("Retrieving all transaction log files for a component",
                                    "{0}/{1}/transaction_logging/{2}/translog_files".format(uri, instance_id,
                                                                                            component_id),
                                    requires_modules=requires_modules, requires_version=requires_version,requires_model=requires_model)


def export_file(isamAppliance, instance_id, component_id, file_id, filepath, check_mode=False, force=False):
    """
    Exporting the transaction logging data file or rollover transaction logging data file for a component
    """

    if os.path.exists(filepath) is True:
        logger.info("File '{0}' already exists.  Skipping export.".format(filepath))
        warnings = ["File '{0}' already exists.  Skipping export.".format(filepath)]
        return isamAppliance.create_return_object(warnings=warnings)

    warnings = _check(isamAppliance,instance_id,component_id)

    if check_mode is True:
        return isamAppliance.create_return_object(changed=True,warnings=warnings)
    else:
        return isamAppliance.invoke_get_file(
            "Exporting the transaction logging data file or rollover transaction logging data file for a component",
            "{0}/{1}/transaction_logging/{2}/translog_files/{3}?export".format(uri, instance_id, component_id, file_id),
            filepath
        ,requires_model=requires_model)

    return isamAppliance.create_return_object(warnings=warnings)


def update(isamAppliance, instance_id, component_id, status, rollover_size, max_rollover_files, compress,
           check_mode=False, force=False):
    """
    Modifying the status and rollover size for a component

    """

    check_value,warnings = _check_update(isamAppliance, instance_id=instance_id, component_id=component_id, status=status,
                                         rollover_size=rollover_size, max_rollover_files=max_rollover_files,
                                         compress=compress)

    if force is True or check_value is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True,warnings=warnings)
        else:

            return isamAppliance.invoke_put(
                "Modifying the status and rollover size for a component",
                "{0}/{1}/transaction_logging/{2}".format(uri, instance_id, component_id),
                {
                    'id': component_id,
                    'status': status,
                    'rollover_size': rollover_size,
                    'max_rollover_files': max_rollover_files,
                    'compress': compress
                },
                requires_modules=requires_modules, requires_version=requires_version,requires_model=requires_model
            )

    return isamAppliance.create_return_object(warnings=warnings)


def rollover(isamAppliance, instance_id, component_id, check_mode=False, force=False):
    """
    Rolling over the transaction logging data file for a component

    """
    check_value, warnings = _check_enabled(isamAppliance, instance_id, component_id)

    if force is True or check_value is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True,warnings=warnings)
        else:
            return isamAppliance.invoke_put(
                "Rolling over the transaction logging data file for a component",
                "{0}/{1}/transaction_logging/{2}".format(uri, instance_id, component_id),
                {
                    'rollover': "yes"
                },
                requires_modules=requires_modules, requires_version=requires_version,requires_model=requires_model
            )

    return isamAppliance.create_return_object(warnings=warnings)


def delete_unused(isamAppliance, instance_id, component_id, check_mode=False, force=False):
    """
    Deleting the unused transaction logging data file and rollover files for a component
    """

    ret_obj = get_files(isamAppliance, instance_id=instance_id, component_id=component_id)

    if force is True or ret_obj['data'] != []:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Deleting the unused transaction logging data file and rollover files for a component",
                "{0}/{1}/transaction_logging/{2}/translog_files".format(uri, instance_id, component_id),requires_model=requires_model)

    return isamAppliance.create_return_object()


def delete(isamAppliance, instance_id, component_id, file_id, check_mode=False, force=False):
    """
    Deleting the transaction logging data file or rollover file for a component
    """
    check_value,warnings = _check_file(isamAppliance, instance_id, component_id, file_id)

    if force is True or check_value is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True,warnings=warnings)
        else:
            return isamAppliance.invoke_delete(
                "Deleting the transaction logging data file or rollover file for a component",
                "{0}/{1}/transaction_logging/{2}/translog_files/{3}".format(uri, instance_id, component_id, file_id),requires_model=requires_model)

    return isamAppliance.create_return_object(warnings=warnings)


def delete_multiple_files(isamAppliance, instance_id, component_id, files, check_mode=False, force=False):
    """
    Deleting multiple transaction logging data file and rollover files for a component
    """
    delete_required = False
    files_to_delete = []

    check_value, warnings = _check(isamAppliance,instance_id,component_id)

    if warnings == []:
        ret_obj = get_files(isamAppliance, instance_id, component_id)

        for obj1 in files:
            for obj2 in ret_obj['data']:
                if obj1['name'] == obj2['id']:
                    files_to_delete.append(obj1)
                    delete_required = True

        if len(files_to_delete) == 1:
            return delete(isamAppliance, instance_id, component_id, files_to_delete[0]['name'])

        if force is True or delete_required is True:
            if check_mode is True:
                return isamAppliance.create_return_object(changed=True)
            else:
                return isamAppliance.invoke_put(
                    "Deleting multiple transaction logging data file and rollover files for a component",
                    "{0}/{1}/transaction_logging/{2}/translog_files?action=delete".format(uri, instance_id, component_id),
                    {
                        'files': files
                    },requires_model=requires_model
                    )

    return isamAppliance.create_return_object(warnings=warnings)


def _check_update(isamAppliance, instance_id, component_id, status, rollover_size, max_rollover_files, compress):
    """
    Check to see if the file_id exists or not
    """
    ret_obj = get(isamAppliance, instance_id)
    warnings = ret_obj['warnings']
    new_obj = {
        'id': component_id,
        'status': status,
        'rollover_size': rollover_size,
        'max_rollover_files': max_rollover_files,
        'compress': compress
    }

    sorted_new_obj = json_sort(new_obj)

    for obj in ret_obj['data']:
        if obj['id'] == component_id:
            if obj['status'] == "Off" and status == "Off":
                return True,warnings
            else:
                del obj['file_size']
                sorted_obj = json_sort(obj)
                if sorted_obj == sorted_new_obj:
                    return True,warnings

    return False,warnings


def _check_file(isamAppliance, instance_id, component_id, file_id):
    """
    Check to see if the file_id exists or not
    """
    ret_obj = get_files(isamAppliance, instance_id, component_id)
    warnings = ret_obj['warnings']

    for obj in ret_obj['data']:
        if obj['id'] == file_id:
            return True,warnings

    return False,warnings


def _check(isamAppliance, instance_id, component_id):
    """
    Check to see if the component_id exists or not
    """
    ret_obj = get(isamAppliance, instance_id)
    warnings = ret_obj['warnings']
    if warnings == []:
        for obj in ret_obj['data']:
            if obj['id'] == component_id:
                return True,warnings

    return False,warnings


def _check_enabled(isamAppliance, instance_id, component_id):
    """
    Check to see if the component is enabled or not
    """
    ret_obj = get(isamAppliance, instance_id)
    warnings = ret_obj['warnings']

    for obj in ret_obj['data']:
        if obj['id'] == component_id and obj['status'] == "On":
            return True,warnings

    return False,warnings
