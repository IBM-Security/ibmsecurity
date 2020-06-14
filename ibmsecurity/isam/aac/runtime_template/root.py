import logging
import os.path
from ibmsecurity.isam.aac.runtime_template import directory
from ibmsecurity.isam.aac.runtime_template import file

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


def import_file(isamAppliance, filename, check_mode=False, force=False):
    """
    Replace all Runtime Template Files
    """
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


def check(isamAppliance, id, type, check_mode=False, force=False):
    ret_obj = None

    if (type.lower() == 'directory'):
        ret_obj = directory._check(isamAppliance, id)
    elif (type.lower() == 'file'):
        ret_obj = file._check(isamAppliance, id)
    else:
        type = 'unknown'

    name = os.path.basename(id)
    path = os.path.dirname(id)

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
        return file.delete(isamAppliance, id)
