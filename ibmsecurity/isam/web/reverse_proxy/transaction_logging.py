import logging
import os.path

from ibmsecurity.utilities.tools import json_sort

logger = logging.getLogger(__name__)
uri = "/wga/reverseproxy"
requires_modules = "wga"
requires_version = None


def get(isamAppliance, instance_id, check_mode=False, force=False):
    """
    Retrieving all transaction logging components and their details

    """
    return isamAppliance.invoke_get("Retrieving all transaction logging components and their details",
                                    "{0}/{1}/transaction_logging".format(uri, instance_id),
                                    requires_modules=requires_modules, requires_version=requires_version)


def get_files(isamAppliance, instance_id, component_id, check_mode=False, force=False):
    """
    Retrieving all transaction log files for a component

    """
    return isamAppliance.invoke_get("Retrieving all transaction log files for a component",
                                    "{0}/{1}/transaction_logging/{2}/translog_files".format(uri, instance_id,
                                                                                            component_id),
                                    requires_modules=requires_modules, requires_version=requires_version)


def export_file(isamAppliance, instance_id, component_id, file_id, filepath, check_mode=False, force=False):
    """
    Exporting the transaction logging data file or rollover transaction logging data file for a component
    """

    if os.path.exists(filepath) is True:
        logger.info("File '{0}' already exists.  Skipping export.".format(filepath))
        warnings = ["File '{0}' already exists.  Skipping export.".format(filepath)]
        return isamAppliance.create_return_object(warnings=warnings)

    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:
        return isamAppliance.invoke_get_file(
            "Exporting the transaction logging data file or rollover transaction logging data file for a component",
            "{0}/{1}/transaction_logging/{2}/translog_files/{3}?export".format(uri, instance_id, component_id, file_id),
            filepath
        )

    return isamAppliance.create_return_object()


def update(isamAppliance, instance_id, component_id, status, rollover_size, max_rollover_files, compress,
           check_mode=False, force=False):
    """
    Modifying the status and rollover size for a component

    """

    if force is True or _check_update(isamAppliance, instance_id=instance_id, component_id=component_id, status=status,
                                      rollover_size=rollover_size, max_rollover_files=max_rollover_files,
                                      compress=compress) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
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
                requires_modules=requires_modules, requires_version=requires_version
            )

    return isamAppliance.create_return_object()


def rollover(isamAppliance, instance_id, component_id, check_mode=False, force=False):
    """
    Rolling over the transaction logging data file for a component

    """
    if force is True or _check_enabled(isamAppliance, instance_id, component_id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Rolling over the transaction logging data file for a component",
                "{0}/{1}/transaction_logging/{2}".format(uri, instance_id, component_id),
                {
                    'rollover': "yes"
                },
                requires_modules=requires_modules, requires_version=requires_version
            )

    return isamAppliance.create_return_object()


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
                "{0}/{1}/transaction_logging/{2}/translog_files".format(uri, instance_id, component_id))

    return isamAppliance.create_return_object()


def delete(isamAppliance, instance_id, component_id, file_id, check_mode=False, force=False):
    """
    Deleting the transaction logging data file or rollover file for a component
    """

    if force is True or _check_file(isamAppliance, instance_id, component_id, file_id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Deleting the transaction logging data file or rollover file for a component",
                "{0}/{1}/transaction_logging/{2}/translog_files/{3}".format(uri, instance_id, component_id, file_id))

    return isamAppliance.create_return_object()


def delete_multiple_files(isamAppliance, instance_id, component_id, files, check_mode=False, force=False):
    """
    Deleting multiple transaction logging data file and rollover files for a component
    """
    delete_required = False
    files_to_delete = []

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
                }
            )

    return isamAppliance.create_return_object()


def _check_update(isamAppliance, instance_id, component_id, status, rollover_size, max_rollover_files, compress):
    """
    Check to see if the file_id exists or not
    """
    ret_obj = get(isamAppliance, instance_id)
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
                return True
            else:
                del obj['file_size']
                sorted_obj = json_sort(obj)
                if sorted_obj == sorted_new_obj:
                    return True

    return False


def _check_file(isamAppliance, instance_id, component_id, file_id):
    """
    Check to see if the file_id exists or not
    """
    ret_obj = get_files(isamAppliance, instance_id, component_id)

    for obj in ret_obj['data']:
        if obj['id'] == file_id:
            return True

    return False


def _check(isamAppliance, instance_id, component_id):
    """
    Check to see if the component_id exists or not
    """
    ret_obj = get(isamAppliance, instance_id)

    for obj in ret_obj['data']:
        if obj['id'] == component_id:
            return True

    return False


def _check_enabled(isamAppliance, instance_id, component_id):
    """
    Check to see if the component is enabled or not
    """
    ret_obj = get(isamAppliance, instance_id)

    for obj in ret_obj['data']:
        if obj['id'] == component_id and obj['status'] == "On":
            return True

    return False
