import logging
import ibmsecurity.utilities.tools
import os.path
import shutil
import zipfile
from ibmsecurity.isam.web.reverse_proxy.management_root import directory
from ibmsecurity.isam.web.reverse_proxy.management_root import file
from ibmsecurity.isam.web.reverse_proxy import instance
from ibmsecurity.utilities.tools import get_random_temp_dir, files_same_zip_content

logger = logging.getLogger(__name__)


def export_zip(isamAppliance, instance_id, filename, check_mode=False, force=False):
    """
    Exporting the contents of the administration pages root as a .zip file

    :param isamAppliance:
    :param instance_id:
    :param filename:
    :param check_mode:
    :param force:
    :return:
    """
    if force is True or os.path.exists(filename) is False:
        if check_mode is False:
            return isamAppliance.invoke_get_file(
                "Exporting the contents of the administration pages root as a .zip file",
                "/wga/reverseproxy/{0}/management_root?index=&name=&enc_name=&type=&browser=".format(instance_id),
                filename=filename, no_headers=True)

    return isamAppliance.create_return_object()


def import_zip(isamAppliance, instance_id, filename, delete_missing=False, check_mode=False, force=False):
    """
    Importing the contents of a .zip file to the administration pages root
    Feature delete_missing will compare import zip with server content and delete missing files in the import zip from server
    """
    warnings = []

    if force is True or _check_import(isamAppliance, instance_id, filename):
        if delete_missing is True:
            tempdir = get_random_temp_dir()
            tempfilename = "management_root.zip"
            tempfile =  os.path.join(tempdir, tempfilename)
            export_zip(isamAppliance, instance_id, tempfile)

            zServerFile = zipfile.ZipFile(tempfile)
            zClientFile = zipfile.ZipFile(filename)

            files_on_server = [];
            for info in zServerFile.infolist():
                files_on_server.append(info.filename)
            files_on_client = [];
            for info in zClientFile.infolist():
                files_on_client.append(info.filename)
            missing_client_files = [x for x in files_on_server if x not in files_on_client]

            if missing_client_files != []:
                logger.info("list all missing files in {}, which will be deleted on the server: {}.".format(filename, missing_client_files))

            for x in missing_client_files:
                if x.endswith('/'):
                    search_dir= os.path.dirname(x[:-1]) + '/'
                    if search_dir not in missing_client_files:
                        logger.debug("delete directory on the server: {0}.".format(x))
                        directory.delete(isamAppliance, instance_id, x, check_mode=check_mode)
                else:
                    search_dir= os.path.dirname(x) + '/'
                    if search_dir not in missing_client_files:
                        logger.debug("delete file on the server: {0}.".format(x))
                        file.delete(isamAppliance, instance_id, x, check_mode=check_mode)
            shutil.rmtree(tempdir)

        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post_files(
                "Importing the contents of a .zip file to the administration pages root",
                 "/wga/reverseproxy/{0}/management_root".format(instance_id),
                [
                    {
                        'file_formfield': 'file',
                        'filename': filename,
                        'mimetype': 'application/octet-stream'
                    }
                ],
                {
                    "force": force
                }, json_response=False)

    return isamAppliance.create_return_object(warnings=warnings)

def _check_import(isamAppliance, instance_id, filename):
    """
    Checks if runtime template zip from server and client differ
    :param isamAppliance:
    :param filename:
    :return:
    """

    if not instance._check(isamAppliance, instance_id):
      logger.info("instance {} does not exist on this server. Skip import".format(instance_id))
      return False

    tempdir = get_random_temp_dir()
    tempfilename = "management_root.zip"
    tempfile =  os.path.join(tempdir, tempfilename)
    export_zip(isamAppliance, instance_id, tempfile)

    identical = files_same_zip_content(filename,tempfile)

    shutil.rmtree(tempdir)
    if identical:
        logger.info("management_root files {} are identical with the server content. No update necessary.".format(filename))
        return False
    else:
        logger.info("management_root files {} differ from the server content. Updating management_root files necessary.".format(filename))
        return True

def check(isamAppliance, instance_id, id, name, type, check_mode=False, force=False):
    ret_obj = None

    if (type.lower() == 'directory'):
        ret_obj = directory._check(isamAppliance, instance_id, id, name)
    elif (type.lower() == 'file'):
        ret_obj = file._check(isamAppliance, instance_id, id, name)
    else:
        type = 'unknown'

    data = {
        'id': ret_obj,
        'top': id,
        'name': name,
        'type': type
    }

    return isamAppliance.create_return_object(data=data)
