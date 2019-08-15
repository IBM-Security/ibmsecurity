import logging
import os.path
from ibmsecurity.utilities.tools import files_same, get_random_temp_dir
import shutil

logger = logging.getLogger(__name__)


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieving all URL Mapping
    """
    return isamAppliance.invoke_get("Retrieving all URL Mapping",
                                    "/wga/dynurl_config")


def get(isamAppliance, id, check_mode=False, force=False):
    """
    Retrieve a URL Mapping
    """
    return isamAppliance.invoke_get("Retrieve a URL Mapping",
                                    "/wga/dynurl_config/{0}".format(id))


def _get_template(isamAppliance):
    """
    Retrieve a URL Mapping Template
    """
    return isamAppliance.invoke_get("Retrieve a URL Mapping Template",
                                    "/wga_templates/dynurl_template.json")


def export_template(isamAppliance, filename, check_mode=False, force=False):
    """
    Exporting the DynURL configuration file template
    """

    if os.path.exists(filename) is True:
        logger.info("File '{0}' already exists.  Skipping export.".format(filename))
        return isamAppliance.create_return_object()

    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:
        return isamAppliance.invoke_get_file(
            "Exporting the DynURL configuration file template",
            "/wga_templates/dynurl_template?export",
            filename)

    return isamAppliance.create_return_object()


def add(isamAppliance, name, dynurl_config_data=None, check_mode=False, force=False):
    """
    Add a URL Mapping
    """
    # Add default template if not specified
    if dynurl_config_data is None:
        ret_obj = _get_template(isamAppliance)
        dynurl_config_data = ret_obj['data']['id']

    if force is True or _check(isamAppliance, name) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post(
                "Add a URL Mapping",
                "/wga/dynurl_config",
                {
                    "name": name,
                    "dynurl_config_data": dynurl_config_data
                })

    return isamAppliance.create_return_object()


def delete(isamAppliance, id, check_mode=False, force=False):
    """
    Deleting a URL Mapping
    """
    if force is True or _check(isamAppliance, id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Delete a URL Mapping",
                "/wga/dynurl_config/{0}".format(id))

    return isamAppliance.create_return_object()


def rename(isamAppliance, id, new_name, check_mode=False, force=False):
    """
    Rename a URL Mapping
    """
    if force is True or _check(isamAppliance, id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Rename a URL Mapping",
                "/wga/dynurl_config/{0}".format(id),
                {
                    'id': id,
                    'new_name': new_name
                })

    return isamAppliance.create_return_object()


def update(isamAppliance, id, dynurl_config_data, check_mode=False, force=False):
    """
    Update a URL Mapping
    """
    if force is True or _check(isamAppliance, id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Update a URL Mapping",
                "/wga/dynurl_config/{0}".format(id),
                {
                    'id': id,
                    'dynurl_config_data': dynurl_config_data
                })

    return isamAppliance.create_return_object()


def export_file(isamAppliance, id, filename, check_mode=False, force=False):
    """
    Exporting a URL Mapping
    """
    if force is True or _check(isamAppliance, id) is True:
        if check_mode is False:  # No point downloading a file if in check_mode
            return isamAppliance.invoke_get_file(
                "Export a URL Mapping",
                "/wga/dynurl_config/{0}?export".format(id),
                filename)

    return isamAppliance.create_return_object()


def import_file(isamAppliance, id, filename, check_mode=False, force=False):
    """
    Importing a URL Mapping
    """
    if force is True or _check_import(isamAppliance, id, filename, check_mode=check_mode):
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post_files(
                "Importing a URL Mapping",
                "/wga/dynurl_config.js",
                [
                    {
                        'file_formfield': 'dynurl_config_file',
                        'filename': filename,
                        'mimetype': 'application/octet-stream'
                    }
                ],
                {})

    return isamAppliance.create_return_object()


def _check(isamAppliance, id):
    """
    Check if URL Mapping already exists
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
    Compare URL Mapping between two appliances
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
