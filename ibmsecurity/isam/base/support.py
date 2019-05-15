import logging
from ibmsecurity.utilities import tools
import os.path

logger = logging.getLogger(__name__)

uri = "/support"
requires_modules = None
requires_version = "9.0.2.0"


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieving information about all valid support files
    """
    return isamAppliance.invoke_get("Retrieving information about all valid support files", uri)


def get_categories(isamAppliance, check_mode=False, force=False):
    """
    Retrieving information about all the support categories
    """
    return isamAppliance.invoke_get("Retrieving information about all the support categories",
                                    "{0}/categories".format(uri))


def get_instances(isamAppliance, name, check_mode=False, force=False):
    """
    Retrieving information about all the instances for a specific support category
    """
    return isamAppliance.invoke_get("Retrieving information about all the instances for a specific support category",
                                    "{0}/categories/{1}/instances".format(uri, name))


def create(isamAppliance, comment='', wrp=None, isam_runtime=None, lmi=None, cluster=None, felb=None,
           aac_federation=None, system=None, check_mode=False, force=False):
    """
    Creating a new support file
    """
    json_data = {}
    json_data['comment'] = comment
    min_version = True

    if 'version' in isamAppliance.facts and isamAppliance.facts['version'] is not None:
        if tools.version_compare(isamAppliance.facts['version'], requires_version) < 0:
            min_version = False

    if min_version is True:
        if wrp != None:
            json_data['wrp'] = wrp

        if isam_runtime != None:
            json_data['isam_runtime'] = isam_runtime

        if lmi != None:
            json_data['lmi'] = lmi

        if cluster != None:
            json_data['cluster'] = cluster

        if felb != None:
            json_data['felb'] = felb

        if aac_federation != None:
            json_data['aac_federation'] = aac_federation

        if system != None:
            json_data['system'] = system

    if force is True or _check(isamAppliance, comment=comment) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post("Creating a new support file",
                                             "{0}/".format(uri),
                                             json_data,
                                             requires_modules=requires_modules,
                                             requires_version=requires_version)

    return isamAppliance.create_return_object()


def _check(isamAppliance, comment='', id=None):
    """
    Check if the last created support file has the exact same comment or id exists

    :param isamAppliance:
    :param comment:
    :return:
    """
    ret_obj = get(isamAppliance)

    if id != None:
        for sups in ret_obj['data']:
            if sups['id'] == id:
                return True
    else:
        for sups in ret_obj['data']:
            if sups['comment'] == comment:
                return True

    #        if isinstance(ret_obj['data'], list):
    #            # check only latest comment
    #            sup_file = min(ret_obj['data'], key=lambda sup: sup['index'])
    #            if sup_file['comment'] == comment:
    #                return True

    return False


def delete(isamAppliance, id, check_mode=False, force=False):
    """
    Deleting a support file
    """
    if force is True or _check(isamAppliance, id=id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            if isinstance(id, list):
                del_uri = "{0}/multi_destroy{1}".format(uri, tools.create_query_string(record_ids=','.join(id)))
            else:
                del_uri = "{0}/{1}".format(uri, id)
            return isamAppliance.invoke_delete("Deleting a support file", del_uri)

    return isamAppliance.create_return_object()


def modify(isamAppliance, id, filename, comment, check_mode=False, force=False):
    """
    Modify the snapshot comment
    """
    if force is True or _check(isamAppliance, id=id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put("Modifying snapshot", "{0}/{1}".format(uri, id),
                                            {
                                                'id': id,
                                                'filename': filename,
                                                'comment': comment
                                            })

    return isamAppliance.create_return_object()


def download(isamAppliance, filename, id, check_mode=False, force=False):
    """
    Download snapshot file(s) to a zip file.
    Note: id can be a list or a single value
    """
    if force is True or (_check(isamAppliance, id=id) is True and os.path.exists(filename) is False):
        if check_mode is False:  # No point downloading a file if in check_mode
            if isinstance(id, list):
                id = ','.join(id)
            uri_download = "{0}/download{1}".format(uri, tools.create_query_string(record_ids=id))
            return isamAppliance.invoke_get_file("Downloading snapshots", uri_download, filename)

    return isamAppliance.create_return_object()


def download_latest(isamAppliance, dir='.', check_mode=False, force=False):
    """
    Download latest support file to a zip file.
    """
    ret_obj = get(isamAppliance)

    # Get snapshot with lowest 'id' value - that will be latest one
    sup_file = min(ret_obj['data'], key=lambda sup: sup['index'])
    id = sup_file['id']
    file = sup_file['filename']
    filename = os.path.join(dir, file)

    return download(isamAppliance, filename, id, check_mode, force)


def compare(isamAppliance1, isamAppliance2):
    """
    Compare list of support files between 2 appliances - not sure if this will ever be useful?
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    for snapshot in ret_obj1['data']:
        del snapshot['id']
        del snapshot['filename']

    for snapshot in ret_obj2['data']:
        del snapshot['id']
        del snapshot['filename']

    return tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['id', 'filename'])
