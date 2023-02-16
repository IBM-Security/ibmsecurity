import logging

from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

uri = "/wga/apiac/policy"
requires_modules = ["wga"]
requires_version = "9.0.7"


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the list of all existing API Access Control Policies
    """
    return isamAppliance.invoke_get("Retrieving the list of all existing API Access Control Policies",
                                    "{0}".format(uri),
                                    requires_modules=requires_modules, requires_version=requires_version)


def get(isamAppliance, policy_name, check_mode=False, force=False):
    """
    Retrieve a single API Access Control Policy

    """
    return isamAppliance.invoke_get("Retrieve a single API Access Control Policy",
                                    "{0}/{1}".format(uri, policy_name),
                                    requires_modules=requires_modules, requires_version=requires_version)


def add(isamAppliance, name, groups=None, attributes=None, check_mode=False, force=False):
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
                    "groups": groups,
                    "attributes": attributes
                }, requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object(warnings=warnings)


def update(isamAppliance, policy_name, groups=[], attributes=[], check_mode=False, force=False):
    """
    Update an existing API Access Control Policy
    """
    update_required, warnings, json_data = _check(isamAppliance, policy_name, groups, attributes)

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Update an existing API Access Control Policy",
                "{0}/{1}".format(uri, policy_name),
                json_data,
                requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object(warnings=warnings)


def set(isamAppliance, policy_name, groups=[], attributes=[], check_mode=False, force=False):
    exist, warnings = _check_exist(isamAppliance, policy_name)
    if exist:
        return update(isamAppliance=isamAppliance, policy_name=policy_name, groups=groups, attributes=attributes,
                      check_mode=check_mode, force=force)
    else:
        return add(isamAppliance=isamAppliance, name=policy_name, groups=groups, attributes=attributes)


def delete(isamAppliance, policy_name, check_mode=False, force=False):
    """
    Delete an access policy
    """
    if force is False:
        exist, warnings = _check_exist(isamAppliance, policy_name)

    if force is True or exist is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Delete an access policy",
                "{0}/{1}".format(uri, policy_name),
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


def _check_exist(isamAppliance, policy_name):
    ret_obj = get_all(isamAppliance)

    for obj in ret_obj['data']:
        if obj['name'] == policy_name:
            return True, ret_obj['warnings']

    return False, ret_obj['warnings']


def _check(isamAppliance, policy_name, groups, attributes):
    """
    The logic of the get_all() rest api is clunky at best, resulting always in failed checks when using groups or attributes
    - Extended attributes : output always includes quotes, while input does not work if you include quotes (api works, but the result does not)
    - Groups : additional groups ('iv-admin', 'webseal-servers') are added to the output.  The groups are put in ACL entries
    """
    json_data = {}
    ret_obj = get_all(isamAppliance)

    for obj in ret_obj['data']:
        if obj['name'] == policy_name:
            obj1 = {
                'name': obj['name'],
            }
            if 'attributes' in obj:
                # parse attributes to match the input (no quotes)
                newAttributes = []
                for l in obj['attributes']:
                    newAttributes.append(l.replace("'", ""))
                obj1["attributes"] = newAttributes
            if 'groups' in obj:
                # groups is not placed in the POP, but in a separate ACL
                #
                defaultGroups = ['iv-admin', 'webseal-servers']
                obj1["groups"] = list(filter(lambda g: g not in defaultGroups, obj["groups"]))
            obj2 = {
                'name': policy_name,
                'groups': groups,
                'attributes': attributes
            }
            sorted_obj1 = tools.json_sort(obj1)
            logger.debug("Sorted existing data: {0}".format(sorted_obj1))
            sorted_obj2 = tools.json_sort(obj2)
            logger.debug("Sorted input data   : {0}".format(sorted_obj2))
            if sorted_obj1 != sorted_obj2:
                logger.info("Changes detected, update needed.")
                return True, ret_obj['warnings'], obj2

    return False, ret_obj['warnings'], json_data


def compare(isamAppliance1, isamAppliance2):
    """
    Compare access policies between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    return tools.json_compare(ret_obj1, ret_obj2)
