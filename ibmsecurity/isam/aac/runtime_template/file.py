import logging
import ibmsecurity.utilities.tools
import os.path
from ibmsecurity.utilities.tools import files_same, get_random_temp_dir
import shutil

logger = logging.getLogger(__name__)

requires_modules = ["mga", "federation"]
requires_version = None


def get(isamAppliance, path, check_mode=False, force=False):
    """
    Retrieving the current runtime template files directory contents
    """
    return isamAppliance.invoke_get("Retrieving the current runtime template files directory contents",
                                    "/mga/template_files/{0}".format(path), requires_modules=requires_modules,
                                    requires_version=requires_version)


def _check(isamAppliance, path, name):
    ret_obj = get(isamAppliance, path)

    for obj in ret_obj['data']['contents']:
        if obj['name'] == name and obj['type'] == 'File':
            logger.info("File .{0}".format(obj['name']))
            return True

    return None


def create(isamAppliance, path, name, contents=None, check_mode=False, force=False):
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
    check_file = _check(isamAppliance, path, name)
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
                }, requires_modules=requires_modules,
                requires_version=requires_version)
    return isamAppliance.create_return_object(warnings=warnings)


def update(isamAppliance, path, name, contents=None, check_mode=False, force=False):
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
    check_file = _check(isamAppliance, path, name)
    if check_file == None:
        warnings.append("File {0} does not exists in path {1}. Ignoring update.".format(name, path))
        return isamAppliance.create_return_object(warnings=warnings)

    if force is True or check_file is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            if contents is not None:
                return isamAppliance.invoke_put_files(
                    "Update a file in the runtime template files directory",
                    "/mga/template_files/{0}/{1}".format(path, name),
                    {
                        'contents': contents,
                        'type': 'file'
                    }, requires_modules=requires_modules,
                    requires_version=requires_version)
            else:
                warnings.append("Either contents or filename parameter need to be provided. Skipping update request.")
                return isamAppliance.create_return_object(warnings=warnings)


def delete(isamAppliance, path, name, check_mode=False, force=False):
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
    check_file = _check(isamAppliance, path, name)
    if check_file == None:
        warnings.append("File {0} does not exists in path {1}. Ignoring delete.".format(name, path))
        return isamAppliance.create_return_object(warnings=warnings)

    if force is True or check_file != None:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Deleting a file in the runtime template files directory",
                "/mga/template_files/{0}/{1}".format(path, name), requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object()


def rename(isamAppliance, path, name, new_name, check_mode=False, force=False):
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
    check_file = _check(isamAppliance, path, name)
    if check_file == None:
        warnings.append("File {0} does not exists in path {1}. Ignoring rename.".format(name, path))
        return isamAppliance.create_return_object(warnings=warnings)

    if force is True or check_file != None:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Renaming a file in the runtime template files directory",
                "/mga/template_files/{0}/{1}".format(path, name),
                {
                    'new_name': new_name,
                    'type': 'file'
                }, requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object()


def export_file(isamAppliance, path, name, filename, check_mode=False, force=False):
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
    check_file = _check(isamAppliance, path, name)
    if check_file == None:
        warnings.append("File {0} does not exists in path {1}. Ignoring export.".format(name, path))
        return isamAppliance.create_return_object(warnings=warnings)

    if force is True or check_file != None:
        if check_mode is False:
            return isamAppliance.invoke_get_file(
                "Exporting a file from the runtime template files directory",
                "/mga/template_files/{0}/{1}?type=File&export=true".format(path, name), filename,
                requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object()


def _check_import(isamAppliance, path, name, filename, check_mode=False):
    """
    Checks if file on the Appliance (name) exists and if so, whether it is different from filename
    :param isamAppliance:
    :param path:
    :param name:
    :param filename:
    :return:
    """
    tmpdir = get_random_temp_dir()
    tmp_original_file = os.path.join(tmpdir, os.path.basename(name))
    if _check(isamAppliance, path, name):
        export_file(isamAppliance, path, name, tmp_original_file, check_mode=False, force=True)
        logger.debug("file already exists on appliance")
        if files_same(tmp_original_file, filename):
            logger.debug("files are the same, so we don't want to do anything")
            shutil.rmtree(tmpdir)
            return False
        else:
            logger.debug("files are different, so we delete existing file in preparation for import")
            delete(isamAppliance, path, name, check_mode=check_mode, force=True)
            shutil.rmtree(tmpdir)
            return True
    else:
        logger.debug("file does not exist on appliance, so we'll want to import")
        shutil.rmtree(tmpdir)
        return True


def import_file(isamAppliance, path, name, filename, check_mode=False, force=False):
    """
    Importing a file in the runtime template files directory.
    """
    warnings = []
    check_file = _check(isamAppliance, path, name)
    if check_file != None and force == False:
        warnings.append("File {0} exists in path {1}.".format(name, path))

    if force is True or _check_import(isamAppliance, path, name, filename, check_mode=check_mode):
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post_files(
                "Importing a file in the runtime template files directory",
                "/mga/template_files/{0}/{1}".format(path, name),
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
                }, requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object(warnings=warnings)
