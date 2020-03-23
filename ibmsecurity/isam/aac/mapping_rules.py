import logging
from io import open

logger = logging.getLogger(__name__)


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieve a list of mapping rules
    """
    return isamAppliance.invoke_get("Retrieve a list of mapping rules",
                                    "/iam/access/v8/mapping-rules")


def get(isamAppliance, name, check_mode=False, force=False):
    """
    Retrieve a specific mapping rule
    """
    ret_obj = search(isamAppliance, name=name)
    id = ret_obj['data']

    if id == {}:
        return isamAppliance.create_return_object()
    else:
        return _get(isamAppliance, id)


def _get(isamAppliance, id):
    """
    Internal function to get data using "id" - used to avoid extra calls

    :param isamAppliance:
    :param id:
    :return:
    """
    return isamAppliance.invoke_get("Retrieve a specific mapping rule",
                                    "/iam/access/v8/mapping-rules/{0}".format(id))


def search(isamAppliance, name, check_mode=False, force=False):
    """
    Search mapping rule by name

    :param isamAppliance:
    :param name:
    :param check_mode:
    :param force:
    :return:
    """
    ret_obj = get_all(isamAppliance, check_mode, force)

    return_obj = isamAppliance.create_return_object()

    for obj in ret_obj['data']:
        if obj['name'] == name:
            return_obj['data'] = obj['id']
            logger.debug("Found id: {0}".format(obj['id']))
            return_obj['rc'] = 0

    return return_obj


def set(isamAppliance, name, category, filename=None, content=None, upload_filename=None, check_mode=False,
        force=False):
    """
    Creating or Modifying an Mapping Rule
    """
    if content is None or content == '':
        if upload_filename is None or upload_filename == '':
            return isamAppliance.create_return_object(
                warnings="Need to pass content or upload_filename for set() to work.")
        else:
            with open(upload_filename, 'r') as contentFile:
                content = contentFile.read()
    if filename is None or filename == '':
        if upload_filename is None or upload_filename == '':
            return isamAppliance.create_return_object(
                warnings="Need to pass filename or upload_filename for set() to work.")
        else:
            filename = _extract_filename(upload_filename)
    if _check(isamAppliance, name=name) is False:
        # Force the add - we already know connection does not exist
        return add(isamAppliance, name=name, filename=filename, content=content, category=category,
                   check_mode=check_mode, force=True)
    else:
        # Update request
        return update(isamAppliance, name=name, content=content, check_mode=check_mode, force=force)


def add(isamAppliance, name, filename=None, content=None, category="OAUTH", check_mode=False, force=False):
    """
    Add a mapping rule
    """
    if force is True or _check(isamAppliance, name) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            if filename is None:
                filename = _extract_filename(name, category)
            return isamAppliance.invoke_post(
                "Add a mapping rule",
                "/iam/access/v8/mapping-rules",
                {
                    "name": name,
                    "fileName": filename,
                    "content": content,
                    "category": category
                })

    return isamAppliance.create_return_object()


def delete(isamAppliance, name, check_mode=False, force=False):
    """
    Delete a mapping rule
    """
    if force is False:
        ret_obj = search(isamAppliance, name)

    if force is True or ret_obj['data'] != {}:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Delete a mapping rule",
                "/iam/access/v8/mapping-rules/{0}".format(ret_obj['data']))

    return isamAppliance.create_return_object()


def update(isamAppliance, name, content, check_mode=False, force=False):
    """
    Update a specified mapping rule
    """
    update_required = False
    ret_obj = search(isamAppliance, name)
    id = ret_obj['data']
    if force is False:
        if id:
            ret_obj_content = _get(isamAppliance, id)
            # Having to strip whitespace to get a good comparison (suspect carriage returns added after save happens)
            if (ret_obj_content['data']['content']).strip() != (content).strip():
                update_required = True

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Update a specified mapping rule",
                "/iam/access/v8/mapping-rules/{0}".format(id),
                {
                    'content': content
                })

    return isamAppliance.create_return_object()


def export_file(isamAppliance, name, filename, check_mode=False, force=False):
    """
    Export a specific mapping rule
    """
    import os.path
    if force is False:
        ret_obj = search(isamAppliance, name)

    if force is True or (ret_obj['data'] != {} and os.path.exists(filename) is False):
        if check_mode is False:  # No point downloading a file if in check_mode
            id = ret_obj['data']
            return isamAppliance.invoke_get_file(
                "Export a specific mapping rule",
                "/iam/access/v8/mapping-rules/{0}/file/".format(id),
                filename)

    return isamAppliance.create_return_object()


def upload(isamAppliance, name, upload_filename, filename=None, category="OAUTH", check_mode=False, force=False):
    """
    Import a new mapping rule
    """
    if force is True or _check(isamAppliance, name) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            if filename is None:
                filename = _extract_filename(upload_filename)

            return isamAppliance.invoke_post_files(
                "Import a new mapping rule",
                "/iam/access/v8/mapping-rules",
                [
                    {
                        'file_formfield': 'file',
                        'filename': upload_filename,
                        'mimetype': 'application/octet-stream'
                    }
                ],
                {
                    "name": name,
                    "filename": filename,
                    "category": category
                })

    return isamAppliance.create_return_object()


def _extract_filename(upload_filename):
    """
    Extract filename from fully qualified path to use if no filename provided
    """
    import os.path
    return os.path.basename(upload_filename)


def import_file(isamAppliance, name, filename, check_mode=False, force=False):
    """
    Import a mapping rule (replace)
    """
    update_required = False
    if force is False:
        ret_obj = search(isamAppliance, name)
        if ret_obj['data'] != {}:
            ret_obj_content = _get(isamAppliance, ret_obj['data'])
            with open(filename, 'r') as infile:
                content = infile.read()
            if (ret_obj_content['data']['content']).strip() != content.strip():
                update_required = True

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post_files(
                "Import a mapping rule (replace)",
                "/iam/access/v8/mapping-rules/{0}/file".format(ret_obj['data']),
                [
                    {
                        'file_formfield': 'file',
                        'filename': filename,
                        'mimetype': 'application/file'
                    }
                ],
                {})

    return isamAppliance.create_return_object()


def _check(isamAppliance, name):
    """
    Check if Mapping Rules already exists
    """
    ret_obj = get_all(isamAppliance)

    for obj in ret_obj['data']:
        if obj['name'] == name:
            return True

    return False


def compare(isamAppliance1, isamAppliance2):
    """
    Compare Mapping Rules between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    for obj in ret_obj1['data']:
        del obj['id']
    for obj in ret_obj2['data']:
        del obj['id']

    import ibmsecurity.utilities.tools
    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['id'])
