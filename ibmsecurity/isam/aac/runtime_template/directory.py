import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)

requires_modules = ["mga", "federation"]
requires_version = None


def get_all(isamAppliance, check_mode=False, force=False, ignore_error=False):
    """
    Retrieving the current runtime template files directory contents
    """
    return isamAppliance.invoke_get("Retrieving the current runtime template files directory contents",
                                    "/mga/template_files?recursive=yes", ignore_error=ignore_error,
                                    requires_modules=requires_modules,
                                    requires_version=requires_version)


def get(isamAppliance, path, recursive=None, check_mode=False, force=False):
    """
    Retrieving the current runtime template files directory contents
    """
    return isamAppliance.invoke_get("Retrieving the current runtime template files directory contents",
                                    "/mga/template_files/{}/{}".format(path,
                                                                       ibmsecurity.utilities.tools.create_query_string(
                                                                           recursive=recursive)),
                                    requires_modules=requires_modules,
                                    requires_version=requires_version)


def _check(isamAppliance, id):
    ret_obj = get_all(isamAppliance, ignore_error=True)

    if (ret_obj['rc'] != 404 or ret_obj['rc'] != 400):
        return _parse_id(ret_obj['data'], id)
    else:
        return None


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
    id = path + "/" + name
    check_dir = _check(isamAppliance, id)
    if check_dir != None:
        warnings.append("Directory {0} exists in path {1}. Ignoring create.".format(name, path))

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
                }, requires_modules=requires_modules,
                requires_version=requires_version)

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
    warnings = []
    check_dir = _check(isamAppliance, id)
    if check_dir == None:
        warnings.append("Directory {0} does not exist. Ignoring delete.".format(id))

    if force is True or check_dir != None:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Deleting a directory in the runtime template files directory",
                "/mga/template_files/{0}".format(id), requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object(warnings=warnings)


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
    warnings = []

    try:
        split_dir = id.split('/')
        path = split_dir[:-1]
        new_path = '/'.join([str(x) for x in path]) + "/" + new_name
    except:
        logger.info("New path can't be build from id: {0} and new_name: {1}.".format(id, new_name))

    if force is False:
        new_dir_id = _check(isamAppliance, new_path)
        dir_id = _check(isamAppliance, id)

    if new_dir_id != None:
        warnings.append("Directory {0} does already exist. Ignoring renameing.".format(new_path))

    if force is True or (dir_id != None and new_dir_id == None):
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Renaming a directory in the runtime template files directory",
                "/mga/template_files/{0}".format(id),
                {
                    'new_name': new_name,
                    'type': 'directory'
                }, requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object(warnings=warnings)


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


def compare(isamAppliance1, isamAppliance2, path):
    ret_obj1 = get(isamAppliance1, path)
    ret_obj2 = get(isamAppliance2, path)

    _remove_version(ret_obj1['data'])
    _remove_version(ret_obj2['data'])

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['version'])
