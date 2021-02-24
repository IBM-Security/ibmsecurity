import logging
import os

import ibmsecurity
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

uri = "/wga/apiac/resource/instance"
requires_modules = ["wga"]
requires_version = "9.0.7"


def get_all(isamAppliance, instance_name, check_mode=False, force=False):
    """
    Retrieving the list of all files in the API Access Control documentation root
    """
    instance_exist, warnings = _check_instance_exist(isamAppliance, instance_name)

    if force is True or instance_exist is True:
        return isamAppliance.invoke_get(
            "Retrieving the list of all files in the API Access Control documentation root ",
            "{0}/{1}/documentation/".format(uri, instance_name),
            requires_modules=requires_modules, requires_version=requires_version)


def get(isamAppliance, instance_name, file_name, check_mode=False, force=False):
    """
    Retrieving the list of all files in the API Access Control documentation root
    """
    instance_exist, warnings = _check_instance_exist(isamAppliance, instance_name)

    if force is True or instance_exist is True:
        return isamAppliance.invoke_get(
            "Retrieving the list of all files in the API Access Control documentation root ",
            "{0}/{1}/documentation/{2}".format(uri, instance_name, file_name),
            requires_modules=requires_modules, requires_version=requires_version)


def add(isamAppliance, instance_name, type, file_name=None, dir_name=None, contents=None,
        check_mode=False, force=False):
    """
    Creating a file or directory in the API Access Control documentation
    """
    exist, warnings = _check_exist(isamAppliance, instance_name, file_name)

    if force is True or exist is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            json_data = {
                "type": type
            }
            if file_name != None:
                json_data['file_name'] = file_name

            if dir_name != None:
                json_data['dir_name'] = dir_name

            if contents != None:
                json_data['contents'] = contents

            return isamAppliance.invoke_post(
                "Creating a file or directory in the API Access Control documentation ",
                "{0}/{1}/documentation".format(uri, instance_name),
                json_data,
                requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object(warnings=warnings)


def update(isamAppliance, instance_name, file_name, contents, type='file', check_mode=False, force=False):
    """
    Updating a file in the API Access Control documentation root
    """
    same_contents, warnings = _check_contents(isamAppliance, instance_name, file_name, contents)

    if force is True or same_contents is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            json_data = {
                "type": type,
                "contents": contents
            }

            return isamAppliance.invoke_put(
                "Updating a file in the API Access Control documentation root  ",
                "{0}/{1}/documentation/{2}".format(uri, instance_name, file_name),
                json_data,
                requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object(warnings=warnings)


def set(isamAppliance, instance_name, file_name, contents, type='file', check_mode=False, force=False):
    exist, warnings = _check_exist(isamAppliance, instance_name, file_name)

    if exist is True:
        return update(isamAppliance=isamAppliance, instance_name=instance_name, file_name=file_name, contents=contents,
                      type=type, check_mode=check_mode, force=force)
    else:
        return add(isamAppliance=isamAppliance, instance_name=instance_name, type=type, file_name=file_name,
                   contents=contents,
                   check_mode=check_mode, force=force)


def rename_directory(isamAppliance, instance_name, file_name, new_name, type='directory', check_mode=False,
                     force=False):
    """
    Renaming a directory in the API Access Control documentation root
    """
    exists, warnings = _check_exist(isamAppliance, instance_name, file_name)

    if force is True or exists is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            json_data = {
                "type": type,
                "new_name": new_name
            }

            return isamAppliance.invoke_put(
                "Renaming a directory in the API Access Control documentation root",
                "{0}/{1}/documentation/{2}".format(uri, instance_name, file_name),
                json_data,
                requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object(warnings=warnings)


def rename_file(isamAppliance, instance_name, file_name, new_name, type='file', check_mode=False, force=False):
    """
    Renaming a file in the API Access Control documentation root
    """
    exists, warnings = _check_exist(isamAppliance, instance_name, file_name)

    if force is True or exists is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            json_data = {
                "type": type,
                "new_name": new_name
            }

            return isamAppliance.invoke_put(
                "Renaming a file in the API Access Control documentation root",
                "{0}/{1}/documentation/{2}".format(uri, instance_name, file_name),
                json_data,
                requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object(warnings=warnings)


def delete(isamAppliance, instance_name, file_name, check_mode=False, force=False):
    """
    Deleting a file or directory from the API Access Control
    """
    exists, warnings = _check_exist(isamAppliance, instance_name, file_name)

    if force is True or exists is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Deleting a file or directory from the API Access Control",
                "{0}/{1}/documentation/{2}".format(uri, instance_name, file_name),
                requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object(warnings=warnings)


def export_file(isamAppliance, instance_name, file_name, file_path, check_mode=False, force=False):
    """
    Exporting a file in the API Access Control documentation root
    """
    if os.path.exists(file_path) is True:
        warn_str = "File {0} already exists".format(file_path)
        warnings = [warn_str]
        return isamAppliance.create_return_object(warnings=warnings)

    exists, warnings = _check_exist(isamAppliance, instance_name, file_name)

    if force is True or exists is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_get_file(
                "Exporting a file in the API Access Control documentation root",
                "{0}/{1}/documentation/{2}?export=true".format(uri, instance_name, file_name),
                file_path,
                requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object(warnings=warnings)


def import_file(isamAppliance, instance_name, file_path, file_name="", check_mode=False, force=False):
    """
    Importing a file to the API Access Control documentation root
    file_path: location of the file to be uploaded.  for example: /home/user/file1.json
    file_name: name of the directory path and filename in API Documentation Root.  for example: dir/subdir or dir/file1
    """
    if os.path.exists(file_path) is False:
        warn_str = "File {0} already exists".format(file_path)
        warnings = [warn_str]
        return isamAppliance.create_return_object(warnings=warnings)

    same_contents, warnings = _check_contents(isamAppliance=isamAppliance, instance_name=instance_name,
                                              file_name=file_name, file=file_path)

    if force is True or same_contents is False:
        return isamAppliance.invoke_post_files("Importing a file to the API Access Control documentation root",
                                               "{0}/{1}/documentation/{2}?uiCalled=true".format(uri, instance_name,
                                                                                                file_name),
                                               [
                                                   {
                                                       'file_formfield': 'file',
                                                       'filename': file_path,
                                                       'mimetype': 'application/octet-stream'
                                                   }
                                               ],
                                               {
                                                   'type': 'file',
                                                   'force': True
                                               },
                                               requires_version=requires_version)

    return isamAppliance.create_return_object(warnings=warnings)


def _check_instance_exist(isamAppliance, instance_name):
    ret_obj = ibmsecurity.isam.web.api_access_control.resources.get_all_instances(isamAppliance)

    for obj in ret_obj['data']:
        if obj['name'] == instance_name:
            return True, ret_obj['warnings']

    return False, ret_obj['warnings']


def _check_exist(isamAppliance, instance_name, file_name):
    try:
        ret_obj = get(isamAppliance, instance_name, file_name)
        if ret_obj['data'] != []:
            return True, ret_obj['warnings']
        else:
            return False, ret_obj['warnings']

    except Exception as e:
        warnings = ["Exception: {0}".format(e)]
        return False, warnings


def _check_contents(isamAppliance, instance_name, file_name, contents=None, file=None):
    try:
        ret_obj = get(isamAppliance, instance_name, file_name)

        if contents != None:
            if ret_obj['data']['contents'] == contents:
                return True, ret_obj['warnings']
            else:
                return False, ret_obj['warnings']
        elif file != None:
            with open(file, 'rt') as myfile:
                new_contents = myfile.read()
            if ret_obj['data']['contents'] == new_contents:
                return True, ret_obj['warnings']
            else:
                return False, ret_obj['warnings']
        else:
            return False, ret_obj['warnings']

    except Exception as e:
        warnings = ["Exception occurred: {0}.".format(e)]
        return True, warnings


def compare(isamAppliance1, isamAppliance2, instance1_name, instance2_name=None):
    """
    Compare documentation root between two appliances
    """

    if instance2_name is None or instance2_name == '':
        instance2_name = instance1_name

    ret_obj1 = get_all(isamAppliance1, instance1_name)
    ret_obj2 = get_all(isamAppliance2, instance2_name)

    return tools.json_compare(ret_obj1, ret_obj2)
