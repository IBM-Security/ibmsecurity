import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)

requires_model = "Appliance"


def get(isamAppliance, check_mode=False, force=False, ignore_error=False):
    """
    Retrieving a list of firmware settings
    """
    return isamAppliance.invoke_get("Retrieving a list of firmware settings",
                                    "/firmware_settings", ignore_error=ignore_error, requires_model=requires_model)


def backup(isamAppliance, check_mode=False, force=False):
    """
    Creating a backup of the active partition
    """
    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:
        return isamAppliance.invoke_put("Creating a backup of the active partition",
                                        "/firmware_settings/kickoff_backup", {}, requires_model=requires_model)


def swap(isamAppliance, check_mode=False, force=False):
    """
    Swapping the active partition
    """
    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:
        ret_obj_old = get(isamAppliance)

        ret_obj = isamAppliance.invoke_put("Swapping the active partition",
                                           "/firmware_settings/kickoff_swap", {}, requires_model=requires_model)
        # Process previous query after a successful call to swap the partition
        for partition in ret_obj_old['data']:
            if partition['active'] is False:  # Get version of inactive partition (active now!)
                ver = partition['firmware_version'].split(' ')
                isamAppliance.facts['version'] = ver[-1]

        return ret_obj


def set(isamAppliance, id, comment, check_mode=False, force=False):
    """
    Updating a comment for a partition
    """

    check_value, warnings = _check_comment(isamAppliance, comment)
    if force is True or check_value is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_put("Updating a comment for a partition",
                                            "/firmware_settings/{0}".format(id),
                                            {'comment': comment}, requires_model=requires_model)

    return isamAppliance.create_return_object(warnings=warnings)


def _check_comment(isamAppliance, comment):
    ret_obj = get(isamAppliance)
    warnings = ret_obj['warnings']

    # Loop through firmware partitions looking for active one
    for partition in ret_obj['data']:
        if partition['active'] is True:
            return (partition['comment'] == comment), warnings

    return False, warnings


def compare(isamAppliance1, isamAppliance2):
    """
    Compare firmware between two appliances
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    for obj in ret_obj1['data']:
        del obj['install_date']
        del obj['backup_date']
        del obj['last_boot']
    for obj in ret_obj2['data']:
        del obj['install_date']
        del obj['backup_date']
        del obj['last_boot']

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2,
                                                    deleted_keys=['install_date', 'backup_date', 'last_boot'])
