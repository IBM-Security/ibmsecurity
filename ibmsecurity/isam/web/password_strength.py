import logging

logger = logging.getLogger(__name__)


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieving all Password Strength
    """
    return isamAppliance.invoke_get("Retrieving all Password Strength",
                                    "/wga/pwd_strength")


def get(isamAppliance, id, check_mode=False, force=False):
    """
    Retrieve a Password Strength
    """
    return isamAppliance.invoke_get("Retrieve a Password Strength",
                                    "/wga/pwd_strength/{0}".format(id))


def add(isamAppliance, id, check_mode=False, force=False):
    """
    Add a Password Strength
    """
    if force is True or _check(isamAppliance, id) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post(
                "Add a Password Strength",
                "/wga/pwd_strength",
                {
                    "name": id
                })

    return isamAppliance.create_return_object()


def delete(isamAppliance, id, check_mode=False, force=False):
    """
    Deleting a Password Strength
    """
    if force is True or _check(isamAppliance, id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Delete a Password Strength",
                "/wga/pwd_strength/{0}".format(id))

    return isamAppliance.create_return_object()


def rename(isamAppliance, id, new_name, check_mode=False, force=False):
    """
    Rename a Password Strength
    """
    if force is True or _check(isamAppliance, id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Rename a Password Strength",
                "/wga/pwd_strength/{0}".format(id),
                {
                    'id': id,
                    'new_name': new_name
                })

    return isamAppliance.create_return_object()


def update(isamAppliance, id, content, check_mode=False, force=False):
    """
    Update a Password Strength
    """
    if force is True or _check(isamAppliance, id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Update a Password Strength",
                "/wga/pwd_strength/{0}".format(id),
                {
                    'id': id,
                    'content': content
                })

    return isamAppliance.create_return_object()


def export_file(isamAppliance, id, filename, check_mode=False, force=False):
    """
    Exporting a Password Strength
    """
    import os.path

    if force is True or (_check(isamAppliance, id) is True and os.path.exists(filename) is False):
        if check_mode is False:  # No point downloading a file if in check_mode
            return isamAppliance.invoke_get_file(
                "Export a Password Strength",
                "/wga/pwd_strength/{0}?export".format(id),
                filename)

    return isamAppliance.create_return_object()


def import_file(isamAppliance, id, filename, check_mode=False, force=False):
    """
    Importing a Password Strength
    """
    if force is True or _check(isamAppliance, id) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post_files(
                "Importing a Password Strength",
                "/wga/pwd_strength.js",
                [
                    {
                        'file_formfield': 'file',
                        'filename': filename,
                        'mimetype': 'application/octet-stream'
                    }
                ],
                {})

    return isamAppliance.create_return_object()


def _check(isamAppliance, id):
    """
    Check if Password Strength already exists
    """
    ret_obj = get_all(isamAppliance)

    for obj in ret_obj['data']:
        if obj['id'] == id:
            return True

    return False


def compare(isamAppliance1, isamAppliance2):
    """
    Compare Password Strength between two appliances
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
