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

def multi_delete(isamAppliance, ids=[], comment=None, check_mode=False, force=False):
    """
    Delete multiple snapshots based on id or comment
    """
    if comment != None:
      ret_obj = search(isamAppliance, comment=comment)
      if ret_obj['data'] == {}:
        return isamAppliance.create_return_object(changed=False)
      else:
        if ids == []:
          ids = ret_obj['data']
        else:
          for snaps in ret_obj['data']:
            ids.append(snaps)

    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:
        return isamAppliance.invoke_delete("Deleting one or multiple snapshots", "/snapshots/multi_destroy?record_ids=" + ",".join(ids))

    return isamAppliance.create_return_object()

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


def apply(isamAppliance, id=None, comment=None, check_mode=False, force=False):
    """
    Apply a snapshot
    There is a priority in the parameter to be used for snapshot applying: id > comment
    """
    if comment != None and id == None:
      ret_obj = search(isamAppliance, comment=comment)
      if ret_obj['data'] == {}:
        return isamAppliance.create_return_object(changed=False)
      elif len(ret_obj['data']) == 1:
        id = ret_obj['data'][0]
      else:
        logger.warn("There are multiple files with matching comments. Only one snapshot at a time can be applied !")

    if id != None:
      if force is True or _check(isamAppliance, id=id) is True:
          if check_mode is True:
              return isamAppliance.create_return_object(changed=True)
          else:
              return isamAppliance.invoke_post_snapshot_id("Applying snapshot", "/snapshots/apply/" + id,
                                                          {"snapshot_id": id})

    return isamAppliance.create_return_object()


def download(isamAppliance, filename, id=None, ids=[], comment=None, check_mode=False, force=False):
    """
    Download one snapshot file to a zip file.
    Multiple file download is now supported.
    For backwards compatibility the id parameter and old behaviour is checked at the beginning.
    """
    if id != None:
      if force is True or (_check(isamAppliance, id=id) is True and os.path.exists(filename) is False):
          if check_mode is False:  # No point downloading a file if in check_mode
              uri = "/snapshots/download?record_ids={0}".format(id)
              return isamAppliance.invoke_get_file("Downloading snapshots", uri, filename)
    else:
      # Search for the id corresponding to the comment and consolidate them in the ids variable
      if comment != None:
        ret_obj = search(isamAppliance, comment=comment)
        if ret_obj['data'] == {}:
          logger.info("No snapshots found with text {0} in it.".format(comment))
        else:
          if ids == []:
            ids = ret_obj['data']
          else:
            for snaps in ret_obj['data']:
              ids.append(snaps)

      # Additional check (REST-Calls) for every id in the ids variable is skipped as in this case error handling is better done by the REST API
      if force is True or os.path.exists(filename) is False: # Don't overwrite if not forced to
        if check_mode is True and ids != []: # We are in check_mode but would try to download named ids
          return isamAppliance.create_return_object(changed=True)
        elif check_mode is True and ids == []: # We are in check_mode but have nothing to download
          return isamAppliance.create_return_object(changed=False)
        else:
          # Download all ids known so far
          return isamAppliance.invoke_get_file("Downloading multiple snapshots","/snapshots/download?record_ids=" + ",".join(ids), filename )

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

def upload(isamAppliance, file, comment=None, check_mode=False, force=False):
    """
    Upload Snapshot file
    """
    if force is True or _check_file(isamAppliance, file) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            if comment == None:
              import zipfile

              zFile = zipfile.ZipFile(file)
              if "Comment" in zFile.namelist():
                comment = zFile.open("Comment")

            return isamAppliance.invoke_post_files(
                "Upload Snapshot",
                "/snapshots",
                [{
                    'file_formfield': 'uploadedfile',
                    'filename': file,
                    'mimetype': 'application/octet-stream'
                }],
                {
                  'comment': comment if comment != None else ''
                }, json_response=False)

    return isamAppliance.create_return_object()

def _check_file(isamAppliance, file):
    """
    Check if snapshot file already exists
    """
    import os.path

    ret_obj = get(isamAppliance)

    filename = os.path.basename(file)

    for obj in ret_obj['data']:
        if obj['filename'] == filename:
            return True

    return False

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
