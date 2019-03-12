import logging
from ibmsecurity.utilities import tools
import os.path

logger = logging.getLogger(__name__)

uri = "/support"


def get(isdsAppliance, check_mode=False, force=False):
    """
    Retrieving information about all valid support files
    """
    return isdsAppliance.invoke_get("Retrieving information about all valid support files", uri)


def create(isdsAppliance, comment='', check_mode=False, force=False):
    """
    Creating a new support file
    """
    if force is True or _check(isdsAppliance, comment=comment) is False:
        if check_mode is True:
            return isdsAppliance.create_return_object(changed=True)
        else:
            return isdsAppliance.invoke_post("Creating a new support file", uri,
                                             {
                                                 'comment': comment
                                             })

    return isdsAppliance.create_return_object()


def _check(isdsAppliance, comment='', id=None):
    """
    Check if the last created support file has the exact same comment or id exists

    :param isdsAppliance:
    :param comment:
    :return:
    """
    ret_obj = get(isdsAppliance)

    if id != None:
        for sups in ret_obj['data']:
            if sups['id'] == id:
                return True
    else:
        for sups in ret_obj['data']:
            if sups['comment'] == comment:
                return True

    #       if isinstance(ret_obj['data'], list):
    #           # check only latest comment
    #           sup_file = min(ret_obj['data'], key=lambda sup: sup['index'])
    #           if sup_file['comment'] == comment:
    #               return True

    return False


def delete(isdsAppliance, id, check_mode=False, force=False):
    """
    Deleting a support file
    """
    if force is True or _check(isdsAppliance, id=id) is True:
        if check_mode is True:
            return isdsAppliance.create_return_object(changed=True)
        else:
            if isinstance(id, list):
                del_uri = "{0}/multi_destroy{1}".format(uri, tools.create_query_string(record_ids=','.join(id)))
            else:
                del_uri = "{0}/{1}".format(uri, id)
            return isdsAppliance.invoke_delete("Deleting a support file", del_uri)

    return isdsAppliance.create_return_object()


def modify(isdsAppliance, id, filename, comment, check_mode=False, force=False):
    """
    Modify the snapshot comment
    """
    if force is True or _check(isdsAppliance, id=id) is True:
        if check_mode is True:
            return isdsAppliance.create_return_object(changed=True)
        else:
            return isdsAppliance.invoke_put("Modifying snapshot", "{0}/{1}".format(uri, id),
                                            {
                                                'id': id,
                                                'filename': filename,
                                                'comment': comment
                                            })

    return isdsAppliance.create_return_object()


def download(isdsAppliance, filename, id, check_mode=False, force=False):
    """
    Download snapshot file(s) to a zip file.
    Note: id can be a list or a single value
    """
    if force is True or (_check(isdsAppliance, id=id) is True and os.path.exists(filename) is False):
        if check_mode is False:  # No point downloading a file if in check_mode
            if isinstance(id, list):
                id = ','.join(id)
            uri_download = "{0}/download{1}".format(uri, tools.create_query_string(record_ids=id))
            return isdsAppliance.invoke_get_file("Downloading snapshots", uri_download, filename)

    return isdsAppliance.create_return_object()


def download_latest(isdsAppliance, dir='.', check_mode=False, force=False):
    """
    Download latest support file to a zip file.
    """
    ret_obj = get(isdsAppliance)

    # Get snapshot with lowest 'id' value - that will be latest one
    sup_file = min(ret_obj['data'], key=lambda sup: sup['index'])
    id = sup_file['id']
    file = sup_file['filename']
    filename = os.path.join(dir, file)

    return download(isdsAppliance, filename, id, check_mode, force)


def compare(isdsAppliance1, isdsAppliance2):
    """
    Compare list of support files between 2 appliances - not sure if this will ever be useful?
    """
    ret_obj1 = get(isdsAppliance1)
    ret_obj2 = get(isdsAppliance2)

    for snapshot in ret_obj1['data']:
        del snapshot['id']
        del snapshot['filename']

    for snapshot in ret_obj2['data']:
        del snapshot['id']
        del snapshot['filename']

    return tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['id', 'filename'])
