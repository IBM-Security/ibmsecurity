import logging
import os.path
from ibmsecurity.utilities.tools import files_same, get_random_temp_dir
import shutil

requires_modules = ["wga"]
requires_version = "9.0.6.0"

logger = logging.getLogger(__name__)


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieving all Rate Limiting policies
    """
    return isamAppliance.invoke_get("Retrieving all Rate limiting policies",
                                    "/wga/ratelimiting",
                                    requires_modules=requires_modules,
                                    requires_version=requires_version)


def get(isamAppliance, id, check_mode=False, force=False):
    """
    Retrieve a Rate Limiting policy
    """
    return isamAppliance.invoke_get("Retrieve a Rate Limiting policy",
                                    "/wga/ratelimiting/{0}".format(id),
                                    requires_modules=requires_modules,
                                    requires_version=requires_version)


def add(isamAppliance, id, content, check_mode=False, force=False):
    """
    Add a new Rate Limiting Policy
    """
    if force is True or _check(isamAppliance, id) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post(
                "Add a new Rate Limiting policy",
                "/wga/ratelimiting",
                {
                    "name": id,
                    "content": content
                },
                requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object()


def delete(isamAppliance, id, check_mode=False, force=False):
    """
    Deleting a Rate Limiting policy
    """
    if force is True or _check(isamAppliance, id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Delete a Rate Limiting policy",
                "/wga/ratelimiting/{0}".format(id),
                requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object()


def rename(isamAppliance, id, new_name, check_mode=False, force=False):
    """
    Rename a Rate Limiting policy
    """
    if force is True or _check(isamAppliance, id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Rename a Rate Limiting policy",
                "/wga/ratelimiting/{0}".format(id),
                {
                    'id': id,
                    'new_name': new_name
                },
                requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object()


def update(isamAppliance, id, content, check_mode=False, force=False):
    """
    Update a Rate Limiting policy
    """
    if force is True or _check(isamAppliance, id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Update a Rate Limiting policy",
                "/wga/ratelimiting/{0}".format(id),
                {
                    'id': id,
                    'content': content
                },
                requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object()


def export_file(isamAppliance, id, filename, check_mode=False, force=False):
    """
    Exporting a Rate Limiting policy
    """
    if force is True or _check(isamAppliance, id) is True:
        if check_mode is False:  # No point downloading a file if in check_mode
            return isamAppliance.invoke_get_file(
                "Export a Rate Limiting policy",
                "/wga/ratelimiting/{0}?export".format(id),
                filename,
                requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object()


def import_file(isamAppliance, id, filename, check_mode=False, force=False):
    """
    Importing a Rate Limiting policy
    """
    if force is True or _check_import(isamAppliance, id, filename, check_mode=check_mode):
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post_files(
                "Importing a Rate Limiting policy",
                "/wga/ratelimiting",
                [
                    {
                        'file_formfield': 'file',
                        'filename': filename,
                        'mimetype': 'application/octet-stream'
                    }
                ],
                {},
                requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object()


def _check(isamAppliance, id):
    """
    Check if rate limiting file already exists
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
    Compare Rate Limiting policy between two appliances
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
