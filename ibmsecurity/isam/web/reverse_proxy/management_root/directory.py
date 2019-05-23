import logging
import ibmsecurity.utilities.tools
import os.path
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)


def get(isamAppliance, instance_id, dir_name='', recursive='yes', check_mode=False, force=False):
    """
    Retrieving the current administration pages contents of a directory.
    Parameter variables have the following behavior:
        dir_name and recursive not set => recursively list from root directory (default behavior)
        dir_name only set => list recursively from dir_name and below
        recursive set to 'no' => flat directory listing of dir_name (which defaults to root)
    """
    return isamAppliance.invoke_get("Retrieving the current administration pages root contents",
                                    "/wga/reverseproxy/{0}/management_root/{1}{2}".format(
                                        instance_id, dir_name, tools.create_query_string(recursive=recursive)))


def _check(isamAppliance, instance_id, id, name):
    ret_obj = get(isamAppliance, instance_id)

    dir_name = os.path.join(id, name)

    return _parse_id(ret_obj['data'], dir_name)


def _parse_id(contents, dir_name):
    """
    Recursively parse and find the id for a given directory

    :param contents:
    :param dir_name:
    :return id:
    """
    try:
        split_dir = dir_name.split('/', 1)
        cur_dir = split_dir[0]
        rest_dir = split_dir[1]
    except:
        rest_dir = ''
    for dir in contents:
        if dir['name'] == cur_dir and dir['type'] == 'Directory':
            if rest_dir == '':
                return dir['id']
            else:
                if len(dir['children']) == 0:
                    return None
                else:
                    return _parse_id(dir['children'], rest_dir)

    return None


def create(isamAppliance, instance_id, id, name, check_mode=False, force=False):
    """
    Creating a directory in the administration pages root

    :param isamAppliance:
    :param instance_id:
    :param id:
    :param name:
    :param check_mode:
    :param force:
    :return:
    """
    if force is True or _check(isamAppliance, instance_id, id, name) == None:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post(
                "Creating a directory in the administration pages root",
                "/wga/reverseproxy/{0}/management_root/{1}".format(instance_id, id),
                {
                    'dir_name': name,
                    'type': 'dir'
                })

    return isamAppliance.create_return_object()


def delete(isamAppliance, instance_id, id, check_mode=False, force=False):
    """
    Deleting a file or directory in the administration pages root

    :param isamAppliance:
    :param instance_id:
    :param id:
    :param name:
    :param check_mode:
    :param force:
    :return:
    """
    if force is True or _check(isamAppliance, instance_id, id, '') != None:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Deleting a directory in the administration pages root",
                "/wga/reverseproxy/{0}/management_root/{1}".format(instance_id, id))

    return isamAppliance.create_return_object()


def rename(isamAppliance, instance_id, id, new_name, check_mode=False, force=False):
    """
    Deleting a file or directory in the administration pages root

    :param isamAppliance:
    :param instance_id:
    :param id:
    :param name:
    :param check_mode:
    :param force:
    :return:
    """
    dir_id = None
    if force is False:
        dir_id = _check(isamAppliance, instance_id, id, '')

    if force is True or dir_id != None:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Renaming a directory in the administration pages root",
                "/wga/reverseproxy/{0}/management_root/{1}".format(instance_id, id),
                {
                    'id': dir_id,
                    'new_name': new_name,
                    'type': 'directory'
                })

    return isamAppliance.create_return_object()


def _remove_version(contents):
    """
    Recursively parse and remove version

    :param contents:
    :return:
    """
    for obj in contents:
        try:
            del obj['version']
            if len(obj['children']) != 0:
                _remove_version(obj['children'])
        except:
            pass
    return


def compare(isamAppliance1, isamAppliance2, instance_id):
    ret_obj1 = get(isamAppliance1, instance_id)
    ret_obj2 = get(isamAppliance2, instance_id)

    _remove_version(ret_obj1['data'])
    _remove_version(ret_obj2['data'])

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['version'])
