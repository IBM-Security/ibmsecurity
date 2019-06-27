import logging
from ibmsecurity.utilities import tools
from ibmsecurity.appliance.ibmappliance import IBMError

logger = logging.getLogger(__name__)

artifact_type = "pip"
# URI for this module
uri = "/iam/access/v8/pips"
requires_modules = ["mga"]
requires_version = "9.0.5.0"


def get_all(isamAppliance, filter=None, sortBy=None, check_mode=False, force=False):
    """
    Retrieve a list of Policy Information Points (PIPs)
    """
    return isamAppliance.invoke_get("Retrieve a list of policy information points (pips)",
                                    "{0}/{1}".format(uri, tools.create_query_string(filter=filter, sortBy=sortBy)),
                                    requires_modules=requires_modules, requires_version=requires_version)


def get(isamAppliance, name=None, check_mode=False, force=False):
    """
    Retrieve a specific Policy Information Point by name
    """
    ret_obj = _get_id(isamAppliance, name=name)
    id = ret_obj['data']

    if id == {}:
        return isamAppliance.create_return_object()
    else:
        try:
            response = isamAppliance.invoke_get("Retrieve a specific PIP",
                                                "{0}/{1}".format(uri, id),
                                                requires_modules=requires_modules,
                                                requires_version=requires_version
                                                )
        except IBMError as e:
            if "404" in e.args[0]:
                response = isamAppliance.create_return_object(rc=404, data=e.args[1])
            else:
                raise

    return response


def get_pip(isamAppliance, pip_id, check_mode=False, force=False):
    """
    Retrieve a specific Policy Information Point by ID
    """
    if _check_exists(isamAppliance, id=pip_id) is True:
        return isamAppliance.invoke_get("Retrieve a specific PIP ID",
                                        "{0}/{1}".format(uri, pip_id), requires_modules=requires_modules,
                                        requires_version=requires_version)
    else:
        return isamAppliance.create_return_object()


def set(isamAppliance, name, searchBaseDN, searchFilter, searchTimeout, serverConnection,
        attributeName, attributeSelector, description='', type="LDAP",
        cacheSize=10000, cacheLifetime=600, check_mode=False, force=False):
    """
    Creating or Modifying an LDAP PIP
    """
    if _check_exists(isamAppliance, name=name) is False:
        # Force the add - we already know connection does not exist
        return add(isamAppliance, name, searchBaseDN, searchFilter, searchTimeout, serverConnection,
                   attributeName, attributeSelector, description='', type="LDAP",
                   cacheSize=10000, cacheLifetime=600, check_mode=False, force=True)
    else:
        # Update request
        return update(isamAppliance, name, searchBaseDN, searchFilter, searchTimeout, serverConnection,
                      attributeName, attributeSelector, description='', type="LDAP",
                      cacheSize=10000, cacheLifetime=600, check_mode=False, force=False)


def add(isamAppliance, name, searchBaseDN, searchFilter, searchTimeout, serverConnection,
        attributeName, attributeSelector, description='', type="LDAP",
        cacheSize=10000, cacheLifetime=600, check_mode=False, force=False):
    """
    Creating an LDAP PIP
    """
    if force is True or _check_exists(isamAppliance, name=name) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            try:
                response = isamAppliance.invoke_post(
                    "Creating an LDAP PIP",
                    "{0}".format(uri),
                    _create_json(name=name, description=description, type=type,
                                 searchBaseDN=searchBaseDN, searchFilter=searchFilter,
                                 searchTimeout=searchTimeout, serverConnection=serverConnection,
                                 cacheSize=cacheSize, cacheLifetime=cacheLifetime,
                                 attributeName=attributeName, attributeSelector=attributeSelector),
                    requires_modules=requires_modules, requires_version=requires_version
                )

            except IBMError as e:
                logger.exception(e)
                if "400" in e.args[0]:
                    response = isamAppliance.create_return_object(rc=400, data=e.args[1])
                elif "409" in e.args[0]:
                    response = isamAppliance.create_return_object(rc=409, data=e.args[1])
                else:
                    raise

    return response


def delete(isamAppliance, name=None, check_mode=False, force=False):
    """
    Deleting an LDAP PIP
    """
    if force is True or _check_exists(isamAppliance, name=name) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            ret_obj = _get_id(isamAppliance, name=name)
            id = ret_obj['data']

            try:
                response = isamAppliance.invoke_delete(
                    "Deleting an LDAP PIP",
                    "{0}/{1}".format(uri, id),
                    requires_modules=requires_modules, requires_version=requires_version
                )
            except IBMError as e:
                if "404" in e.args[0]:
                    response = isamAppliance.create_return_object(rc=404, data=e.args[1])
                else:
                    raise

    return response


def update(isamAppliance, name, searchBaseDN, searchFilter, searchTimeout, serverConnection,
           attributeName, attributeSelector, description='', type="LDAP", cacheSize=10000,
           cacheLifetime=600, new_name=None, check_mode=False, force=False):
    """
    Modifying an LDAP PIP
    Use new_name to rename the connection
    """
    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:
        ret_obj = _get_id(isamAppliance, name=name)
        id = ret_obj['data']
        json_data = _create_json(name=name, description=description, type=type,
                                 searchBaseDN=searchBaseDN, searchFilter=searchFilter,
                                 searchTimeout=searchTimeout, serverConnection=serverConnection,
                                 cacheSize=cacheSize, cacheLifetime=cacheLifetime,
                                 attributeName=attributeName, attributeSelector=attributeSelector)
        if new_name is not None:  # Rename condition
            json_data['name'] = new_name

        try:
            response = isamAppliance.invoke_put(
                "Modifying an LDAP PIP",
                "{0}/{1}".format(uri, id), json_data, requires_modules=requires_modules,
                requires_version=requires_version)
        except IBMError as e:
            if "400" in e.args[0]:
                response = isamAppliance.create_return_object(rc=400, data=e.args[1])
            else:
                raise

        return response


def _create_json(name, description, type, searchBaseDN, searchFilter,
                 searchTimeout, serverConnection, cacheSize, cacheLifetime,
                 attributeName, attributeSelector):
    """
    Create a JSON to be used for the REST API call
    """
    json = {
        "name": name,
        "description": description,
        "type": "LDAP",
        "properties": [
            {"key": "searchBaseDN", "value": searchBaseDN, "datatype": "String",
             "sensitive": False, "readOnly": False},
            {"key": "searchFilter", "value": searchFilter,
             "datatype": "String", "sensitive": False, "readOnly": False},
            {"key": "searchTimeout", "value": searchTimeout, "datatype": "Integer",
             "sensitive": False, "readOnly": False},
            {"key": "dataSource", "value": serverConnection,
             "datatype": "String", "sensitive": False, "readOnly": False},
            {"key": "cacheSize", "value": cacheSize, "datatype": "Integer",
             "sensitive": False, "readOnly": False},
            {"key": "cacheLifetime", "value": cacheLifetime, "datatype": "Integer",
             "sensitive": False, "readOnly": False}
        ],
        "attributes": [
            {"name": attributeName, "selector": attributeSelector}
        ]
    }

    return json


def _get_id(isamAppliance, name):
    """
    Retrieve ID for named LDAP PIP
    """
    ret_obj = get_all(isamAppliance)

    ret_obj_new = isamAppliance.create_return_object()

    for obj in ret_obj['data']:
        if obj['name'] == name:
            ret_obj_new['data'] = obj['id']

    return ret_obj_new


def _check_exists(isamAppliance, name=None, id=None):
    """
    Check if LDAP PIP already exists
    """
    ret_obj = get_all(isamAppliance)

    for obj in ret_obj['data']:
        if (name is not None and obj['name'] == name) or (id is not None and obj['id'] == id):
            return True

    return False


def compare(isamAppliance1, isamAppliance2):
    """
    Compare LDAP PIPs between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    for obj in ret_obj1['data']:
        del obj['id']
    for obj in ret_obj2['data']:
        del obj['id']

    return tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['id'])
