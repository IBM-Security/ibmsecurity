import logging
from typing import List
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# "uri" variable already used so using a different name
module_uri = "/iam/access/v8/authentication/policies"
module_uri_json = "/iam/access/v8/authentication/policies/json" # new in 10.0.6.0
requires_modules = ["mga"]
requires_version = None


def get_all(isamAppliance, start=None, count=None, filter=None, sortBy=None, formatting='xml', check_mode=False, force=False):
    """
    Retrieve a list of authentication policies

    formatting can be xml or json (actually, if it's not json, it's going to return xml) for version 10.0.6+
    """
    warnings = []

    if formatting == 'json':
        if tools.version_compare(isamAppliance.facts["version"], "10.0.6.0") < 0:
            warnings.append(
                f"Appliance is at version: {isamAppliance.facts['version']}. JSON format not supported unless at least 10.0.6.0. Setting to xml.")
            formatting = 'xml'
    if formatting == 'json':
        return isamAppliance.invoke_get("Retrieve a list of authentication policies (JSON)", "{0}/{1}".format(module_uri_json,
                                                                                                   tools.create_query_string(
                                                                                                       start=start,
                                                                                                       count=count,
                                                                                                       filter=filter,
                                                                                                       sortBy=sortBy)),
                                    requires_modules=requires_modules, requires_version=requires_version,warnings=warnings)
    else:
        return isamAppliance.invoke_get("Retrieve a list of authentication policies", "{0}/{1}".format(module_uri,
                                                                                                   tools.create_query_string(
                                                                                                       start=start,
                                                                                                       count=count,
                                                                                                       filter=filter,
                                                                                                       sortBy=sortBy)),
                                    requires_modules=requires_modules, requires_version=requires_version,warnings=warnings)


def get(isamAppliance, name, formatting='xml', check_mode=False, force=False):
    """
    Retrieve a specific authentication policy
    """
    ret_obj = search(isamAppliance, name, formatting=formatting)
    if ret_obj['data'] != {}:
        return _get(isamAppliance, ret_obj['data'], formatting=formatting)
    else:
        return isamAppliance.create_return_object()


def _get(isamAppliance, id, formatting='xml'):
    """
    Retrieve a specific authentication policy
    """
    warnings = []
    if formatting == 'json':
        if tools.version_compare(isamAppliance.facts["version"], "10.0.6.0") < 0:
            warnings.append(
                "Appliance is at version: {0}. JSON format not supported unless at least 10.0.6.0. Setting to xml.".format(
                    isamAppliance.facts["version"]))
            formatting = 'xml'
    if formatting == 'json':
        return isamAppliance.invoke_get("Retrieve a specific authentication policy (JSON)",
                                    "{0}/{1}".format(module_uri_json, id), requires_modules=requires_modules,
                                    warnings=warnings,
                                    requires_version=requires_version)
    else:
        return isamAppliance.invoke_get("Retrieve a specific authentication policy",
                                    "{0}/{1}".format(module_uri, id), requires_modules=requires_modules,
                                    warnings=warnings,
                                    requires_version=requires_version)

def set_file(isamAppliance, name, policy_file, uri, description="",
             dialect="urn:ibm:security:authentication:policy:1.0:schema", enabled=None, formatting='xml', check_mode=False, force=False):
    # Read policy from file and call set()
    with open(policy_file, 'r') as myfile:
        policy = myfile.read().replace('\n', '')
    return set(isamAppliance, name, policy, uri, description=description, dialect=dialect, enabled=enabled, formatting=formatting, check_mode=check_mode, force=force)


def set(isamAppliance, name, policy, uri, description="", dialect="urn:ibm:security:authentication:policy:1.0:schema",
        enabled=None, formatting='xml', check_mode=False, force=False):
    ret_obj = search(isamAppliance, name, formatting=formatting)
    if ret_obj['data'] == {}:
        return add(isamAppliance, name, policy, uri, description=description, dialect=dialect, enabled=enabled,
                   formatting=formatting, check_mode=check_mode, force=True)
    else:
        return update(isamAppliance, name, policy, uri, description=description, dialect=dialect, enabled=enabled,
                    formatting=formatting, check_mode=check_mode, force=force)


def add(isamAppliance, name, policy, uri, description="", dialect="urn:ibm:security:authentication:policy:1.0:schema",
        enabled=None, formatting='xml', check_mode=False, force=False):
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
                        "Appliance is at version: {0}. Enabled parameter not supported unless at least 9.0.2.1. Ignoring value.".format(
                            isamAppliance.facts["version"]))
                else:
                    json_data["enabled"] = enabled

            if formatting == 'json':
                 if tools.version_compare(isamAppliance.facts["version"], "10.0.6.0") < 0:
                     warnings.append(
                            "Appliance is at version: {0}. JSON format not supported unless at least 10.0.6.0. Setting to xml.".format(
                                isamAppliance.facts["version"]))
                     formatting = 'xml'


            if formatting == 'json':
                return isamAppliance.invoke_post(
                    "Duplicate and create an authentication policy (JSON)", module_uri_json, json_data,
                    requires_modules=requires_modules, requires_version=requires_version, warnings=warnings)
            else:
                return isamAppliance.invoke_post(
                    "Duplicate and create an authentication policy", module_uri, json_data,
                    requires_modules=requires_modules, requires_version=requires_version, warnings=warnings)

    return isamAppliance.create_return_object()


def delete(isamAppliance, id=None, name=None, check_mode=False, force=False):
    """
    Delete an authentication policy
    There's also a new json url for this, but I don't think that makes sense.
    """
    if id == None and name == None:
        from ibmsecurity.appliance.ibmappliance import IBMError
        raise IBMError("999", "Either id or name attribute must be provided")

    if force is True or _check(isamAppliance, id=id, name=name) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            if id == None:
                ret_obj = get(isamAppliance, name)
                id = ret_obj['data']['id']
            return isamAppliance.invoke_delete(
                "Delete an authentication policy",
                "{0}/{1}".format(module_uri, id), requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()


def update(isamAppliance, name, policy, uri, description="",
           dialect="urn:ibm:security:authentication:policy:1.0:schema", enabled=None, formatting='xml', check_mode=False, force=False):
    """
    Update a specified authentication policy
    """
    logger.debug(f"\n\nPERFORMING UPDATE {formatting}\n\n")
    warnings = []
    needs_update = False
    json_data = {
        "name": name,
        "description": description,
        "policy": policy,
        "uri": uri,
        "dialect": dialect
    }
    if formatting == 'json':
        if tools.version_compare(isamAppliance.facts["version"], "10.0.6.0") < 0:
            warnings.append(
                "Appliance is at version: {0}. JSON format not supported unless at least 10.0.6.0. Setting to xml.".format(
                    isamAppliance.facts["version"]))
            formatting = 'xml'
    if enabled is not None:
        if tools.version_compare(isamAppliance.facts["version"], "9.0.2.1") < 0:
            warnings.append(
                "Appliance is at version: {0}. Enabled parameter not supported unless at least 9.0.2.1. Ignoring value.".format(
                    isamAppliance.facts["version"]))
        else:
            json_data["enabled"] = enabled
    if force is not True:
        ret_obj = get(isamAppliance, name, formatting=formatting)
        id = ret_obj['data']['id']

        ret_obj['data'].pop('id', None)
        ret_obj['data'].pop('datecreated', None)
        ret_obj['data'].pop('dateCreated', None)
        ret_obj['data'].pop('lastmodified', None)
        ret_obj['data'].pop('lastModified', None)
        ret_obj['data'].pop('userlastmodified', None)
        ret_obj['data'].pop('userLastModified', None)
        ret_obj['data'].pop('predefined', None)

        exist_data = tools.json_sort(ret_obj['data'])
        new_data = tools.json_sort(json_data)
        logger.debug("\n\nExisting Data: {0}".format(exist_data))
        logger.debug("\n\nProvided Data: {0}".format(new_data))
        if exist_data != new_data:
            needs_update = True

    if force is True or needs_update is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            if formatting == 'json':
                return isamAppliance.invoke_put(
                    "Update a specified authentication policy (JSON)",
                    "{0}/{1}".format(module_uri_json, id), json_data, requires_modules=requires_modules,
                    requires_version=requires_version, warnings=warnings)
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


def search(isamAppliance, name, formatting='xml', check_mode=False, force=False):
    """
    Retrieve the id for a given policy name
    """
    ret_obj = isamAppliance.create_return_object()
    ret_obj_all = get_all(isamAppliance, formatting=formatting)

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
            "Appliance is at version: {0}. Enabled parameter not supported unless at least 9.0.2.1. Ignoring value.".format(
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
