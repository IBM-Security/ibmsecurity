import logging
import os.path
import zipfile
import shutil
from ibmsecurity.isam.aac.runtime_template import directory
from ibmsecurity.isam.aac.runtime_template import file
from ibmsecurity.utilities.tools import get_random_temp_dir, files_same_zip_content

logger = logging.getLogger(__name__)

uri = "/mga/template_files"

requires_modules = ["mga", "federation"]
requires_version = None


def export_file(isamAppliance, filename, check_mode=False, force=False):
    """
    Export all Runtime Template Files
    """
    import os.path

    if force is True or os.path.exists(filename) is False:
        if check_mode is False:  # No point downloading a file if in check_mode
            return isamAppliance.invoke_get_file(
                "Export all Runtime Template Files",
                "{0}/?export=true".format(uri),
                filename, no_headers=True, requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object()


def import_file(isamAppliance, filename, delete_missing=False, check_mode=False, force=False):
    """
    Import all Runtime Template Files with sync capability
    If delete_missing=True also sync provided file as master with the server.
    This will delete files on the server that exist there but are missing in the provided zip file
    To use import_file in additive mode, leave delete_missing=False
    """

    warnings = []

    if force is True or _check_import(isamAppliance, filename):
        if delete_missing is True:
            tempdir = get_random_temp_dir()
            tempfilename = "template_files.zip"
            tempfile =  os.path.join(tempdir, tempfilename)
            export_file(isamAppliance, tempfile)

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
                        delete(isamAppliance, x, "directory", check_mode=check_mode)
                else:
                    search_dir= os.path.dirname(x) + '/'
                    if search_dir not in missing_client_files:
                        logger.debug("delete file on the server: {0}.".format(x))
                        delete(isamAppliance, x, "file", check_mode=check_mode)
            zServerFile.close()
            shutil.rmtree(tempdir)

        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post_files(
                "Replace all Runtime Template Files",
                uri,
                [
                    {
                        'file_formfield': 'file',
                        'filename': filename,
                        'mimetype': 'application/octet-stream'
                    }
                ],
                {
                    "force": force
                }, json_response=False, requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object(warnings=warnings)

def _check_import(isamAppliance, filename):
    """
    Checks if runtime template zip from server and client differ
    :param isamAppliance:
    :param filename:
    :return:
    """

    tempdir = get_random_temp_dir()
    tempfilename = "template_files.zip"
    tempfile =  os.path.join(tempdir, tempfilename)
    export_file(isamAppliance, tempfile)

    if os.path.exists(tempfile):
      identical = files_same_zip_content(filename,tempfile)

      shutil.rmtree(tempdir)
      if identical:
          logger.info("runtime template files {} are identical with the server content. No update necessary.".format(filename))
          return False
      else:
          logger.info("runtime template files {} differ from the server content. Updating runtime template files necessary.".format(filename))
          return True
    else:
      logger.info("missing zip file from server. Comparison skipped.")
      return False

def check(isamAppliance, id, type, check_mode=False, force=False):
    ret_obj = None

    name = os.path.basename(id)
    path = os.path.dirname(id)

    if (type.lower() == 'directory'):
        ret_obj = directory._check(isamAppliance, id)
    elif (type.lower() == 'file'):
        ret_obj = file._check(isamAppliance, path, name)
    else:
        type = 'unknown'

    data = {
        'id': ret_obj,
        'path': path,
        'name': name,
        'type': type
    }

    return isamAppliance.create_return_object(data=data)


def delete(isamAppliance, id, type, check_mode=False, force=False):
    """
    Deleting a file or directory in the runtime template files directory

    :param isamAppliance:
    :param id:
    :param_type:
    :param check_mode:
    :param force:
    :return:
    """
    if (type.lower() == 'directory'):
        return directory.delete(isamAppliance, id)
    elif (type.lower() == 'file'):
        name = os.path.basename(id)
        path = os.path.dirname(id)
        return file.delete(isamAppliance, path, name)
