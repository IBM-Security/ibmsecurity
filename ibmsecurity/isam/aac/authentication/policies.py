import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# "uri" variable already used so using a different name
module_uri = "/iam/access/v8/authentication/policies"
requires_modules = ["mga"]
requires_version = None


def get_all(isamAppliance, start=None, count=None, filter=None, sortBy=None, check_mode=False, force=False):
    """
    Retrieve a list of authentication policies
    """
    return isamAppliance.invoke_get("Retrieve a list of authentication policies", "{0}/{1}".format(module_uri,
                                                                                                   tools.create_query_string(
                                                                                                       start=start,
                                                                                                       count=count,
                                                                                                       filter=filter,
                                                                                                       sortBy=sortBy)),
                                    requires_modules=requires_modules, requires_version=requires_version)


def get(isamAppliance, name, check_mode=False, force=False):
    """
    Retrieve a specific authentication policy
    """
    ret_obj = search(isamAppliance, name)
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
    ret_obj = search(isamAppliance, name)
    if ret_obj['data'] == {}:
        return add(isamAppliance, name, policy, uri, description, dialect, enabled, check_mode, True)
    else:
        return update(isamAppliance, name, policy, uri, description, dialect, enabled, check_mode, force)


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
                if tools.version_compare(isamAppliance.facts["version"], "9.0.2.1") < 0:
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


def update(isamAppliance, name, policy, uri, description="",
           dialect="urn:ibm:security:authentication:policy:1.0:schema", enabled=None, check_mode=False, force=False):
    """
    Update a specified authentication policy
    """
    warnings = []
    needs_update = False
    json_data = {
        "name": name,
        "description": description,
        "policy": policy,
        "uri": uri,
        "dialect": dialect
    }
    if enabled is not None:
        if tools.version_compare(isamAppliance.facts["version"], "9.0.2.1") < 0:
            warnings.append(
                "Appliance is at version: {0}. Enabled parameter not supported unless atleast 9.0.2.1. Ignoring value.".format(
                    isamAppliance.facts["version"]))
        else:
            json_data["enabled"] = enabled
    if force is not True:
        try:
            ret_obj = get(isamAppliance, name)
            id = ret_obj['data']['id']
            del ret_obj['data']['id']
            del ret_obj['data']['datecreated']
            del ret_obj['data']['lastmodified']
            del ret_obj['data']['userlastmodified']
            del ret_obj['data']['predefined']
            import ibmsecurity.utilities.tools
            exist_data = ibmsecurity.utilities.tools.json_sort(ret_obj['data'])
            new_data = ibmsecurity.utilities.tools.json_sort(json_data)
            logger.debug("Existing Data: {0}".format(exist_data))
            logger.debug("Provided Data: {0}".format(new_data))
            if exist_data != new_data:
                needs_update = True
        except:
            pass

    if force is True or needs_update is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Update a specified authentication policy",
                "{0}/{1}".format(module_uri, id), json_data, requires_modules=requires_modules,
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


def search(isamAppliance, name, check_mode=False, force=False):
    """
    Retrieve the id for a given policy name
    """
    ret_obj = isamAppliance.create_return_object()
    ret_obj_all = get_all(isamAppliance)

    for obj in ret_obj_all['data']:
        if obj['name'] == name:
            ret_obj['data'] = obj['id']
            break

    return ret_obj


def activate(isamAppliance, name, enabled=True, check_mode=False, force=False):
    """
    Enable or disable a policy
    """
    warnings = []
    if tools.version_compare(isamAppliance.facts["version"], "9.0.2.1") < 0:
        warnings.append(
            "Appliance is at version: {0}. Enabled parameter not supported unless atleast 9.0.2.1. Ignoring value.".format(
                isamAppliance.facts["version"]))
    else:
        ret_obj = get(isamAppliance, name=name)
        if force or ret_obj['data']['enabled'] != enabled:
            if check_mode is True:
                return isamAppliance.create_return_object(changed=True, warnings=warnings)
            else:
                return update(isamAppliance, name=name, policy=ret_obj['data']['policy'], uri=ret_obj['data']['uri'],
                              description=ret_obj['data']['description'], dialect=ret_obj['data']['dialect'],
                              enabled=enabled)

    return isamAppliance.create_return_object(warnings=warnings)


def compare(isamAppliance1, isamAppliance2):
    """
    Compare Authentication Policies between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    for obj in ret_obj1['data']:
        ret_obj = _get(isamAppliance1, obj['id'])
        obj['policy'] = ret_obj['data']['policy']
        del obj['id']
        del obj['datecreated']
        del obj['lastmodified']
        del obj['userlastmodified']
    for obj in ret_obj2['data']:
        ret_obj = _get(isamAppliance2, obj['id'])
        obj['policy'] = ret_obj['data']['policy']
        del obj['id']
        del obj['datecreated']
        del obj['lastmodified']
        del obj['userlastmodified']

    return tools.json_compare(ret_obj1, ret_obj2,
                              deleted_keys=['id', 'datecreated', 'lastmodified', 'userlastmodified'])
