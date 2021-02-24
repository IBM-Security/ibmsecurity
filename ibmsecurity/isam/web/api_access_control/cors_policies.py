import logging

from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

uri = "/wga/apiac/cors"
requires_modules = ["wga"]
requires_version = "10.0.0"


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the list of all existing CORS Policies
    """
    return isamAppliance.invoke_get("Retrieving the list of all existing CORS Policies",
                                    "{0}".format(uri),
                                    requires_modules=requires_modules, requires_version=requires_version)


def get(isamAppliance, cors_policy_name, check_mode=False, force=False):
    """
    Retrieve a single CORS Policy
    """
    return isamAppliance.invoke_get("Retrieve a single CORS Policy",
                                    "{0}/{1}".format(uri, cors_policy_name),
                                    requires_modules=requires_modules, requires_version=requires_version)


def add(isamAppliance, name, allowed_origins, allow_credentials=False, exposed_headers=[], handle_preflight=False,
        allowed_methods=[], allowed_headers=[], max_age=0, check_mode=False, force=False):
    """
    Create a new API Access Control Policy
    """
    exist, warnings = _check_exist(isamAppliance, name)

    if force is True or exist is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post(
                "Create a new API Access Control Policy", uri,
                {
                    "name": name,
                    "allowed_origins": allowed_origins,
                    "allow_credentials": allow_credentials,
                    "exposed_headers": exposed_headers,
                    "handle_preflight": handle_preflight,
                    "allowed_methods": allowed_methods,
                    "allowed_headers": allowed_headers,
                    "max_age": max_age
                }, requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object(warnings=warnings)


def update(isamAppliance, cors_policy_name, allowed_origins, allow_credentials=False, exposed_headers=[],
           handle_preflight=False, allowed_methods=[], allowed_headers=[], max_age=0, check_mode=False, force=False):
    """
    Update an existing API Access Control Policy
    """
    update_required, warnings, json_data = _check(isamAppliance=isamAppliance, cors_policy_name=cors_policy_name,
                                                  allowed_origins=allowed_origins, allow_credentials=allow_credentials,
                                                  exposed_headers=exposed_headers, handle_preflight=handle_preflight,
                                                  allowed_methods=allowed_methods, allowed_headers=allowed_headers,
                                                  max_age=max_age)

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Update an existing API Access Control Policy",
                "{0}/{1}".format(uri, cors_policy_name),
                json_data,
                requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object(warnings=warnings)


def set(isamAppliance, cors_policy_name, allowed_origins, allow_credentials=False, exposed_headers=[],
        handle_preflight=False, allowed_methods=[], allowed_headers=[], max_age=0, check_mode=False, force=False):
    exist, warnings = _check_exist(isamAppliance, cors_policy_name)
    if exist:
        return update(isamAppliance=isamAppliance, cors_policy_name=cors_policy_name, allowed_origins=allowed_origins,
                      allow_credentials=allow_credentials, exposed_headers=exposed_headers,
                      handle_preflight=handle_preflight, allowed_methods=allowed_methods,
                      allowed_headers=allowed_headers, max_age=max_age)
    else:
        return add(isamAppliance=isamAppliance, name=cors_policy_name, allowed_origins=allowed_origins,
                   allow_credentials=allow_credentials, exposed_headers=exposed_headers,
                   handle_preflight=handle_preflight, allowed_methods=allowed_methods, allowed_headers=allowed_headers,
                   max_age=max_age)


def delete(isamAppliance, cors_policy_name, check_mode=False, force=False):
    """
    Delete an access policy
    """
    if force is False:
        exist, warnings = _check_exist(isamAppliance, cors_policy_name)

    if force is True or exist is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Delete an access policy",
                "{0}/{1}".format(uri, cors_policy_name),
                requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object(warnings=warnings)


def delete_all(isamAppliance, check_mode=False, force=False):
    """
    Delete all existing API Access Control Policies
    """
    ret_obj = get_all(isamAppliance)

    if force is True or ret_obj['data'] != []:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Delete all existing API Access Control Policies",
                "{0}".format(uri),
                requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object()


def delete_selection(isamAppliance, policies, command="DELETE", check_mode=False, force=False):
    """
    Delete a selection of API Access Control Policies
    """
    found_any = False
    new_list_policies = []

    ret_obj = get_all(isamAppliance)
    warnings = ret_obj['warnings']

    for policy in policies:
        found = False
        for obj in ret_obj['data']:
            if obj['name'] == policy:
                found_any = True
                found = True
        if found is False:
            warnings.append("Did not find policy {0} to delete".format(policy))
        else:
            new_list_policies.append(policy)

    if force is True or found_any is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Delete a selection of API Access Control Policies",
                "{0}".format(uri),
                {
                    'command': command,
                    'policies': new_list_policies
                },
                requires_modules=requires_modules,
                requires_version=requires_version, warnings=warnings)

    return isamAppliance.create_return_object(warnings=warnings)


def _check_exist(isamAppliance, cors_policy_name):
    ret_obj = get_all(isamAppliance)

    for obj in ret_obj['data']:
        if obj['name'] == cors_policy_name:
            return True, ret_obj['warnings']

    return False, ret_obj['warnings']


def _check(isamAppliance, cors_policy_name, allowed_origins, allow_credentials, exposed_headers,
           handle_preflight, allowed_methods, allowed_headers, max_age):
    ret_obj = get_all(isamAppliance)
    exist = False
    json_data = {}

    for obj in ret_obj['data']:
        if obj['name'] == cors_policy_name:
            current_data = obj
            exist = True

    if exist is False:
        return False, ret_obj['warnings'], json_data

    json_data = {
        "name": cors_policy_name,
        "allowed_origins": allowed_origins,
        "allow_credentials": allow_credentials,
        "exposed_headers": exposed_headers,
        "handle_preflight": handle_preflight,
        "allowed_methods": allowed_methods,
        "allowed_headers": allowed_headers,
        "max_age": max_age
    }

    sorted_obj1 = tools.json_sort(json_data)
    logger.debug("Sorted input: {0}".format(sorted_obj1))
    sorted_obj2 = tools.json_sort(current_data)
    logger.debug("Sorted existing data: {0}".format(sorted_obj2))
    if sorted_obj1 != sorted_obj2:
        logger.info("Changes detected, update needed.")
        return True, ret_obj['warnings'], json_data
    else:
        return False, ret_obj['warnings'], json_data


def compare(isamAppliance1, isamAppliance2):
    """
    Compare cors policies between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    return tools.json_compare(ret_obj1, ret_obj2)
