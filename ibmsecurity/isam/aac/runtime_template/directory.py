import logging
import ibmsecurity.utilities.tools
import os.path

logger = logging.getLogger(__name__)


def get(isamAppliance, path, check_mode=False, force=False):
    """
    Retrieving the current runtime template files directory contents
    """
    return isamAppliance.invoke_get("Retrieving the current runtime template files directory contents",
                                    "/mga/template_files/{0}".format(path))


def _check(isamAppliance, path, name):
    ret_obj = get(isamAppliance, path)

    for obj in ret_obj['data']['contents']:
        if obj['name'] == name and obj['type'] == 'Directory':
            logger.info("Dir .{0}".format(obj['name']))
            return obj['id']    
   
    return None


def create(isamAppliance, path, name, check_mode=False, force=False):
    """
    Creating a directory in the runtime template files directory

    :param isamAppliance:
    :param id:
    :param name:
    :param check_mode:
    :param force:
    :return:
    """
    warnings = []
    check_dir = _check(isamAppliance, path, name)
    if check_dir != None:
        warnings.append("Directory {0} exists in path {1}. Ignoring create.".format(name,path))

    if force is True or check_dir == None:
        if check_mode is True:          
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_post(
                "Creating a directory in the runtime template files directory",
                "/mga/template_files/{0}".format(path),
                {
                    'dir_name': name,
                    'type': 'dir'
                })

    return isamAppliance.create_return_object(warnings=warnings)


def delete(isamAppliance, id, check_mode=False, force=False):
    """
    Deleting a file or directory in the runtime template files directory

    :param isamAppliance:
    :param id:
    :param check_mode:
    :param force:
    :return:
    """
    if force is True or _check(isamAppliance, id, '') != None:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Deleting a directory in the runtime template files directory",
                "/mga/template_files/{0}".format(id))

    return isamAppliance.create_return_object()


def rename(isamAppliance, id, new_name, check_mode=False, force=False):
    """
    Deleting a file or directory in the runtime template files directory

    :param isamAppliance:
    :param id:
    :param new_name:
    :param check_mode:
    :param force:
    :return:
    """
    dir_id = None
    if force is False:
        dir_id = _check(isamAppliance, id, '')

    if force is True or dir_id != None:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Renaming a directory in the runtime template files directory",
                "/mga/template_files/{0}".format(id),
                {
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
