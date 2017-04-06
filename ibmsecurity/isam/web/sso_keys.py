import logging
import os.path
from ibmsecurity.utilities.tools import files_same, get_random_temp_dir
import shutil

logger = logging.getLogger(__name__)


def get(isamAppliance, check_mode=False, force=False):
    """
    Listing all current SSO key files
    """
    return isamAppliance.invoke_get("Listing all current SSO key files",
                                    "/wga/sso_key")


def add(isamAppliance, ssokey_name, check_mode=False, force=False):
    """
    Creating an SSO key file
    """
    if force is True or _check(isamAppliance, ssokey_name) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post(
                "Creating an SSO key file",
                "/wga/sso_key",
                {
                    "ssokey_name": ssokey_name
                })

    return isamAppliance.create_return_object()


def delete(isamAppliance, id, check_mode=False, force=False):
    """
    Deleting an SSO key file
    """
    if force is True or _check(isamAppliance, id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Deleting an SSO key file",
                "/wga/sso_key/{0}".format(id))

    return isamAppliance.create_return_object()


def export_key(isamAppliance, id, filename, check_mode=False, force=False):
    """
    Exporting an SSO key file
    """

    if force is True or _check(isamAppliance, id) is True:
        if check_mode is False:  # No point downloading a file if in check_mode
            return isamAppliance.invoke_get_file(
                "Export an SSO key file",
                "/wga/sso_key/{0}?export".format(id),
                filename)

    return isamAppliance.create_return_object()


def import_key(isamAppliance, id, filename, check_mode=False, force=False):
    """
    Importing an SSO key file
    """
    if force is True or _check_import(isamAppliance, id, filename, check_mode=check_mode):
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post_files(
                "Importing an SSO key file",
                "/wga/sso_key",
                [
                    {
                        'file_formfield': 'sso_keyfile',
                        'filename': filename,
                        'mimetype': 'application/octet-stream'
                    }
                ],
                {})

    return isamAppliance.create_return_object()


def _check(isamAppliance, id):
    """
    Check if SSO Key already exists
    """
    ret_obj = get(isamAppliance)

    for obj in ret_obj['data']:
        if obj['id'] == id:
            return True

    return False


def _check_import(isamAppliance, id, filename, check_mode=False):
    """
    Checks if key on the Appliance exists and if so, whether it is different from filename
    """
    tmpdir = get_random_temp_dir()
    tmp_original_file = os.path.join(tmpdir, os.path.basename(id))
    if _check(isamAppliance, id):
        export_key(isamAppliance, id, tmp_original_file, check_mode=False, force=True)
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


def compare(isamAppliance1, isamAppliance2):
    """
    Compare SSO keys between two appliances
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    for obj in ret_obj1['data']:
        del obj['version']
    for obj in ret_obj2['data']:
        del obj['version']

    import ibmsecurity.utilities.tools
    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['version'])
