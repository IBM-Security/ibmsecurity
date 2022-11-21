import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get(isvgAppliance, check_mode=False, force=False):
    """
    Retrieve existing firmware.
    """
    return isvgAppliance.invoke_get("Retrieving firmware",
                                    "/firmware_settings")


def backup(isvgAppliance, check_mode=False, force=False):
    """
    Kickoff Backup of active partition
    """
    if check_mode is True:
        return isvgAppliance.create_return_object(changed=True)
    else:
        return isvgAppliance.invoke_put("Kickoff Backup of Active Partition",
                                        "/firmware_settings/kickoff_backup", {})


def swap(isvgAppliance, check_mode=False, force=False):
    """
    Kickoff swap of active partition
    """
    if check_mode is True:
        return isvgAppliance.create_return_object(changed=True)
    else:
        ret_obj_old = get(isvgAppliance)

        ret_obj = isvgAppliance.invoke_put("Kickoff swap of Active Partition",
                                           "/firmware_settings/kickoff_swap", {})
        # Process previous query after a successful call to swap the partition
        for partition in ret_obj_old['data']:
            if partition['active'] is False:  # Get version of inactive partition (active now!)
                ver = partition['firmware_version'].split(' ')
                isvgAppliance.facts['version'] = ver[-1]

        return ret_obj


def set(isvgAppliance, id, comment, check_mode=False, force=False):
    """
    Update comment on partition
    """
    if force is True or _check_comment(isvgAppliance, comment) is False:
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True)
        else:
            return isvgAppliance.invoke_put("Update comment on Partition",
                                            "/firmware_settings/{0}".format(id),
                                            {'comment': comment})

    return isvgAppliance.create_return_object()


def _check_comment(isvgAppliance, comment):
    ret_obj = get(isvgAppliance)

    # Loop through firmware partitions looking for active one
    for partition in ret_obj['data']:
        if partition['active'] is True:
            return (partition['comment'] == comment)

    return False


def compare(isvgAppliance1, isvgAppliance2):
    """
    Compare firmware between two appliances
    """
    ret_obj1 = get(isvgAppliance1)
    ret_obj2 = get(isvgAppliance2)

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
