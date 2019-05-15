import logging
import ibmsecurity.utilities.tools
import os.path

logger = logging.getLogger(__name__)


def get(isdsAppliance, check_mode=False, force=False):
    """
    Get information on existing snapshots
    """
    return isdsAppliance.invoke_get("Retrieving snapshots", "/snapshots")


def create(isdsAppliance, comment='', check_mode=False, force=False):
    """
    Create a new snapshot
    """
    if force is True or _check(isdsAppliance, comment=comment) is False:
        if check_mode is True:
            return isdsAppliance.create_return_object(changed=True)
        else:
            return isdsAppliance.invoke_post("Creating snapshot", "/snapshots",
                                             {
                                                 'comment': comment
                                             })

    return isdsAppliance.create_return_object()


def delete(isdsAppliance, id, check_mode=False, force=False):
    """
    Delete a snapshot
    """
    if force is True or _check(isdsAppliance, id=id) is True:
        if check_mode is True:
            return isdsAppliance.create_return_object(changed=True)
        else:
            return isdsAppliance.invoke_delete("Deleting snapshot", "/snapshots/" + id)

    return isdsAppliance.create_return_object()


def modify(isdsAppliance, id, comment, check_mode=False, force=False):
    """
    Modify the snapshot comment
    """
    if force is True or _check(isdsAppliance, id=id) is True:
        if check_mode is True:
            return isdsAppliance.create_return_object(changed=True)
        else:
            return isdsAppliance.invoke_put("Modifying snapshot", "/snapshots/" + id,
                                            {
                                                'comment': comment
                                            })

    return isdsAppliance.create_return_object()


def apply(isdsAppliance, id, check_mode=False, force=False):
    """
    Apply a snapshot
    """
    uri = "/snapshots/apply/" + id
    if force is True or _check(isdsAppliance, id=id) is True:
        if check_mode is True:
            return isdsAppliance.create_return_object(changed=True)
        else:
            return isdsAppliance.invoke_post("Applying snapshot", uri,
                                             {"authenticity_token": "KRVlgWbaS4GCOxfZcw+hkrPH2fVB1Vi+k8cayf0y9T4"})

    return isdsAppliance.create_return_object()


def download(isdsAppliance, filename, id, check_mode=False, force=False):
    """
    Download one snapshot file to a zip file.
    TODO: Can handle multiple id's - but rest of logic deals with just one for now
    """
    if force is True or (_check(isdsAppliance, id=id) is True and os.path.exists(filename) is False):
        if check_mode is False:  # No point downloading a file if in check_mode
            uri = "/snapshots/download?record_ids={0}".format(id)
            return isdsAppliance.invoke_get_file("Downloading snapshots", uri, filename)

    return isdsAppliance.create_return_object()


def download_latest(isdsAppliance, dir='.', check_mode=False, force=False):
    """
    Download latest snapshot file to a zip file.
    """
    ret_obj = get(isdsAppliance)

    # Get snapshot with lowest 'id' value - that will be latest one
    snaps = min(ret_obj['data'], key=lambda snap: snap['index'])
    id = snaps['id']
    file = snaps['filename']
    filename = os.path.join(dir, file)

    return download(isdsAppliance, filename, id, check_mode, force)


def upload(isdsAppliance, filename, check_mode=False, force=False):
    """
    Upload snapshot
    """
    uri = "/snapshots/upload"
    if _check(isdsAppliance, fn=filename) is False:
        if check_mode is True:
            return isdsAppliance.create_return_object(changed=True)
        else:
            return isdsAppliance.invoke_post_files(
                description="Upload snapshot",
                uri="{0}".format(uri),
                fileinfo=[{
                    'file_formfield': 'file',
                    'filename': filename,
                    'mimetype': 'application/octet-stream'
                }],
                data={},
                json_response=False)

    return isdsAppliance.create_return_object()


def apply_latest(isdsAppliance, check_mode=False, force=False):
    """
    Apply latest snapshot file (revert to latest)
    """
    ret_obj = get(isdsAppliance)

    # Get snapshot with lowest 'id' value - that will be latest one
    snaps = min(ret_obj['data'], key=lambda snap: snap['index'])
    id = snaps['id']

    return apply(isdsAppliance, id, check_mode, force)


def compare(isdsAppliance1, isdsAppliance2):
    """
    Compare list of snapshots between 2 appliances
    """
    ret_obj1 = get(isdsAppliance1)
    ret_obj2 = get(isdsAppliance2)

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


def _check(isdsAppliance, comment='', id=None, fn=None):
    """
    Check if the last created snapshot has the exact same comment or id exists

    :param isdsAppliance:
    :param comment:
    :return:
    """
    ret_obj = get(isdsAppliance)

    if id != None:
        for snaps in ret_obj['data']:
            if snaps['id'] == id:
                return True
    elif fn != None:
        for snaps in ret_obj['data']:
            if snaps['filename'] == fn:
                return True
    else:
        for snaps in ret_obj['data']:
            if snaps['comment'] == comment:
                return True

    return False
