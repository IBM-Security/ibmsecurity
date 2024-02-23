import logging
import os.path
from ibmsecurity.utilities.tools import files_same, get_random_temp_dir
import shutil

logger = logging.getLogger(__name__)

uri = "/wga/waf_config"
requires_modules = ["wga"]
requires_version = "10.0.5.0"


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieving all waf rules and data files
    """
    return isamAppliance.invoke_get("Retrieving all waf rules files",
                                    "/wga/waf_config")


def get(isamAppliance, id, check_mode=False, force=False):
    """
    Retrieve a waf file
    """
    return isamAppliance.invoke_get("Retrieve a waf file",
                                    "/wga/waf_config/{0}".format(id))


def add(isamAppliance, id, content, check_mode=False, force=False):
    """
    Add a new WAF rule or data file.
    """
    if force is True or _check(isamAppliance, id) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post(
                "Add a new WAF file",
                "/wga/waf_config",
                {
                    "name": id,
                    "waf_config_data": content
                })

    return isamAppliance.create_return_object()


def delete(isamAppliance, id, check_mode=False, force=False):
    """
    Delete a WAF file.
    """
    if force is True or _check(isamAppliance, id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Delete a WAF file",
                "/wga/waf_config/{0}".format(id))

    return isamAppliance.create_return_object()


def rename(isamAppliance, id, new_name, check_mode=False, force=False):
    """
    Rename a WAF file.
    """
    if force is True or _check(isamAppliance, id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Rename a WAF file",
                "/wga/waf_config/{0}".format(id),
                {
                    'id': id,
                    'new_name': new_name
                })

    return isamAppliance.create_return_object()


def update(isamAppliance, id, content, check_mode=False, force=False):
    """
    Update a WAF file.
    """
    if force is True or _check(isamAppliance, id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Update a WAF file",
                "/wga/waf_config/{0}".format(id),
                {
                    'id': id,
                    'waf_config_data': content
                })

    return isamAppliance.create_return_object()


def update_crs_setup(isamAppliance, content, check_mode=False, force=False):
    """
    Update the crs-setup.conf file.
    """
    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:
        return isamAppliance.invoke_put(
            "Update the crs-setup.conf file",
            "/wga/waf_config/crs-setup.conf",
            {
                'id': 'crs-setup.conf',
                'waf_config_data': content
            })

    return isamAppliance.create_return_object()


def export_file(isamAppliance, id, filename, check_mode=False, force=False):
    """
    Export a WAF file.
    """
    if force is True or _check(isamAppliance, id) is True:
        if check_mode is False:  # No point downloading a file if in check_mode
            return isamAppliance.invoke_get_file(
                "Export a WAF file",
                "/wga/waf_config/{0}?export".format(id),
                filename)

    return isamAppliance.create_return_object()


def export_crs_setup_file(isamAppliance, filename, check_mode=False, force=False):
    """
    Export the crs_setup.conf file.
    """
    if check_mode is False:  # No point downloading a file if in check_mode
        logger.debug("Entered export stage.")
        return isamAppliance.invoke_get_file(
            "Export the crs-setup.conf file",
            "/wga/waf_config/crs-setup.conf?export", filename)

    return isamAppliance.create_return_object()


def import_file(isamAppliance, id, filename, check_mode=False, force=False):
    """
    Import a WAF file.
    """
    if force is True or _check_import(isamAppliance, id, filename, check_mode=check_mode):
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post_files(
                "Importing a WAF file",
                "/wga/waf_config",
                [
                    {
                        'file_formfield': 'waf_config_file',
                        'filename': filename,
                        'mimetype': 'application/octet-stream'
                    }
                ],
                {})

    return isamAppliance.create_return_object()

def export_zip(isamAppliance, filename, check_mode=False, force=False):
    """
    Export the WAF rules and data files as a .zip file
    """
    if force is True or os.path.exists(filename) is False:
        if check_mode is False:
            uri = "/wga/waf_config?export=zip"
            return isamAppliance.invoke_get_file(
                "Exporting WAF rules as a .zip file", uri, filename)

    return isamAppliance.create_return_object()


def _check(isamAppliance, id):
    """
    Check if WAF file already exists
    """
    ret_obj = get_all(isamAppliance)

    for obj in ret_obj['data']:
        if obj['id'] == id:
            return True

    return False


def _check_import(isamAppliance, id, filename, check_mode=False):
    """
    Checks if file on the Appliance exists and if so, whether it is different from filename
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


def compare(isamAppliance1, isamAppliance2):
    """
    Compare WAF files between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    for obj in ret_obj1['data']:
        del obj['version']
        ret_obj = get(isamAppliance1, obj['id'])
        obj['script'] = ret_obj['data']['contents']
    for obj in ret_obj2['data']:
        del obj['version']
        ret_obj = get(isamAppliance2, obj['id'])
        obj['script'] = ret_obj['data']['contents']

    import ibmsecurity.utilities.tools
    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['version'])
