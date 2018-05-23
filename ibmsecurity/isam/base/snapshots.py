import logging
import ibmsecurity.utilities.tools
import os.path

logger = logging.getLogger(__name__)


def get(isamAppliance, check_mode=False, force=False):
    """
    Get information on existing snapshots
    """
    return isamAppliance.invoke_get("Retrieving snapshots", "/snapshots")


def get_latest(isamAppliance, check_mode=False, force=False):
    """
    Retrieve id of latest found snapshot
    """
    ret_obj_id = isamAppliance.create_return_object()
    ret_obj = get(isamAppliance)

    # Get snapshot with lowest 'id' value - that will be latest one
    snaps = min(ret_obj['data'], key=lambda snap: snap['index'])
    ret_obj_id['data'] = snaps['id']

    return ret_obj_id


def search(isamAppliance, comment, check_mode=False, force=False):
    """
    Retrieve snapshots with given comment contained
    """
    ret_obj = isamAppliance.create_return_object()
    ret_obj_all = get(isamAppliance)

    for obj in ret_obj_all['data']:
        if comment in obj['comment']:
            logger.debug("Snapshot comment \"{0}\" has this string \"{1}\" in it.".format(obj['comment'], comment))
            if ret_obj['data'] == {}:
                ret_obj['data'] = [obj['id']]
            else:
                ret_obj['data'].append(obj['id'])

    return ret_obj


def create(isamAppliance, comment='', check_mode=False, force=False):
    """
    Create a new snapshot
    """
    if force is True or _check(isamAppliance, comment=comment) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post("Creating snapshot", "/snapshots",
                                             {
                                                 'comment': comment
                                             })

    return isamAppliance.create_return_object()


def _check(isamAppliance, comment='', id=None):
    """
    Check if the last created snapshot has the exact same comment or id exists

    :param isamAppliance:
    :param comment:
    :return:
    """
    ret_obj = get(isamAppliance)

    if id != None:
        for snaps in ret_obj['data']:
            if snaps['id'] == id:
                return True
    else:
        for snaps in ret_obj['data']:
            if snaps['comment'] == comment:
                return True
                # # Get snapshot with lowest 'id' value - that will be latest one
                # snaps = min(ret_obj['data'], key=lambda snap: snap['index'])
                # logging.debug('Snapshot with lowest index is: ' + str(snaps))
                # try:
                #     if snaps['comment'] == comment:
                #         return True
                # except:
                #     pass

    return False


def delete(isamAppliance, id, check_mode=False, force=False):
    """
    Delete a snapshot
    """
    if force is True or _check(isamAppliance, id=id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete("Deleting snapshot", "/snapshots/" + id)

    return isamAppliance.create_return_object()

    # Logic to delete multiple snapshots - may need to be coded later
    #    uri = "/snapshots/multi_destroy?record_ids=" + ",".join(ids)
    #    return isamAppliance.invoke_delete("Deleting multiple snapshots", uri);


def modify(isamAppliance, id, comment, check_mode=False, force=False):
    """
    Modify the snapshot comment
    """
    if force is True or _check(isamAppliance, id=id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put("Modifying snapshot", "/snapshots/" + id,
                                            {
                                                'comment': comment
                                            })

    return isamAppliance.create_return_object()


def apply(isamAppliance, id, check_mode=False, force=False):
    """
    Apply a snapshot
    """
    if force is True or _check(isamAppliance, id=id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post_snapshot_id("Applying snapshot", "/snapshots/apply/" + id,
                                                         {"snapshot_id": id})

    return isamAppliance.create_return_object()


def download(isamAppliance, filename, id, check_mode=False, force=False):
    """
    Download one snapshot file to a zip file.
    TODO: Can hadnle multiple id's - but rest of logic deals with just one for now
    """
    if force is True or (_check(isamAppliance, id=id) is True and os.path.exists(filename) is False):
        if check_mode is False:  # No point downloading a file if in check_mode
            uri = "/snapshots/download?record_ids={0}".format(id)
            return isamAppliance.invoke_get_file("Downloading snapshots", uri, filename)

    return isamAppliance.create_return_object()


def download_latest(isamAppliance, dir='.', check_mode=False, force=False):
    """
    Download latest snapshot file to a zip file.
    """
    ret_obj = get(isamAppliance)

    # Get snapshot with lowest 'id' value - that will be latest one
    snaps = min(ret_obj['data'], key=lambda snap: snap['index'])
    id = snaps['id']
    file = snaps['filename']
    filename = os.path.join(dir, file)

    return download(isamAppliance, filename, id, check_mode, force)


def apply_latest(isamAppliance, check_mode=False, force=False):
    """
    Apply latest snapshot file (revert to latest)
    """
    ret_obj = get(isamAppliance)

    # Get snapshot with lowest 'id' value - that will be latest one
    snaps = min(ret_obj['data'], key=lambda snap: snap['index'])
    id = snaps['id']

    return apply(isamAppliance, id, check_mode, force)


def compare(isamAppliance1, isamAppliance2):
    """
    Compare list of snapshots between 2 appliances
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    # id of snapshot is uniquely generated on appliance and should therefore be ignored in comparison.
    # filename of snapshot is generated based on exact date/time and will differ even if 2 snapshots are taken near the
    # same time. Therefore, filename should be ignored in comparison
    for snapshot in ret_obj1['data']:
        del snapshot['id']
        del snapshot['filename']

    for snapshot in ret_obj2['data']:
        del snapshot['id']
        del snapshot['filename']

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['id', 'filename'])
