import logging
import json
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

uri = "/mga/scim/configuration/schema_extensions"
requires_modules = ["mga"]
requires_version = "10.0.4"

"""
Manage SCIM Custom Schema Extensions

The array of attributes must be included in create and update requests as detailed below.

Attribute parameters include:
name
description
type - string, boolean, decimal, integer, dateTime, reference, complex (object), binary
mapping.sourceType - ldap, session, fixed
mapping.sourceAttribute
multiValued - True/False
required - True/False
mutability - readOnly, readWrite, immutable, writeOnly, adminWrite, userWrite
returned - always, never, default, request
canonicalValues
subAttributes

For example:

[
    {
        "name": "memberNumber",
        "description": "",
        "type": "integer",
        "mapping": {
            "sourceType": "ldap",
            "sourceAttribute": "membershipNumber"
        },
        "multiValued": False,
        "required": False,
        "mutability": "immutable",
        "returned": "default",
        "canonicalValues": [1, 2, 3]
    },
    {
        "name": "department",
        "description": "",
        "mutability": "readWrite",
        "type": "complex",
        "multiValued": False,
        "returned": "default",
        "required": False,
        "subAttributes": [
            {
                "mapping": {
                "sourceType": "ldap",
                "sourceAttribute": "department"
                },
                "name": "name",
                "description": "",
                "mutability": "readWrite",
                "type": "string",
                "multiValued": False,
                "returned": "default",
                "required": False
            },
            {
                "mapping": {
                "sourceType": "ldap",
                "sourceAttribute": "departmentCode"
                },
                "name": "code",
                "description": "",
                "mutability": "readWrite",
                "type": "string",
                "multiValued": False,
                "returned": "default",
                "required": False
            }
        ]
    }
]

"""

def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the complete list of SCIM Custom Schema Extensions
    """
    return isamAppliance.invoke_get("Retrieving the complete list of SCIM Custom Schema Extensions",
                                    uri)


def get(isamAppliance, urn, check_mode=False, force=False):
    """
    Retrieving the configuration of a SCIM Custom Schema Extension by urn/id
    """
    return isamAppliance.invoke_get("Retrieve the configuration of a SCIM Custom Schema Extension by urn/id",
                                       "{0}/{1}".format(uri, urn))


def set(isamAppliance, urn, name, description='', attributes=None,
        new_name=None, check_mode=False, force=False):
    """
    Creating or Modifying a SCIM Custom Schema Extension
    """
    if _check_exists(isamAppliance, urn=urn, name=name) is False:
        # Force the add - we already know connection does not exist
        return add(isamAppliance=isamAppliance, urn=urn, name=name, description=description,
                    attributes=attributes, check_mode=check_mode, force=True)
    else:
        # Update request
        return update(isamAppliance=isamAppliance, urn=urn, name=name, description=description,
                      attributes=attributes, new_name=new_name, check_mode=check_mode, force=force)


def add(isamAppliance, urn, name, description='', attributes=None, check_mode=False, force=False):
    """
    Creating a SCIM Custom Schema Extension
    """
    if force is True or _check_exists(isamAppliance, urn=urn, name=name) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post(
                "Creating a SCIM Custom Schema Extension",
                uri,
                _create_json(urn=urn, name=name, description=description, attributes=attributes),
                requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()


def update(isamAppliance, urn, name, description='', attributes=None, new_name=None, check_mode=False, force=False):
    """
    Modifying a SCIM Custom Schema Extension

    Use new_name to rename the extension.
    """
    ret_obj = get(isamAppliance, urn)
    warnings = ret_obj["warnings"]

    if ret_obj["data"] == {}:
        warnings.append("SCIM Custom Schema Extension {0} not found, skipping update.".format(urn))
        return isamAppliance.create_return_object(warnings=warnings)
    else:
        id = ret_obj["data"]["id"]

    needs_update = False

    json_data = _create_json(urn=urn, name=name, description=description, attributes=attributes)
    if new_name is not None:  # Rename condition
        json_data['name'] = new_name

    if force is not True:
        sorted_ret_obj = tools.json_sort(ret_obj['data'])
        sorted_json_data = tools.json_sort(json_data)
        logger.debug("Sorted Existing Data:{0}".format(sorted_ret_obj))
        logger.debug("Sorted Desired  Data:{0}".format(sorted_json_data))

        if sorted_ret_obj != sorted_json_data:
            needs_update = True

    if force is True or needs_update is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_put(
                "Modifying a SCIM Custom Schema Extension",
               "{0}/{1}".format(uri, urn), json_data,
                requires_modules=requires_modules, requires_version=requires_version, warnings=warnings)

    return isamAppliance.create_return_object(warnings=warnings)


def delete(isamAppliance, urn=None, name=None, check_mode=False, force=False):
    """
    Deleting a SCIM Custom Schema Extension
    """
    if force is True or _check_exists(isamAppliance, urn=urn, name=name) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            if urn == None and name != None:
                ret_obj = search(isamAppliance, name=name)
                urn = ret_obj['data']

            return isamAppliance.invoke_delete(
                "Deleting a SCIM Custom Schema Extension",
                "{0}/{1}".format(uri, urn),
                requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()


def search(isamAppliance, name):
    """
    Retrieve URN for named SCIM Custom Schema Extension
    """
    ret_obj = get_all(isamAppliance)

    ret_obj_new = isamAppliance.create_return_object()

    for obj in ret_obj['data']:
        if obj['name'] == name:
            ret_obj_new['data'] = obj['id']

    return ret_obj_new


def _create_json(urn, name, description, attributes):
    """
    Create a JSON to be used for the REST API call
    """

    json = {
        "id": urn,
        "name": name,
        "description": description,
        "attributes": attributes
    }

    return json


def _check_exists(isamAppliance, urn, name):
    """
    Check if the SCIM Custom Schema Extension already exists
    """
    ret_obj = get_all(isamAppliance)

    for obj in ret_obj['data']:
        if (name is not None and obj['name'] == name) or (urn is not None and obj['id'] == urn):
            return True

    return False
