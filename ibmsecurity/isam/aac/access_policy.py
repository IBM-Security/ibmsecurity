import logging
from ibmsecurity.utilities import tools
from io import open

logger = logging.getLogger(__name__)

# URI for this module
uri = "/iam/access/v8/access-policies/"
requires_modules = ["federation", "mga"]
requires_version = "9.0.4.0"


def get_all(isamAppliance, sortBy=None, count=None, start=None, filter=None, check_mode=False, force=False):
    """
    Retrieve a list of access policies
    """
    return isamAppliance.invoke_get("Retrieve a list of access policies", "{0}{1}".format(uri,
                                                                                          tools.create_query_string(
                                                                                              sortBy=sortBy,
                                                                                              count=count, start=start,
                                                                                              filter=filter)),
                                    requires_modules=requires_modules, requires_version=requires_version)


def get(isamAppliance, name, check_mode=False, force=False):
    """
    Retrieve a specific access policy
    """
    ret_obj = search(isamAppliance, name, check_mode, force)

    warnings = []
    if ret_obj['data'] == {}:
        return isamAppliance.create_return_object(warnings=["Access policy with name {} not found.".format(name)])
    else:
        return _get(isamAppliance, ret_obj['data'])


def _get(isamAppliance, access_policy_id):
    """
    Internal function to get data using "id" - used to avoid extra calls
    """
    return isamAppliance.invoke_get("Retrieve a specific access policy", "{0}{1}".format(uri, access_policy_id),
                                    requires_modules=requires_modules, requires_version=requires_version)


def search(isamAppliance, name, check_mode=False, force=False):
    """
    Search access policy by name
    """
    ret_obj = get_all(isamAppliance, check_mode=check_mode, force=force)

    return_obj = isamAppliance.create_return_object()

    for obj in ret_obj['data']:
        if obj['name'] == name:
            return_obj['data'] = obj['id']
            logger.debug("Found id: {0}".format(obj['id']))
            return_obj['rc'] = 0

    return return_obj


def set(isamAppliance, name, file=None, content=None, type='JavaScript', category='OIDC', check_mode=False,
        force=False):
    """
    Creating or Modifying an Access Policy
    """
    if content is None or content == '':
        if file is None or file == '':
            return isamAppliance.create_return_object(
                warnings=["Need to pass content or file for set() to work."])
        else:
            with open(file, 'r') as contentFile:
                content = contentFile.read()
    ret_obj = search(isamAppliance, name=name)
    if ret_obj['data'] == {}:
        # Force the add - we already know connection does not exist
        return add(isamAppliance, name=name, content=content, category=category, type=type,
                   check_mode=check_mode, force=True)
    else:
        # Update request
        return update(isamAppliance, name=name, content=content, check_mode=check_mode, force=force)


def add(isamAppliance, name, content, type="JavaScript", category="OIDC", check_mode=False, force=False):
    """
    Create a new access policy
    """
    ret_obj = search(isamAppliance, name)
    if force is True or ret_obj['data'] == {}:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post(
                "Create a new access policy", uri,
                {
                    "name": name,
                    "type": type,
                    "content": content,
                    "category": category
                }, requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()


def delete(isamAppliance, name, check_mode=False, force=False):
    """
    Delete an access policy
    """
    if force is False:
        ret_obj = search(isamAppliance, name)

    if force is True or ret_obj['data'] != {}:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Delete an access policy",
                "{}{}".format(uri, ret_obj['data']), requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object()


def update(isamAppliance, name, content, check_mode=False, force=False):
    """
    Update a specified access policy
    """
    update_required = False
    ret_obj = search(isamAppliance, name)
    id = ret_obj['data']
    if force is False:
        if id:
            ret_obj_content = _get(isamAppliance, id)
            # Having to strip whitespace to get a good comparison (suspect carriage returns added after save happens)
            if (ret_obj_content['data']['properties']['content']).strip() != (content).strip():
                update_required = True

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Update a specified access policy",
                "{}{}".format(uri, id),
                {
                    'content': content
                }, requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()


def export_file(isamAppliance, name, filename, check_mode=False, force=False):
    """
    Export a specific access policy
    """
    import os.path
    if force is False:
        ret_obj = search(isamAppliance, name)

    if force is True or (ret_obj['data'] != {} and os.path.exists(filename) is False):
        if check_mode is False:  # No point downloading a file if in check_mode
            id = ret_obj['data']
            return isamAppliance.invoke_get_file(
                "Export a specific access policy",
                "{}{}/file".format(uri, id),
                filename, requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()


def upload(isamAppliance, name, file, type='JavaScript', category="OIDC", check_mode=False, force=False):
    """
    Import a new access policy
    """
    ret_obj = search(isamAppliance, name)
    if force is True or ret_obj['data'] == {}:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post_files(
                "Import a new access policy", uri,
                [
                    {
                        'file_formfield': 'file',
                        'filename': file,
                        'mimetype': 'application/octet-stream'
                    }
                ],
                {
                    "name": name,
                    "type": type,
                    "category": category
                }, requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()


def import_file(isamAppliance, name, file, check_mode=False, force=False):
    """
    Import a access policy
    """
    update_required = False
    if force is False:
        ret_obj = search(isamAppliance, name)
        if ret_obj['data'] != {}:
            ret_obj_content = _get(isamAppliance, ret_obj['data'])
            with open(file, 'r') as infile:
                content = infile.read()
            if (ret_obj_content['data']['properties']['content']).strip() != content.strip():
                update_required = True

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post_files(
                "Import a access policy",
                "{}{}/file".format(uri, ret_obj['data']),
                [
                    {
                        'file_formfield': 'file',
                        'filename': file,
                        'mimetype': 'application/file'
                    }
                ],
                {}, requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()


def compare(isamAppliance1, isamAppliance2):
    """
    Compare access policies between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    for obj in ret_obj1['data']:
        obj = _get(isamAppliance1, obj['id'])['data']
        del obj['id']
    for obj in ret_obj2['data']:
        obj = _get(isamAppliance2, obj['id'])['data']
        del obj['id']

    return tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['id'])
