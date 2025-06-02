import logging
from ibmsecurity.utilities import tools
from ibmsecurity.isam.aac.api_protection import definitions

logger = logging.getLogger(__name__)

# URI for this module
uri = "/iam/access/v8/clients"
requires_modules = ["mga", "federation"]
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
        logger.info(f"Client {name} had no match, skipping retrieval.")
        warnings.append(f"Client Name {name} had no match.")
        return isamAppliance.create_return_object(warnings=warnings)
    else:
        return _get(isamAppliance, client_id)


def _get(isamAppliance, client_id):
    return isamAppliance.invoke_get("Retrieve a specific API protection client", f"{uri}/{client_id}",
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
            logger.info(f"Found API Protection Client {name} id: {obj['id']}")
            return_obj['data'] = obj['id']
            return_obj['rc'] = 0

    return return_obj

def search_id(isamAppliance, clientId, check_mode=False, force=False):
    """
    Search API Protection Client by name
    """
    ret_obj = get_all(isamAppliance)
    return_obj = isamAppliance.create_return_object()
    return_obj['warnings'] = ret_obj["warnings"]

    for obj in ret_obj['data']:
        if obj['clientId'] == clientId:
            logger.info(f"Found API Protection Client {clientId} id: {obj['id']}")
            return_obj['data'] = obj['id']
            return_obj['rc'] = 0

    return return_obj

def _get_id(isamAppliance, clientId, check_mode=False, force=False):
    """
    Search API Protection Client by name
    """
    ret_obj = get_all(isamAppliance)
    return_obj = isamAppliance.create_return_object()
    return_obj['warnings'] = ret_obj["warnings"]

    for obj in ret_obj['data']:
        if obj['clientId'] == clientId:
            logger.info(f"Found API Protection Client {clientId} id: {obj['id']}")
            return_obj['data'] = obj
            return_obj['rc'] = 0

    return return_obj


def generate_client_id(isamAppliance, check_mode=False, force=False):
    """
    Generate a client ID
    """
    return isamAppliance.invoke_get("Generate a client ID", f"{uri}/clientid",
                                    requires_modules=requires_modules,
                                    requires_version=requires_version)


def generate_client_secret(isamAppliance, check_mode=False, force=False):
    """
    Generate a client secret
    """
    return isamAppliance.invoke_get("Generate a client secret", f"{uri}/clientsecret",
                                    requires_modules=requires_modules,
                                    requires_version=requires_version)


def add(isamAppliance, name, definitionName, companyName, redirectUri=None, companyUrl=None, contactPerson=None,
        contactType=None, email=None, phone=None, otherInfo=None, clientId=None, clientSecret=None,
        requirePkce=None, encryptionDb=None, encryptionCert=None, jwksUri=None, extProperties=None, introspectWithSecret=None,
        check_mode=False, force=False):
    """
    Create an API protection definition
    """
    ret_obj = definitions.search(isamAppliance, definitionName, check_mode=check_mode, force=force)
    if ret_obj['data'] == {}:
        warnings = ret_obj["warnings"]
        warnings.append(
            f"API Protection Definition {definitionName} is not found. Cannot process client request.")
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
            if requirePkce is not None:
                if tools.version_compare(isamAppliance.facts["version"], "9.0.4.0") < 0:
                    warnings.append(
                        f"Appliance at version: {isamAppliance.facts['version']}, requirePkce: {requirePkce} is not supported. Needs 9.0.4.0 or higher. Ignoring requirePkce for this call.")
                else:
                    client_json["requirePkce"] = requirePkce
            if encryptionDb is not None:
                if tools.version_compare(isamAppliance.facts["version"], "9.0.4.0") < 0:
                    warnings.append(
                        f"Appliance at version: {isamAppliance.facts['version']}, encryptionDb: {encryptionDb} is not supported. Needs 9.0.4.0 or higher. Ignoring encryptionDb for this call.")
                else:
                    client_json["encryptionDb"] = encryptionDb
            if encryptionCert is not None:
                if tools.version_compare(isamAppliance.facts["version"], "9.0.4.0") < 0:
                    warnings.append(
                        f"Appliance at version: {isamAppliance.facts['version']}, encryptionCert: {encryptionCert} is not supported. Needs 9.0.4.0 or higher. Ignoring encryptionCert for this call.")
                else:
                    client_json["encryptionCert"] = encryptionCert
            if jwksUri is not None:
                if tools.version_compare(isamAppliance.facts["version"], "9.0.4.0") < 0:
                    warnings.append(
                        f"Appliance at version: {isamAppliance.facts['version']}, jwksUri: {jwksUri} is not supported. Needs 9.0.4.0 or higher. Ignoring jwksUri for this call.")
                else:
                    client_json["jwksUri"] = jwksUri
            if extProperties is not None:
                if tools.version_compare(isamAppliance.facts["version"], "9.0.5.0") < 0:
                    warnings.append(
                        f"Appliance at version: {isamAppliance.facts['version']}, extProperties: {extProperties} is not supported. Needs 9.0.5.0 or higher. Ignoring extProperties for this call.")
                else:
                    client_json["extProperties"] = extProperties
            if introspectWithSecret is not None:
                if tools.version_compare(isamAppliance.facts["version"], "9.0.7.0") < 0:
                    warnings.append(
                        f"Appliance at version: {isamAppliance.facts['version']}, introspectWithSecret: {introspectWithSecret} is not supported. Needs 9.0.7.0 or higher. Ignoring introspectWithSecret for this call.")
                else:
                    client_json["introspectWithSecret"] = introspectWithSecret

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
        logger.info(f"Client {name} not found, skipping delete.")
    else:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_delete(
                "Delete an API protection client registration", f"{uri}/{client_id}",
                requires_modules=requires_modules, requires_version=requires_version, warnings=warnings)

    return isamAppliance.create_return_object(warnings=warnings)


def update(isamAppliance, name, definitionName, companyName, redirectUri=None, companyUrl=None, contactPerson=None,
           contactType=None, email=None, phone=None, otherInfo=None, clientId=None, clientSecret=None,
           requirePkce=None, encryptionDb=None, encryptionCert=None, jwksUri=None, extProperties=None, introspectWithSecret=None,
           check_mode=False, force=False, new_name=None):
    """
    Update a specified mapping rule
    """
    ret_obj = definitions.search(isamAppliance, definitionName, check_mode=check_mode, force=force)
    if ret_obj['data'] == {}:
        warnings = ret_obj["warnings"]
        warnings.append(
            f"API Protection Definition {definitionName} is not found. Cannot process client request.")
        return isamAppliance.create_return_object(warnings=warnings)
    else:
        definition = ret_obj['data']

    ret_obj = get(isamAppliance, name)
    warnings = ret_obj["warnings"]

    if ret_obj["data"] == {}:
        warnings.append(f"Client {name} not found, skipping update.")
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

    del ret_obj['data']['id']
    # Add attributes that have been supplied... otherwise skip them.
    if redirectUri is not None:
        json_data["redirectUri"] = redirectUri
    elif 'redirectUri' in ret_obj['data']:
        if ret_obj['data']['redirectUri'] is not None:
            json_data['redirectUri'] = ret_obj['data']['redirectUri']
        else:
            del ret_obj['data']['redirectUri']
    if companyUrl is not None:
        json_data['companyUrl'] = companyUrl
    elif 'companyUrl' in ret_obj['data']:
        if ret_obj['data']['companyUrl'] is not None:
            json_data['companyUrl'] = ret_obj['data']['companyUrl']
        else:
            del ret_obj['data']['companyUrl']
    if contactPerson is not None:
        json_data['contactPerson'] = contactPerson
    elif 'contactPerson' in ret_obj['data']:
        if ret_obj['data']['contactPerson'] is not None:
            json_data['contactPerson'] = ret_obj['data']['contactPerson']
        else:
            del ret_obj['data']['contactPerson']
    if contactType is not None:
        json_data['contactType'] = contactType
    elif 'contactType' in ret_obj['data']:
        if ret_obj['data']['contactType'] is not None:
            json_data['contactType'] = ret_obj['data']['contactType']
        else:
            del ret_obj['data']['contactType']
    if email is not None:
        json_data['email'] = email
    elif 'email' in ret_obj['data']:
        if ret_obj['data']['email'] is not None:
            json_data['email'] = ret_obj['data']['email']
        else:
            del ret_obj['data']['email']
    if phone is not None:
        json_data['phone'] = phone
    elif 'phone' in ret_obj['data']:
        if ret_obj['data']['phone'] is not None:
            json_data['phone'] = ret_obj['data']['phone']
        else:
            del ret_obj['data']['phone']
    if otherInfo is not None:
        json_data['otherInfo'] = otherInfo
    elif 'otherInfo' in ret_obj['data']:
        if ret_obj['data']['otherInfo'] is not None:
            json_data['otherInfo'] = ret_obj['data']['otherInfo']
        else:
            del ret_obj['data']['otherInfo']
    if clientId is not None:
        json_data['clientId'] = clientId
    elif 'clientId' in ret_obj['data']:
        if ret_obj['data']['clientId'] is not None:
            json_data['clientId'] = ret_obj['data']['clientId']
        else:
            del ret_obj['data']['clientId']
    if clientSecret is not None:
        json_data['clientSecret'] = clientSecret
    elif 'clientSecret' in ret_obj['data']:
        if ret_obj['data']['clientSecret'] is not None:
            json_data['clientSecret'] = ret_obj['data']['clientSecret']
        else:
            del ret_obj['data']['clientSecret']
    if requirePkce is not None:
        if tools.version_compare(isamAppliance.facts["version"], "9.0.4.0") < 0:
            warnings.append(
                f"Appliance at version: {isamAppliance.facts['version']}, requirePkce: {requirePkce} is not supported. Needs 9.0.4.0 or higher. Ignoring requirePkce for this call.")
        else:
            json_data['requirePkce'] = requirePkce
    elif 'requirePkce' in ret_obj['data']:
        if ret_obj['data']['requirePkce'] is not None:
            json_data['requirePkce'] = ret_obj['data']['requirePkce']
        else:
            del ret_obj['data']['requirePkce']
    if encryptionDb is not None:
        if tools.version_compare(isamAppliance.facts["version"], "9.0.4.0") < 0:
            warnings.append(
                f"Appliance at version: {isamAppliance.facts['version']}, encryptionDb: {encryptionDb} is not supported. Needs 9.0.4.0 or higher. Ignoring encryptionDb for this call.")
        else:
            json_data['encryptionDb'] = encryptionDb
    elif 'encryptionDb' in ret_obj['data']:
        if ret_obj['data']['encryptionDb'] is not None:
            json_data['encryptionDb'] = ret_obj['data']['encryptionDb']
        else:
            del ret_obj['data']['encryptionDb']
    if encryptionCert is not None:
        if tools.version_compare(isamAppliance.facts["version"], "9.0.4.0") < 0:
            warnings.append(
                f"Appliance at version: {isamAppliance.facts['version']}, encryptionCert: {encryptionCert} is not supported. Needs 9.0.4.0 or higher. Ignoring encryptionCert for this call.")
        else:
            json_data['encryptionCert'] = encryptionCert
    elif 'encryptionCert' in ret_obj['data']:
        if ret_obj['data']['encryptionCert'] is not None:
            json_data['encryptionCert'] = ret_obj['data']['encryptionCert']
        else:
            del ret_obj['data']['encryptionCert']
    if jwksUri is not None:
        if tools.version_compare(isamAppliance.facts["version"], "9.0.4.0") < 0:
            warnings.append(
                f"Appliance at version: {isamAppliance.facts['version']}, jwksUri: {jwksUri} is not supported. Needs 9.0.4.0 or higher. Ignoring jwksUri for this call.")
        else:
            json_data['jwksUri'] = jwksUri
    elif 'jwksUri' in ret_obj['data']:
        if ret_obj['data']['jwksUri'] is not None:
            json_data['jwksUri'] = ret_obj['data']['jwksUri']
        else:
            del ret_obj['data']['jwksUri']
    if extProperties is not None:
        if tools.version_compare(isamAppliance.facts["version"], "9.0.5.0") < 0:
            warnings.append(
                f"Appliance at version: {isamAppliance.facts['version']}, extProperties: {extProperties} is not supported. Needs 9.0.5.0 or higher. Ignoring extProperties for this call.")
        else:
            json_data['extProperties'] = extProperties
    elif 'extProperties' in ret_obj['data']:
        if ret_obj['data']['extProperties'] is not None:
            json_data['extProperties'] = ret_obj['data']['extProperties']
        else:
            del ret_obj['data']['extProperties']
    if introspectWithSecret is not None:
        if tools.version_compare(isamAppliance.facts["version"], "9.0.7.0") < 0:
            warnings.append(
                f"Appliance at version: {isamAppliance.facts['version']}, introspectWithSecret: {introspectWithSecret} is not supported. Needs 9.0.7.0 or higher. Ignoring introspectWithSecret for this call.")
        else:
            json_data["introspectWithSecret"] = introspectWithSecret
    elif 'introspectWithSecret' in ret_obj['data']:
        if ret_obj['data']['introspectWithSecret'] is not None:
            json_data['introspectWithSecret'] = ret_obj['data']['introspectWithSecret']
        else:
            del ret_obj['data']['introspectWithSecret']

    sorted_ret_obj = tools.json_sort(ret_obj['data'])
    sorted_json_data = tools.json_sort(json_data)
    logger.debug(f"Sorted Existing Data:{sorted_ret_obj}")
    logger.debug(f"Sorted Desired  Data:{sorted_json_data}")
    if sorted_ret_obj != sorted_json_data:
        needs_update = True

    if force is True or needs_update is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_put(
                "Update a specified mapping rule", f"{uri}/{id}", json_data,
                requires_modules=requires_modules, requires_version=requires_version, warnings=warnings)

    return isamAppliance.create_return_object(warnings=warnings)


def set(isamAppliance, name, definitionName, companyName, redirectUri=None, companyUrl=None, contactPerson=None,
        contactType=None, email=None, phone=None, otherInfo=None, clientId=None, clientSecret=None, new_name=None,
        requirePkce=None, encryptionDb=None, encryptionCert=None, jwksUri=None, extProperties=None, introspectWithSecret=None,
        check_mode=False, force=False):
    """
    Creating or Modifying an API Protection Definition
    """
    if (search(isamAppliance, name=name))['data'] == {}:
        # Force the add - we already know policy does not exist
        logger.info(f"Definition {name} had no match, requesting to add new one.")
        return add(isamAppliance, name, definitionName, companyName, redirectUri=redirectUri, companyUrl=companyUrl,
                   contactPerson=contactPerson, contactType=contactType, email=email, phone=phone, otherInfo=otherInfo,
                   clientId=clientId, clientSecret=clientSecret, requirePkce=requirePkce, encryptionDb=encryptionDb,
                   encryptionCert=encryptionCert, jwksUri=jwksUri, extProperties=extProperties, introspectWithSecret=introspectWithSecret,
                   check_mode=check_mode, force=True)
    else:
        # Update request
        logger.info(f"Definition {name} exists, requesting to update.")
        return update(isamAppliance, name, definitionName, companyName, redirectUri=redirectUri, companyUrl=companyUrl,
                      contactPerson=contactPerson, contactType=contactType, email=email, phone=phone,
                      otherInfo=otherInfo, clientId=clientId, clientSecret=clientSecret, new_name=new_name,
                      requirePkce=requirePkce, encryptionDb=encryptionDb, encryptionCert=encryptionCert,
                      jwksUri=jwksUri, extProperties=extProperties, introspectWithSecret=introspectWithSecret, check_mode=check_mode, force=force)

def update_id(isamAppliance, clientId, name, definitionName, companyName, redirectUri=None, companyUrl=None, contactPerson=None,
           contactType=None, email=None, phone=None, otherInfo=None, clientSecret=None,
           requirePkce=None, encryptionDb=None, encryptionCert=None, jwksUri=None, extProperties=None, introspectWithSecret=None,
           check_mode=False, force=False, new_clientId=None):
    """
    Update a specified mapping rule
    """

    ret_obj = definitions.search(isamAppliance, definitionName, check_mode=check_mode, force=force)
    if ret_obj['data'] == {}:
        warnings = ret_obj["warnings"]
        warnings.append(
            f"API Protection Definition {definitionName} is not found. Cannot process client request.")
        return isamAppliance.create_return_object(warnings=warnings)
    else:
        definition = ret_obj['data']

    ret_obj = _get_id(isamAppliance, clientId=clientId)
    warnings = ret_obj["warnings"]

    if ret_obj["data"] == {}:
        warnings.append(f"Client {clientId} not found, skipping update.")
        return isamAppliance.create_return_object(warnings=warnings)
    else:
        id = ret_obj["data"]["id"]

    needs_update = False
    # Create a simple json with just the main client attributes
    json_data = {
        "definition": definition,
        "companyName": companyName,
        "name": name
    }

    if new_clientId is not None:
        json_data['clientId'] = new_clientId
    else:
        json_data['clientId'] = clientId

    del ret_obj['data']['id']
    # Add attributes that have been supplied... otherwise skip them.
    if redirectUri is not None:
        json_data['redirectUri'] = redirectUri
    elif 'redirectUri' in ret_obj['data']:
        if ret_obj['data']['redirectUri'] is not None:
            json_data["redirectUri"] = ret_obj['data']['redirectUri']
        else:
            del ret_obj['data']['redirectUri']
    if companyUrl is not None:
        json_data["companyUrl"] = companyUrl
    elif 'companyUrl' in ret_obj['data']:
        if ret_obj['data']['companyUrl'] is not None:
            json_data["companyUrl"] = ret_obj['data']['companyUrl']
        else:
            del ret_obj['data']['companyUrl']
    if contactPerson is not None:
        json_data["contactPerson"] = contactPerson
    elif 'contactPerson' in ret_obj['data']:
        if ret_obj['data']['contactPerson'] is not None:
            json_data["contactPerson"] = ret_obj['data']['contactPerson']
        else:
            del ret_obj['data']['contactPerson']
    if contactType is not None:
        json_data["contactType"] = contactType
    elif 'contactType' in ret_obj['data']:
        if ret_obj['data']['contactType'] is not None:
            json_data["contactType"] = ret_obj['data']['contactType']
        else:
            del ret_obj['data']['contactType']
    if email is not None:
        json_data["email"] = email
    elif 'email' in ret_obj['data']:
        if ret_obj['data']['email'] is not None:
            json_data["email"] = ret_obj['data']['email']
        else:
            del ret_obj['data']['email']
    if phone is not None:
        json_data["phone"] = phone
    elif 'phone' in ret_obj['data']:
        if ret_obj['data']['phone'] is not None:
            json_data["phone"] = ret_obj['data']['phone']
        else:
            del ret_obj['data']['phone']
    if otherInfo is not None:
        json_data["otherInfo"] = otherInfo
    elif 'otherInfo' in ret_obj['data']:
        if ret_obj['data']['otherInfo'] is not None:
            json_data["otherInfo"] = ret_obj['data']['otherInfo']
        else:
            del ret_obj['data']['otherInfo']
    if clientSecret is not None:
        json_data["clientSecret"] = clientSecret
    elif 'clientSecret' in ret_obj['data']:
        if ret_obj['data']['clientSecret'] is not None:
            json_data["clientSecret"] = ret_obj['data']['clientSecret']
        else:
            del ret_obj['data']['clientSecret']
    if requirePkce is not None:
        if tools.version_compare(isamAppliance.facts["version"], "9.0.4.0") < 0:
            warnings.append(
                f"Appliance at version: {isamAppliance.facts['version']}, requirePkce: {requirePkce} is not supported. Needs 9.0.4.0 or higher. Ignoring requirePkce for this call.")
        else:
            json_data["requirePkce"] = requirePkce
    elif 'requirePkce' in ret_obj['data']:
        if ret_obj['data']['requirePkce'] is not None:
            json_data["requirePkce"] = ret_obj['data']['requirePkce']
        else:
            del ret_obj['data']['requirePkce']
    if encryptionDb is not None:
        if tools.version_compare(isamAppliance.facts["version"], "9.0.4.0") < 0:
            warnings.append(
                f"Appliance at version: {isamAppliance.facts['version']}, encryptionDb: {encryptionDb} is not supported. Needs 9.0.4.0 or higher. Ignoring encryptionDb for this call.")
        else:
            json_data["encryptionDb"] = encryptionDb
    elif 'encryptionDb' in ret_obj['data']:
        if ret_obj['data']['encryptionDb'] is not None:
            json_data["encryptionDb"] = ret_obj['data']['encryptionDb']
        else:
            del ret_obj['data']['encryptionDb']
    if encryptionCert is not None:
        if tools.version_compare(isamAppliance.facts["version"], "9.0.4.0") < 0:
            warnings.append(
                f"Appliance at version: {isamAppliance.facts['version']}, encryptionCert: {encryptionCert} is not supported. Needs 9.0.4.0 or higher. Ignoring encryptionCert for this call.")
        else:
            json_data["encryptionCert"] = encryptionCert
    elif 'encryptionCert' in ret_obj['data']:
        if ret_obj['data']['encryptionCert'] is not None:
            json_data["encryptionCert"] = ret_obj['data']['encryptionCert']
        else:
            del ret_obj['data']['encryptionCert']
    if jwksUri is not None:
        if tools.version_compare(isamAppliance.facts["version"], "9.0.4.0") < 0:
            warnings.append(
                f"Appliance at version: {isamAppliance.facts['version']}, jwksUri: {jwksUri} is not supported. Needs 9.0.4.0 or higher. Ignoring jwksUri for this call.")
        else:
            json_data["jwksUri"] = jwksUri
    elif 'jwksUri' in ret_obj['data']:
        if ret_obj['data']['jwksUri'] is not None:
            json_data["jwksUri"] = ret_obj['data']['jwksUri']
        else:
            del ret_obj['data']['jwksUri']
    if extProperties is not None:
        if tools.version_compare(isamAppliance.facts["version"], "9.0.5.0") < 0:
            warnings.append(
                f"Appliance at version: {isamAppliance.facts['version']}, extProperties: {extProperties} is not supported. Needs 9.0.5.0 or higher. Ignoring extProperties for this call.")
        else:
            json_data["extProperties"] = extProperties
    elif 'extProperties' in ret_obj['data']:
        if ret_obj['data']['extProperties'] is not None:
            json_data["extProperties"] = ret_obj['data']['extProperties']
        else:
            del ret_obj['data']['extProperties']
    if introspectWithSecret is not None:
        if tools.version_compare(isamAppliance.facts["version"], "9.0.7.0") < 0:
            warnings.append(
                f"Appliance at version: {isamAppliance.facts['version']}, introspectWithSecret: {introspectWithSecret} is not supported. Needs 9.0.7.0 or higher. Ignoring introspectWithSecret for this call.")
        else:
            json_data["introspectWithSecret"] = introspectWithSecret
    elif 'introspectWithSecret' in ret_obj['data']:
        if ret_obj['data']['introspectWithSecret'] is not None:
            json_data["introspectWithSecret"] = ret_obj['data']['introspectWithSecret']
        else:
            del ret_obj['data']['introspectWithSecret']

    sorted_ret_obj = tools.json_sort(ret_obj['data'])
    sorted_json_data = tools.json_sort(json_data)
    logger.debug(f"Sorted Existing Data:{sorted_ret_obj}")
    logger.debug(f"Sorted Desired  Data:{sorted_json_data}")
    if sorted_ret_obj != sorted_json_data:
        needs_update = True

    if force is True or needs_update is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_put(
                "Update a specified mapping rule", f"{uri}/{id}", json_data,
                requires_modules=requires_modules, requires_version=requires_version, warnings=warnings)

    return isamAppliance.create_return_object(warnings=warnings)


def set_id(isamAppliance, clientId, name, definitionName, companyName, redirectUri=None, companyUrl=None, contactPerson=None,
        contactType=None, email=None, phone=None, otherInfo=None, clientSecret=None, new_clientId=None,
        requirePkce=None, encryptionDb=None, encryptionCert=None, jwksUri=None, extProperties=None, introspectWithSecret=None,
        check_mode=False, force=False):
    """
    Creating or Modifying an API Protection Definition
    """
    if (search_id(isamAppliance, clientId))['data'] == {}:
        # Force the add - we already know policy does not exist
        logger.info(f"Definition {clientId} had no match, requesting to add new one.")
        return add(isamAppliance, name=name, definitionName=definitionName, companyName=companyName, redirectUri=redirectUri, companyUrl=companyUrl,
                   contactPerson=contactPerson, contactType=contactType, email=email, phone=phone, otherInfo=otherInfo,
                   clientId=clientId, clientSecret=clientSecret, requirePkce=requirePkce, encryptionDb=encryptionDb,
                   encryptionCert=encryptionCert, jwksUri=jwksUri, extProperties=extProperties, introspectWithSecret=introspectWithSecret,
                   check_mode=check_mode, force=True)
    else:
        # Update request
        logger.info(f"Definition {clientId} exists, requesting to update.")
        return update_id(isamAppliance, clientId=clientId, definitionName=definitionName, companyName=companyName, name=name, redirectUri=redirectUri, companyUrl=companyUrl,
                      contactPerson=contactPerson, contactType=contactType, email=email, phone=phone,
                      otherInfo=otherInfo, clientSecret=clientSecret, new_clientId=new_clientId,
                      requirePkce=requirePkce, encryptionDb=encryptionDb, encryptionCert=encryptionCert,
                      jwksUri=jwksUri, extProperties=extProperties, introspectWithSecret=introspectWithSecret, check_mode=check_mode, force=force)


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

    return tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['id', 'definition'])
