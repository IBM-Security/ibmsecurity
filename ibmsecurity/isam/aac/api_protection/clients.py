import logging
import ibmsecurity.utilities.tools
from ibmsecurity.isam.aac.api_protection import definitions

logger = logging.getLogger(__name__)

# URI for this module
uri = "/iam/access/v8/clients"
requires_modules = ["mga"]
requires_version = None


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieve a list of API protection clients
    """
    return isamAppliance.invoke_get("Retrieve a list of API protection clients", uri, requires_modules=requires_modules,
                                    requires_version=requires_version)


def get(isamAppliance, name, check_mode=False, force=False):
    """
    Retrieve a specific API protection client
    """
    ret_obj = search(isamAppliance, name=name, check_mode=check_mode, force=force)
    client_id = ret_obj['data']
    warnings = ret_obj["warnings"]

    if client_id == {}:
        logger.info("Client {0} had no match, skipping retrieval.".format(name))
        warnings.append("Client Name {0} had no match.".format(name))
        return isamAppliance.create_return_object(warnings=warnings)
    else:
        return _get(isamAppliance, client_id)


def _get(isamAppliance, client_id):
    return isamAppliance.invoke_get("Retrieve a specific API protection client", "{0}/{1}".format(uri, client_id),
                                    requires_modules=requires_modules, requires_version=requires_version)


def search(isamAppliance, name, check_mode=False, force=False):
    """
    Search API Protection Client by name
    """
    ret_obj = get_all(isamAppliance)
    return_obj = isamAppliance.create_return_object()
    return_obj['warnings'] = ret_obj["warnings"]

    for obj in ret_obj['data']:
        if obj['name'] == name:
            logger.info("Found API Protection Client {0} id: {1}".format(name, obj['id']))
            return_obj['data'] = obj['id']
            return_obj['rc'] = 0

    return return_obj


def generate_client_id(isamAppliance, check_mode=False, force=False):
    """
    Generate a client ID
    """
    return isamAppliance.invoke_get("Generate a client ID", "{0}/clientid".format(uri),
                                    requires_modules=requires_modules,
                                    requires_version=requires_version)


def generate_client_secret(isamAppliance, check_mode=False, force=False):
    """
    Generate a client secret
    """
    return isamAppliance.invoke_get("Generate a client secret", "{0}/clientsecret".format(uri),
                                    requires_modules=requires_modules,
                                    requires_version=requires_version)


def add(isamAppliance, name, definitionName, companyName, redirectUri=None, companyUrl=None, contactPerson=None,
        contactType=None, email=None, phone=None, otherInfo=None, clientId=None, clientSecret=None, check_mode=False,
        force=False):
    """
    Create an API protection definition
    """
    ret_obj = definitions.search(isamAppliance, definitionName, check_mode=check_mode, force=force)
    if ret_obj['data'] == {}:
        warnings = ret_obj["warnings"]
        warnings.append(
            "API Protection Definition {0} is not found. Cannot process client request.".format(definitionName))
        return isamAppliance.create_return_object(warnings=warnings)
    else:
        definition = ret_obj['data']

    ret_obj = search(isamAppliance, name=name, check_mode=check_mode, force=force)
    warnings = ret_obj["warnings"]

    if force is True or ret_obj["data"] == {}:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            # Create a simple json with just the main client attributes
            client_json = {
                "name": name,
                "definition": definition,
                "companyName": companyName
            }
            # Add attributes that have been supplied... otherwise skip them.
            if redirectUri is not None:
                client_json["redirectUri"] = redirectUri
            if companyUrl is not None:
                client_json["companyUrl"] = companyUrl
            if contactPerson is not None:
                client_json["contactPerson"] = contactPerson
            if contactType is not None:
                client_json["contactType"] = contactType
            if email is not None:
                client_json["email"] = email
            if phone is not None:
                client_json["phone"] = phone
            if otherInfo is not None:
                client_json["otherInfo"] = otherInfo
            if clientId is not None:
                client_json["clientId"] = clientId
            if clientSecret is not None:
                client_json["clientSecret"] = clientSecret

            return isamAppliance.invoke_post(
                "Create an API protection definition", uri, client_json, requires_modules=requires_modules,
                requires_version=requires_version, warnings=warnings)

    return isamAppliance.create_return_object(warnings=warnings)


def delete(isamAppliance, name, check_mode=False, force=False):
    """
    Delete an API protection client registration
    """
    ret_obj = search(isamAppliance, name, check_mode=check_mode, force=force)
    client_id = ret_obj['data']
    warnings = ret_obj["warnings"]

    if client_id == {}:
        logger.info("Client {0} not found, skipping delete.".format(name))
    else:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_delete(
                "Delete an API protection client registration", "{0}/{1}".format(uri, client_id),
                requires_modules=requires_modules, requires_version=requires_version, warnings=warnings)

    return isamAppliance.create_return_object(warnings=warnings)


def update(isamAppliance, name, definitionName, companyName, redirectUri=None, companyUrl=None, contactPerson=None,
           contactType=None, email=None, phone=None, otherInfo=None, clientId=None, clientSecret=None, check_mode=False,
           force=False, new_name=None):
    """
    Update a specified mapping rule
    """
    ret_obj = definitions.search(isamAppliance, definitionName, check_mode=check_mode, force=force)
    if ret_obj['data'] == {}:
        warnings = ret_obj["warnings"]
        warnings.append(
            "API Protection Definition {0} is not found. Cannot process client request.".format(definitionName))
        return isamAppliance.create_return_object(warnings=warnings)
    else:
        definition = ret_obj['data']

    ret_obj = get(isamAppliance, name)
    warnings = ret_obj["warnings"]

    if ret_obj["data"] == {}:
        warnings.append("Client {0} not found, skipping update.".format(name))
        return isamAppliance.create_return_object(warnings=warnings)
    else:
        id = ret_obj["data"]["id"]

    needs_update = False
    # Create a simple json with just the main client attributes
    json_data = {
        "definition": definition,
        "companyName": companyName
    }
    if new_name is not None:
        json_data['name'] = new_name
    else:
        json_data['name'] = name

    if force is not True:
        del ret_obj['data']['id']
        # Add attributes that have been supplied... otherwise skip them.
        if redirectUri is not None:
            json_data["redirectUri"] = redirectUri
        elif 'redirectUri' in ret_obj['data']:
            del ret_obj['data']['redirectUri']
        if companyUrl is not None:
            json_data["companyUrl"] = companyUrl
        elif 'companyUrl' in ret_obj['data']:
            del ret_obj['data']['companyUrl']
        if contactPerson is not None:
            json_data["contactPerson"] = contactPerson
        elif 'contactPerson' in ret_obj['data']:
            del ret_obj['data']['contactPerson']
        if contactType is not None:
            json_data["contactType"] = contactType
        elif 'contactType' in ret_obj['data']:
            del ret_obj['data']['contactType']
        if email is not None:
            json_data["email"] = email
        elif 'email' in ret_obj['data']:
            del ret_obj['data']['email']
        if phone is not None:
            json_data["phone"] = phone
        elif 'phone' in ret_obj['data']:
            del ret_obj['data']['phone']
        if otherInfo is not None:
            json_data["otherInfo"] = otherInfo
        elif 'otherInfo' in ret_obj['data']:
            del ret_obj['data']['otherInfo']
        if clientId is not None:
            json_data["clientId"] = clientId
        elif 'clientId' in ret_obj['data']:
            del ret_obj['data']['clientId']
        if clientSecret is not None:
            json_data["clientSecret"] = clientSecret
        elif 'clientSecret' in ret_obj['data']:
            del ret_obj['data']['clientSecret']
        if ibmsecurity.utilities.tools.json_sort(ret_obj['data']) != ibmsecurity.utilities.tools.json_sort(
                json_data):
            needs_update = True

    if force is True or needs_update is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_put(
                "Update a specified mapping rule", "{0}/{1}".format(uri, id), json_data,
                requires_modules=requires_modules, requires_version=requires_version, warnings=warnings)

    return isamAppliance.create_return_object(warnings=warnings)


def set(isamAppliance, name, definitionName, companyName, redirectUri=None, companyUrl=None, contactPerson=None,
        contactType=None, email=None, phone=None, otherInfo=None, clientId=None, clientSecret=None, new_name=None,
        check_mode=False,
        force=False):
    """
    Creating or Modifying an API Protection Definition
    """
    if (search(isamAppliance, name=name))['data'] == {}:
        # Force the add - we already know policy does not exist
        logger.info("Definition {0} had no match, requesting to add new one.".format(name))
        return add(isamAppliance, name, definitionName, companyName, redirectUri=redirectUri, companyUrl=companyUrl,
                   contactPerson=contactPerson,
                   contactType=contactType, email=email, phone=phone, otherInfo=otherInfo, clientId=clientId,
                   clientSecret=clientSecret, check_mode=check_mode, force=True)
    else:
        # Update request
        logger.info("Definition {0} exists, requesting to update.".format(name))
        return update(isamAppliance, name, definitionName, companyName, redirectUri=redirectUri, companyUrl=companyUrl,
                      contactPerson=contactPerson, contactType=contactType, email=email, phone=phone,
                      otherInfo=otherInfo, clientId=clientId, clientSecret=clientSecret, new_name=new_name,
                      check_mode=check_mode, force=force)


def compare(isamAppliance1, isamAppliance2):
    """
    Compare API Protection Definitions between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    for obj in ret_obj1['data']:
        del obj['id']
        del obj['definition']
    for obj in ret_obj2['data']:
        del obj['id']
        del obj['definition']

    import ibmsecurity.utilities.tools
    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['id', 'definition'])
