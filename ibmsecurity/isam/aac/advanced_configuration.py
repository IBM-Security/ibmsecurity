import logging

logger = logging.getLogger(__name__)

# URI for this module
uri = "/iam/access/v8/override-configs"
requires_modules = ["mga", "federation"]
requires_version = None
mga_uri = "/mga/advanced_config/files"


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieve a list of configuration properties
    """
    return isamAppliance.invoke_get("Retrieve a list of configuration properties",
                                    "/iam/access/v8/override-configs", requires_modules=requires_modules,
                                    requires_version=requires_version)


def get(isamAppliance, key, check_mode=False, force=False):
    """
    Retrieve a specific configuration property
    """
    ret_obj = search(isamAppliance, key=key)
    id = ret_obj['data']

    if id == {}:
        return isamAppliance.create_return_object()
    else:
        return isamAppliance.invoke_get("Retrieve a specific configuration property",
                                        "/iam/access/v8/override-configs/{0}".format(id),
                                        requires_modules=requires_modules, requires_version=requires_version)


def update(isamAppliance, key, value, sensitive, check_mode=False, force=False):
    """
    Update a configuration property
    """
    id, matches = None, None
    if force is False:
        id, matches = _check(isamAppliance, key, value, sensitive)

    if force is True or (matches is False and id is not None):
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Update a configuration property",
                "/iam/access/v8/override-configs/{0}".format(id),
                {
                    'value': value,
                    'sensitive': sensitive
                }, requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()


def update_all(isamAppliance, values, check_mode=False, force=False):
    """
    Update a list of configuration properties

    Unlike the REST API use key values instead of id
    """
    matches, vals = None, values
    if force is False:
        matches, vals = _check_values(isamAppliance, values)

    if force is True or matches is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Update a list of configuration properties",
                "/iam/access/v8/override-configs",
                vals, requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()


def get_files(isamAppliance, path, check_mode=False, force=False):
    """
    Retrieving a list of configuration files
    :param isamAppliance:
    :param check_mode:
    :param force:
    :return:
    """
    return isamAppliance.invoke_get("Retrieving a list of configuration files",
                                    "{0}/{1}".format(mga_uri, path),
                                    requires_modules=requires_modules, requires_version="10.0.0")


def get_paths(isamAppliance, check_mode=False, force=False):
    """
    Retrieving a list of configuration file component paths
    :param isamAppliance:
    :param check_mode:
    :param force:
    :return:
    """
    return isamAppliance.invoke_get("Retrieving a list of configuration file component paths",
                                    "{0}".format(mga_uri),
                                    requires_modules=requires_modules, requires_version="10.0.0")


def get_contents(isamAppliance, path, filename, check_mode=False, force=False):
    """
    Retrieving a list of configuration file component paths
    :param isamAppliance:
    :param check_mode:
    :param force:
    :return:
    """
    return isamAppliance.invoke_get("Retrieving a list of configuration file component paths",
                                    "{0}/{1}/{2}".format(mga_uri, path, filename),
                                    requires_modules=requires_modules, requires_version="10.0.0")


def export_file(isamAppliance, path, filename, file_path, check_mode=False, force=False):
    """
    Exporting a configuration file
    :param isamAppliance:
    :param check_mode:
    :param force:
    :return:
    """
    import os.path

    if force is True or (os.path.exists(file_path) is False):
        return isamAppliance.invoke_get_file("Exporting a configuration file",
                                             "{0}/{1}/{2}?export=true".format(mga_uri, path, filename),
                                             file_path,
                                             requires_modules=requires_modules, requires_version="10.0.0")

    return isamAppliance.create_return_object(warnings=["File {0} already exists".format(file_path)])


def update_file_contents(isamAppliance, path, filename, contents, check_mode=False, force=False):
    """
    Update the contents of a configuration file
    :param isamAppliance:
    :param check_mode:
    :param force:
    :return:
    """
    update, warnings = _check_contents(isamAppliance, path, filename, contents)

    if force is True or update is True:
        return isamAppliance.invoke_put("Update the contents of a configuration file",
                                        "{0}/{1}/{2}".format(mga_uri, path, filename),
                                        {
                                            'contents': contents,
                                            'type': 'file'
                                        },
                                        requires_modules=requires_modules, requires_version="10.0.0")
    return isamAppliance.create_return_object(warnings=warnings)


def import_file(isamAppliance, path, filename, file_path, check_mode=False, force=False):
    """
    Upload a new configuration file
    :param isamAppliance:
    :param check_mode:
    :param force:
    :return:
    """
    update, warnings = _check_import(isamAppliance, path, filename, file_path)

    if force is True or update is True:
        return isamAppliance.invoke_put_files("Upload a new configuration file",
                                              "{0}/{1}/{2}?uiCalled=true".format(mga_uri, path, filename),
                                              [
                                                  {
                                                      'file_formfield': 'file',
                                                      'filename': file_path,
                                                      'mimetype': 'application/octet-stream'
                                                  }
                                              ],
                                              {
                                                  "force": "yes",
                                                  "type": "file"
                                              },
                                              requires_modules=requires_modules, requires_version="10.0.0")
    return isamAppliance.create_return_object(warnings=warnings)


def _check_contents(isamAppliance, path, filename, contents):
    ret_obj = get_contents(isamAppliance, path, filename)
    if 'contents' in ret_obj['data']:
        if (ret_obj['data']['contents']) == contents:
            return False, ret_obj['warnings']
        else:
            return True, ret_obj['warnings']
    else:
        return False, ret_obj['warnings']


def _check_import(isamAppliance, path, filename, file_path):
    ret_obj = get_contents(isamAppliance, path, filename)

    import os
    if os.path.exists(file_path) is False:
        warnings = file_path + " does not exist."
        return False, [warnings]

    with open(file_path, 'r') as infile:
        input_contents = infile.read()

    if 'contents' in ret_obj['data']:
        if (ret_obj['data']['contents']) == input_contents:
            return False, ret_obj['warnings']
        else:
            return True, ret_obj['warnings']
    else:
        return False, ret_obj['warnings']


def _check(isamAppliance, key, value, sensitive):
    """
    Check and see if given key value matches existing values to be updated and also
    extract the id to use instead of the key
    """
    id, matches = None, None
    ret_obj = get_all(isamAppliance)

    for obj in ret_obj['data']:
        if obj['key'] == key:
            id = obj['id']
            if obj['value'] == value and obj['sensitive'] == sensitive:
                matches = True
            else:
                matches = False
            break

    return id, matches


def _check_values(isamAppliance, values):
    """
    Filter out values to be updated, and evaluate if an update needs to happen

    Note: Key values not found will be skipped!
    """
    matches, vals = True, []
    ret_obj = get_all(isamAppliance)

    for new_obj in values:
        for obj in ret_obj['data']:
            if obj['key'] == new_obj['key']:
                if obj['value'] != new_obj['value'] or obj['sensitive'] != new_obj['sensitive']:
                    matches = False
                    vals.append({'id': obj['id'], 'value': new_obj['value'], 'sensitive': new_obj['sensitive']})
                break

    logger.debug(vals)

    return matches, vals


def search(isamAppliance, key):
    """
    Get the ID for a given key value
    """
    ret_obj = get_all(isamAppliance)

    ret_obj_new = isamAppliance.create_return_object()

    for obj in ret_obj['data']:
        if obj['key'] == key:
            ret_obj_new['data'] = obj['id']
            break

    return ret_obj_new


def compare(isamAppliance1, isamAppliance2):
    """
    Compare AAC Advanced configuration between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    for obj in ret_obj1['data']:
        del obj['id']
    for obj in ret_obj2['data']:
        del obj['id']

    import ibmsecurity.utilities.tools
    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['id'])
