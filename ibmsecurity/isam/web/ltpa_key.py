import logging

logger = logging.getLogger(__name__)


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieving all current LTPA Key files
    """
    return isamAppliance.invoke_get("Retrieving all LTPA Keys",
                                    "/wga/ltpa_key")


def delete(isamAppliance, id, check_mode=False, force=False):
    """
    Deleting a LTPA Key file
    """
    if force is True or _check(isamAppliance, id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Delete a LTPA key file",
                "/wga/ltpa_key/{0}".format(id))

    return isamAppliance.create_return_object()


def rename(isamAppliance, id, new_name, check_mode=False, force=False):
    """
    Rename a LTPA key file
    """
    if force is True or _check(isamAppliance, id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Rename a LTPA Key file",
                "/wga/ltpa_key/{0}".format(id),
                {
                    'id': id,
                    'new_name': new_name
                })

    return isamAppliance.create_return_object()


def export_key(isamAppliance, id, filename, check_mode=False, force=False):
    """
    Exporting a LTPA Key
    """
    import os.path

    if force is True or (_check(isamAppliance, id) is True and os.path.exists(filename) is False):
        if check_mode is False:  # No point downloading a file if in check_mode
            return isamAppliance.invoke_get_file(
                "Export a LTPA key file",
                "/wga/ltpa_key/{0}?export".format(id),
                filename)

    return isamAppliance.create_return_object()


def import_key(isamAppliance, id, ltpa_keyfile, check_mode=False, force=False):
    """
    Importing a LTPA key file
    """
    if force is True or _check(isamAppliance, id) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post_files(
                "Importing a LTPA key file",
                "/wga/ltpa_key/",
                [
                    {
                        'file_formfield': 'ltpa_keyfile',
                        'filename': ltpa_keyfile,
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


def compare(isamAppliance1, isamAppliance2):
    """
    Compare URL Mapping between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    for obj in ret_obj1['data']:
        del obj['version']
    for obj in ret_obj2['data']:
        del obj['version']

    import ibmsecurity.utilities.tools
    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['version'])
