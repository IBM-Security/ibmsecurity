import logging

logger = logging.getLogger(__name__)


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieving all Junction Mapping
    """
    return isamAppliance.invoke_get("Retrieving all Junction Mapping",
                                    "/wga/jmt_config")


def get(isamAppliance, id, check_mode=False, force=False):
    """
    Retrieve a Junction Mapping
    """
    return isamAppliance.invoke_get("Retrieve a Junction Mapping",
                                    "/wga/jmt_config/{0}".format(id))


def _get_template(isamAppliance):
    """
    Retrieve a Junction Mapping Template
    """
    return isamAppliance.invoke_get("Retrieve a Junction Mapping Template",
                                    "/isam/wga_templates/jmt_template.json")


def add(isamAppliance, id, jmt_config_data=None, check_mode=False, force=False):
    """
    Add a Junction Mapping
    """
    # Add default template if not specified
    if jmt_config_data is None:
        ret_obj = _get_template(isamAppliance)
        jmt_config_data = ret_obj['data']['id']

    if force is True or _check(isamAppliance, id) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post(
                "Add a Junction Mapping",
                "/wga/jmt_config",
                {
                    "name": id,
                    "jmt_config_data": jmt_config_data
                })

    return isamAppliance.create_return_object()


def delete(isamAppliance, id, check_mode=False, force=False):
    """
    Deleting a Junction Mapping
    """
    if force is True or _check(isamAppliance, id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Delete a Junction Mapping",
                "/wga/jmt_config/{0}".format(id))

    return isamAppliance.create_return_object()


def rename(isamAppliance, id, new_name, check_mode=False, force=False):
    """
    Rename a Junction Mapping
    """
    if force is True or _check(isamAppliance, id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Rename a Junction Mapping",
                "/wga/jmt_config/{0}".format(id),
                {
                    'id': id,
                    'new_name': new_name
                })

    return isamAppliance.create_return_object()


def update(isamAppliance, id, jmt_config_data, check_mode=False, force=False):
    """
    Update a Junction Mapping
    """
    warnings = []
    update_required = False
    ret_obj_content = get(isamAppliance, id)
    if ret_obj_content['data'] == {}:
        warnings.append("Junction Mapping {} not found. Skipping update.".format(id))
    # Having to strip whitespace to get a good comparison (suspect carriage returns added after save happens)
    elif (ret_obj_content['data']['contents']).strip() != (jmt_config_data).strip():
        update_required = True

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_put(
                "Update a Junction Mapping",
                "/wga/jmt_config/{0}".format(id),
                {
                    'id': id,
                    'jmt_config_data': jmt_config_data
                }, warnings=warnings)

    return isamAppliance.create_return_object(warnings=warnings)


def export_file(isamAppliance, id, filename, check_mode=False, force=False):
    """
    Exporting a Junction Mapping
    """
    import os.path

    if force is True or (_check(isamAppliance, id) is True and os.path.exists(filename) is False):
        if check_mode is False:  # No point downloading a file if in check_mode
            return isamAppliance.invoke_get_file(
                "Export a Junction Mapping",
                "/wga/jmt_config/{0}?export".format(id),
                filename)

    return isamAppliance.create_return_object()


def export_template(isamAppliance, filename, check_mode=False, force=False):
    """
    Exporting the JMT configuration file template
    """
    import os.path

    if os.path.exists(filename) is True:
        logger.info("File '{0}' already exists. Skipping export.".format(filename))
        return isamAppliance.create_return_object()

    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:
        return isamAppliance.invoke_get_file(
            "Exporting the JMT configuration file template",
            "/isam/wga_templates/jmt_template?export",
            filename)

    return isamAppliance.create_return_object()


def import_file(isamAppliance, id, filename, check_mode=False, force=False):
    """
    Importing a Junction Mapping
    """
    if force is True or _check(isamAppliance, id) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post_files(
                "Importing a Junction Mapping",
                "/wga/jmt_config.js",
                [
                    {
                        'file_formfield': 'jmt_config_file',
                        'filename': filename,
                        'mimetype': 'application/octet-stream'
                    }
                ],
                {})

    return isamAppliance.create_return_object()


def _check(isamAppliance, id):
    """
    Check if Junction Mapping already exists
    """
    ret_obj = get_all(isamAppliance)

    for obj in ret_obj['data']:
        if obj['id'] == id:
            return True

    return False


def compare(isamAppliance1, isamAppliance2):
    """
    Compare Junction Mapping between two appliances
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
