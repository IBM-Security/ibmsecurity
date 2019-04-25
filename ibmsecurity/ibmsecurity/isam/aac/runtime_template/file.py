import logging
import ibmsecurity.utilities.tools
import os.path
from ibmsecurity.utilities.tools import files_same, get_random_temp_dir
import shutil

logger = logging.getLogger(__name__)


def get_all(isamAppliance, check_mode=False, force=False, ignore_error=False):
    """
    Retrieving the current runtime template files directory contents
    """
    return isamAppliance.invoke_get("Retrieving the current runtime template files directory contents",
                                    "/mga/template_files?recursive=yes", ignore_error=ignore_error)


def get(isamAppliance, id, check_mode=False, force=False, ignore_error=False):
    """
    Retrieving the current runtime template files directory contents
    """
    return isamAppliance.invoke_get("Retrieving the current runtime template files directory contents",
                                    "/mga/template_files/{0}".format(id), ignore_error=ignore_error)


def _check(isamAppliance, id):
    ret_obj = get_all(isamAppliance, ignore_error=True)

    if (ret_obj['rc'] != 404 or ret_obj['rc'] != 400):
        return _parse_id(ret_obj['data'], id)
    else:
        return None


def _parse_id(contents, file_name):
    """
    Recursively parse and find the id for a given file name

    :param contents:
    :param file_name:
    :return id:
    """
    try:
        split_file = file_name.split('/', 1)
        cur_file = split_file[0]
        rest_file = split_file[1]
    except:
        rest_file = ''
    for file in contents:
        if file['name'] == cur_file:
            if rest_file == '':
                if file['type'] == 'File':
                    return file['id']
                else:
                    return None
            else:
                if len(file['children']) == 0:
                    return None
                else:
                    return _parse_id(file['children'], rest_file)

    return None


def create(isamAppliance, path, name, contents="", check_mode=False, force=False):
    """
    Creating a file in the runtime template files directory

    :param isamAppliance:
    :param path:
    :param name:
    :param contents:
    :param check_mode:
    :param force:
    :return:
    """
    warnings = []
    id = path + "/" + name
    check_file = _check(isamAppliance, id)
    if check_file != None:
        warnings.append("File {0} exists in path {1}. Ignoring create.".format(name, path))

    if force is True or check_file == None:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_post(
                "Creating a file in the runtime template files directory",
                "/mga/template_files/{0}".format(path),
                {
                    'file_name': name,
                    'type': 'file',
                    'contents': contents
                })
    return isamAppliance.create_return_object(warnings=warnings)


def update(isamAppliance, id, contents=None, check_mode=False, force=False):
    """
    Update a file in the runtime template files directory
    :param isamAppliance:
    :param path:
    :param name:
    :param contents:
    :param check_mode:
    :param force:
    :return:
    """
    warnings = []
    check_file = _check(isamAppliance, id)
    if check_file == None:
        warnings.append("File {0} does not exists. Ignoring update.".format(id))
        return isamAppliance.create_return_object(warnings=warnings)

    if force is True or check_file != None:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            if contents is not None:
                return isamAppliance.invoke_put(
                    "Update a file in the runtime template files directory",
                    "/mga/template_files/{0}".format(id),
                    {
                        'contents': contents,
                        'type': 'file'
                    })
            else:
                warnings.append("Either contents or filename parameter need to be provided. Skipping update request.")
                return isamAppliance.create_return_object(warnings=warnings)


def delete(isamAppliance, id, check_mode=False, force=False):
    """
    Deleting a file in the runtime template files directory

    :param isamAppliance:
    :param path:
    :param name:
    :param check_mode:
    :param force:
    :return:
    """
    warnings = []
    check_file = _check(isamAppliance, id)
    if check_file == None:
        warnings.append("File {0} does not exists. Ignoring delete.".format(id))
        return isamAppliance.create_return_object(warnings=warnings)

    if force is True or check_file != None:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Deleting a file in the runtime template files directory",
                "/mga/template_files/{0}".format(id))

    return isamAppliance.create_return_object()


def rename(isamAppliance, id, new_name, check_mode=False, force=False):
    """
    Deleting a file in the runtime template files directory

    :param isamAppliance:
    :param path:
    :param name:
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
        new_file_id = _check(isamAppliance, new_path)
        file_id = _check(isamAppliance, id)

    if new_file_id != None:
        warnings.append("File {0} does already exist. Ignoring renameing.".format(new_path))

    if force is True or (file_id != None and new_file_id == None):
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Renaming a file in the runtime template files directory",
                "/mga/template_files/{0}".format(id),
                {
                    'new_name': new_name,
                    'type': 'file'
                })

    return isamAppliance.create_return_object(warnings=warnings)


def export_file(isamAppliance, id, filename, check_mode=False, force=False):
    """
    Exporting a file from the runtime template files directory

    :param isamAppliance:
    :param path:
    :param name:
    :param check_mode:
    :param force:
    :return:
    """
    warnings = []
    check_file = _check(isamAppliance, id)
    if check_file == None:
        warnings.append("File {0} does not exists. Ignoring export.".format(id))
        return isamAppliance.create_return_object(warnings=warnings)

    if force is True or check_file != None:
        if check_mode is False:
            return isamAppliance.invoke_get_file(
                "Exporting a file from the runtime template files directory",
                "/mga/template_files/{0}?type=File&export=true".format(id), filename)

    return isamAppliance.create_return_object()


def _check_import(isamAppliance, id, filename, check_mode=False):
    """
    Checks if file on the Appliance (name) exists and if so, whether it is different from filename
    :param isamAppliance:
    :param path:
    :param name:
    :param filename:
    :return:
    """
    tmpdir = get_random_temp_dir()
    tmp_original_file = os.path.join(tmpdir, os.path.basename(id))
    if _check(isamAppliance, id):
        export_file(isamAppliance, id, tmp_original_file, check_mode=False, force=True)
        logger.debug("file already exists on appliance")
        if files_same(tmp_original_file, filename):
            logger.debug("files are the same, so we don't want to do anything")
            shutil.rmtree(tmpdir)
            return False
        else:
            logger.debug("files are different, so we delete existing file in preparation for import")
            delete(isamAppliance, id, check_mode=check_mode, force=True)
            shutil.rmtree(tmpdir)
            return True
    else:
        logger.debug("file does not exist on appliance, so we'll want to import")
        shutil.rmtree(tmpdir)
        return True


def import_file(isamAppliance, id, filename, check_mode=False, force=False):
    """
    Importing a file in the runtime template files directory.
    """
    warnings = []
    check_file = _check(isamAppliance, id)
    if check_file != None and force == False:
        warnings.append("File {0} exist.".format(id))

    if force is True or _check_import(isamAppliance, id, filename, check_mode=check_mode):
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post_files(
                "Importing a file in the runtime template files directory",
                "/mga/template_files/{0}".format(id),
                [
                    {
                        'file_formfield': 'file',
                        'filename': filename,
                        'mimetype': 'application/octet-stream'
                    }
                ],
                {
                    'type': 'file',
                    'force': force
                })

    return isamAppliance.create_return_object(warnings=warnings)


def compare(isamAppliance1, isamAppliance2):
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
