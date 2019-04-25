import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get(isdsAppliance, check_mode=False, force=False):
    """
    Retrieve existing firmware.
    """
    return isdsAppliance.invoke_get("Retrieving firmware",
                                    "/firmware_settings")


def backup(isdsAppliance, check_mode=False, force=False):
    """
    Kickoff Backup of active partition
    """
    if check_mode is True:
        return isdsAppliance.create_return_object(changed=True)
    else:
        return isdsAppliance.invoke_put("Kickoff Backup of Active Partition",
                                        "/firmware_settings/kickoff_backup", {})


def swap(isdsAppliance, check_mode=False, force=False):
    """
    Kickoff swap of active partition
    """
    if check_mode is True:
        return isdsAppliance.create_return_object(changed=True)
    else:
        ret_obj_old = get(isdsAppliance)

        ret_obj = isdsAppliance.invoke_put("Kickoff swap of Active Partition",
                                           "/firmware_settings/kickoff_swap", {})
        # Process previous query after a successful call to swap the partition
        for partition in ret_obj_old['data']:
            if partition['active'] is False:  # Get version of inactive partition (active now!)
                ver = partition['firmware_version'].split(' ')
                isdsAppliance.facts['version'] = ver[-1]

        return ret_obj


def set(isdsAppliance, id, comment, check_mode=False, force=False):
    """
    Update comment on partition
    """
    if force is True or _check_comment(isdsAppliance, comment) is False:
        if check_mode is True:
            return isdsAppliance.create_return_object(changed=True)
        else:
            return isdsAppliance.invoke_put("Update comment on Partition",
                                            "/firmware_settings/{0}".format(id),
                                            {'comment': comment})

    return isdsAppliance.create_return_object()


def _check_comment(isdsAppliance, comment):
    ret_obj = get(isdsAppliance)

    # Loop through firmware partitions looking for active one
    for partition in ret_obj['data']:
        if partition['active'] is True:
            return (partition['comment'] == comment)

    return False


def compare(isdsAppliance1, isdsAppliance2):
    """
    Compare firmware between two appliances
    """
    ret_obj1 = get(isdsAppliance1)
    ret_obj2 = get(isdsAppliance2)

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
