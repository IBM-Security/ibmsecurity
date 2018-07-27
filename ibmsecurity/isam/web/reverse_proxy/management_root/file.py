import logging
import ibmsecurity.utilities.tools
import os.path
from ibmsecurity.utilities.tools import files_same, get_random_temp_dir
import shutil

logger = logging.getLogger(__name__)


def get_all(isamAppliance, instance_id, check_mode=False, force=False):
    """
    Retrieving the current administration pages root contents
    """
    return isamAppliance.invoke_get("Retrieving the current administration pages root contents",
                                    "/wga/reverseproxy/{0}/management_root?recursive=yes".format(instance_id))


def get(isamAppliance, instance_id, id, check_mode=False, force=False):
    """
    Retrieving the contents of a file in the administration pages root
    """
    return isamAppliance.invoke_get("Retrieving the contents of a file in the administration pages root",
                                    "/wga/reverseproxy/{0}/management_root/{1}".format(instance_id, id))


def _check(isamAppliance, instance_id, id, name):
    ret_obj = get_all(isamAppliance, instance_id)

    file_name = os.path.join(id, name)

    return _parse_id(ret_obj['data'], file_name)


def _check_file(isamAppliance, instance_id, id):
    """
    Check whether file exists
    :param isamAppliance:
    :param instance_id:
    :param id:
    :return: True/False
    """
    ret_obj = get(isamAppliance, instance_id, id)

    logger.info(ret_obj['data'])

    if ret_obj['rc'] == 0:
        return True
    else:
        return False


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


def create(isamAppliance, instance_id, id, name, contents=None, check_mode=False, force=False):
    """
    Creating a file in the administration pages root

    :param isamAppliance:
    :param instance_id:
    :param id:
    :param name:
    :param contents:
    :param check_mode:
    :param force:
    :return:
    """
    if force is True or _check(isamAppliance, instance_id, id, name) == None:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post(
                "Creating a file in the administration pages root",
                "/wga/reverseproxy/{0}/management_root/{1}".format(instance_id, id),
                {
                    'file_name': name,
                    'type': 'file',
                    'contents': contents
                })

    return isamAppliance.create_return_object()


def update(isamAppliance, instance_id, id, filename=None, contents=None, check_mode=False, force=False):
    """
    Update a file in the administration pages root
    :param isamAppliance:
    :param instance_id:
    :param id:
    :param name:
    :param contents:
    :param check_mode:
    :param force:
    :return:
    """

    if force is True or _check_file(isamAppliance, instance_id, id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            if filename is not None:
                return isamAppliance.invoke_put_files(
                    "Update a file in the administration page root",
                    "/wga/reverseproxy/{0}/management_root/{1}".format(instance_id, id),
                    [
                        {
                            'file_formfield': 'file',
                            'filename': filename,
                            'mimetype': 'application/octet-stream'
                        }
                    ],
                    {
                        'file': filename,
                        'type': 'file'
                    })
            elif contents is not None:
                return isamAppliance.invoke_put_files(
                    "Update a file in the administration page root",
                    "/wga/reverseproxy/{0}/management_root/{1}".format(instance_id, id),
                    {
                        'contents': contents,
                        'type': 'file'
                    })
            else:
                return isamAppliance.create_return_object(
                    warnings=["Either contents or filename parameter need to be provided. Skipping update request."])


def delete(isamAppliance, instance_id, id, check_mode=False, force=False):
    """
    Deleting a file in the administration pages root

    :param isamAppliance:
    :param instance_id:
    :param id:
    :param check_mode:
    :param force:
    :return:
    """
    if force is True or _check(isamAppliance, instance_id, id, '') != None:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Deleting a file in the administration pages root",
                "/wga/reverseproxy/{0}/management_root/{1}".format(instance_id, id))

    return isamAppliance.create_return_object()


def rename(isamAppliance, instance_id, id, new_name, check_mode=False, force=False):
    """
    Deleting a file in the administration pages root

    :param isamAppliance:
    :param instance_id:
    :param id:
    :param new_name:
    :param check_mode:
    :param force:
    :return:
    """
    file_id = None
    if force is False:
        file_id = _check(isamAppliance, instance_id, id, '')

    if force is True or file_id != None:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Renaming a file in the administration pages root",
                "/wga/reverseproxy/{0}/management_root/{1}".format(instance_id, id),
                {
                    'id': file_id,
                    'new_name': new_name,
                    'type': 'file'
                })

    return isamAppliance.create_return_object()


def export_file(isamAppliance, instance_id, id, filename, check_mode=False, force=False):
    """
    Exporting a file in the administration pages root

    :param isamAppliance:
    :param instance_id:
    :param id:
    :param filename:
    :param check_mode:
    :param force:
    :return:
    """
    if force is True or (_check(isamAppliance, instance_id, id, name='') is not None):
        if check_mode is False:
            return isamAppliance.invoke_get_file(
                "Exporting a file in the administration pages root",
                "/wga/reverseproxy/{0}/management_root/{1}?export=true".format(instance_id, id), filename)

    return isamAppliance.create_return_object()


def _check_import(isamAppliance, instance_id, id, filename, check_mode=False):
    """
    Checks if file on the Appliance (id) exists and if so, whether it is different from filename
    :param isamAppliance:
    :param instance_id:
    :param id:
    :param filename:
    :return:
    """
    tmpdir = get_random_temp_dir()
    tmp_original_file = os.path.join(tmpdir, os.path.basename(id))
    if (_check(isamAppliance, instance_id, id, '') is not None):
        export_file(isamAppliance, instance_id, id, tmp_original_file, check_mode=False, force=True)
        logger.debug("file already exists on appliance")
        if files_same(tmp_original_file, filename):
            logger.debug("files are the same, so we don't want to do anything")
            shutil.rmtree(tmpdir)
            return False
        else:
            logger.debug("files are different, so we delete existing file in preparation for import")
            delete(isamAppliance, instance_id, id, check_mode=check_mode, force=True)
            shutil.rmtree(tmpdir)
            return True
    else:
        logger.debug("file does not exist on appliance, so we'll want to import")
        shutil.rmtree(tmpdir)
        return True


def import_file(isamAppliance, instance_id, id, filename, check_mode=False, force=False):
    """
    Importing a file in the administration pages root.
    Note that _check_import() checks that the file (id) is present and if so, whether it is
    the same and the one being imported.  If it's the same, there is no need to import the new file.
    """
    if force is True or _check_import(isamAppliance, instance_id, id, filename, check_mode=check_mode):
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post_files(
                "Importing a file in the administration pages root",
                "/wga/reverseproxy/{0}/management_root/{1}".format(instance_id, id),
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

    return isamAppliance.create_return_object()


def compare(isamAppliance1, isamAppliance2, instance_id):
    ret_obj1 = get_all(isamAppliance1, instance_id)
    ret_obj2 = get_all(isamAppliance2, instance_id)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
