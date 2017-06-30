import logging

logger = logging.getLogger(__name__)

# "uri" variable already used so using a different name
module_uri = "/iam/access/v8/authentication/policies"
requires_modules = ["mga"]
requires_version = None


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieve a list of authentication policies
    """
    return isamAppliance.invoke_get("Retrieve a list of authentication policies", module_uri,
                                    requires_modules=requires_modules, requires_version=requires_version)


def get(isamAppliance, name, check_mode=False, force=False):
    """
    Retrieve a specific authentication policy
    """
    ret_obj = search(isamAppliance, filter="name equals {}".format(name))
    if ret_obj['data'] != {}:
        return _get(isamAppliance, ret_obj['data'])
    else:
        return isamAppliance.create_return_object()


def _get(isamAppliance, id):
    """
    Retrieve a specific authentication policy
    """
    return isamAppliance.invoke_get("Retrieve a specific authentication policy",
                                    "{0}/{1}".format(module_uri, id), requires_modules=requires_modules,
                                    requires_version=requires_version)


def set_file(isamAppliance, name, policy_file, uri, description="",
             dialect="urn:ibm:security:authentication:policy:1.0:schema", enabled=None, check_mode=False, force=False):
    # Read policy from file and call set()
    with open(policy_file, 'r') as myfile:
        policy = myfile.read().replace('\n', '')
    return set(isamAppliance, name, policy, uri, description, dialect, enabled, check_mode, force)


def set(isamAppliance, name, policy, uri, description="", dialect="urn:ibm:security:authentication:policy:1.0:schema",
        enabled=None, check_mode=False, force=False):
    ret_obj = search(isamAppliance, filter="name equals {}".format(name))
    if ret_obj['data'] == {}:
        return add(isamAppliance, name, policy, uri, description, dialect, enabled, check_mode, True)
    else:
        try:
            id = ret_obj['data']['id']
        except KeyError:
            error = "Unable to find ID for policy named '{}'".format(name)
            warnings.append(error)
            logging.error(error)
            return isamAppliance.create_return_object(warnings=warnings)
        return update(isamAppliance, id, name=name, policy=policy, ur=uri, description=description, dialect=dialect, enabled=enabled, check_mode=check_mode, force=force)


def add(isamAppliance, name, policy, uri, description="", dialect="urn:ibm:security:authentication:policy:1.0:schema",
        enabled=None, check_mode=False, force=False):
    """
    Duplicate and create an authentication policy
    """
    if force is True or _check(isamAppliance, name=name) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            warnings = []
            json_data = {
                "name": name,
                "description": description,
                "policy": policy,
                "uri": uri,
                "dialect": dialect
            }
            if enabled is not None:
                if isamAppliance.facts["version"] < "9.0.2.1":
                    warnings.append(
                        "Appliance is at version: {0}. Enabled parameter not supported unless atleast 9.0.2.1. Ignoring value.".format(
                            isamAppliance.facts["version"]))
                else:
                    json_data["enabled"] = enabled
            return isamAppliance.invoke_post(
                "Duplicate and create an authentication policy", module_uri, json_data,
                requires_modules=requires_modules, requires_version=requires_version, warnings=warnings)

    return isamAppliance.create_return_object()


def delete(isamAppliance, id, check_mode=False, force=False):
    """
    Delete an authentication policy
    """
    if force is True or _check(isamAppliance, id=id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Delete an authentication policy",
                "{0}/{1}".format(module_uri, id), requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()

def update(isamAppliance, id, name=None, policy=None, uri=None, description=None,
           dialect=None, user_last_modified=None, last_modified=None,
           date_created=None, predefined=None, enabled=None, check_mode=False, force=False):
    """
    Update a specific policy by its ID. If options are provided, they will be modified.
    If options are not provided, they won't be modified.
    """
    warnings = []
    needs_update = False

    def add_if_not_empty(data, key, value):
        if value is not None:
            data[key] = value

    data = {}
    add_if_not_empty(data, "name", name)
    add_if_not_empty(data, "policy", policy)
    add_if_not_empty(data, "uri", uri)
    add_if_not_empty(data, "description", description)
    add_if_not_empty(data, "dialect", dialect)
    add_if_not_empty(data, "id", id)
    add_if_not_empty(data, "userlastmodified", user_last_modified)
    add_if_not_empty(data, "lastmodified", last_modified)
    add_if_not_empty(data, "datecreated", date_created)
    add_if_not_empty(data, "predefined", predefined)

    if force is True or needs_update is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Update a specified authentication policy",
                "{0}/{1}".format(module_uri, id), data, requires_modules=requires_modules,
                requires_version=requires_version, warnings=warnings)

    return isamAppliance.create_return_object()


def _check(isamAppliance, id=None, name=None):
    """
    Check if API Protection Definition already exists
    """
    ret_obj = get_all(isamAppliance)

    for obj in ret_obj['data']:
        if (id is not None and obj['id'] == id) or (name is not None and obj['name'] == name):
            return True

    return False


# Provides a list of policies matching the specified parameters.
# For information on the 'filter', consult the RAPI doc for "Retrieve a list of policies".
def search(isamAppliance, sort_by=None, count=None, start=None, filter=None):
    parameters = {}
    parameters["sortBy"] = sort_by
    parameters["count"] = count
    parameters["start"] = start
    parameters["filter"] = filter

    return isamAppliance.invoke_get("Search for authentication policies", module_uri, parameters)


def activate(isamAppliance, name, enabled=True, check_mode=False, force=False):
    """
    Enable or disable a policy
    """
    warnings = []
    if isamAppliance.facts["version"] < "9.0.2.1":
        warnings.append(
            "Appliance is at version: {0}. Enabled parameter not supported unless atleast 9.0.2.1. Ignoring value.".format(
                isamAppliance.facts["version"]))
    else:
        ret_obj = get(isamAppliance, name=name)
        if force or ret_obj['data']['enabled'] != enabled:
            if check_mode is True:
                return isamAppliance.create_return_object(changed=True, warnings=warnings)
            else:
                return update(isamAppliance, ret_obj['data']['id'],
                              enabled=enabled)

    return isamAppliance.create_return_object(warnings=warnings)


def compare(isamAppliance1, isamAppliance2):
    """
    Compare Authentication Policies between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    for obj in ret_obj1['data']:
        del obj['id']
        del obj['datecreated']
        del obj['lastmodified']
        del obj['userlastmodified']
        ret_obj = _get(isamAppliance1, ret_obj1['data']['id'])
        obj['policy'] = ret_obj['data']['policy']
    for obj in ret_obj2['data']:
        del obj['id']
        del obj['datecreated']
        del obj['lastmodified']
        del obj['userlastmodified']
        ret_obj = _get(isamAppliance2, ret_obj1['data']['id'])
        obj['policy'] = ret_obj['data']['policy']

    import ibmsecurity.utilities.tools
    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2,
                                                    deleted_keys=['id', 'datecreated', 'lastmodified',
                                                                  'userlastmodified'])
