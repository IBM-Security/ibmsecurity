import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/openid"


def get_all(isvgAppliance, check_mode=False, force=False):
    """
    Retrieve all openid entries
    """
    return isvgAppliance.invoke_get("Retrieve all openid entries", "{0}".format(uri))


def search(isvgAppliance, name, check_mode=False, force=False):
    """
    Search for existing openid.
    Just care for presence of openid, not its actual value.
    """
    ret_obj = get_all(isvgAppliance)
    return_obj = isvgAppliance.create_return_object()

    for obj in ret_obj['data']:
        if obj['name'] == name:
            logger.info("Found openid entry {0}".format(name))
            return_obj['data'] = obj
            return_obj['rc'] = 0
            break

    return return_obj


def add(isvgAppliance, name, clientID, secret, certAlias, domains, issuerIdentifier, redirectToRPHostPort, userRealm, authUrl, tokenUrl, jwkUrl, logoffUrl, discoveryUrl, advanced, signAlgorithm, userIDToCreateSubject, scope, check_mode=False, force=False):
    """
    Create an openid entry
    """
    if force is True:
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True)
        else:
            # Create a simple json with just the openid entry
            openid_json = {
                "name": name,
                "clientID": clientID,
                "secret": secret,
                "certAlias": certAlias,
                "domains": domains,
                "issuerIdentifier": issuerIdentifier,
                "redirectToRPHostPort": redirectToRPHostPort,
                "userRealm": userRealm,
                "authUrl": authUrl,
                "tokenUrl": tokenUrl,
                "jwkUrl": jwkUrl,
                "logoffUrl": logoffUrl,
                "discoveryUrl": discoveryUrl,
                "advanced": advanced,
                "signAlgorithm": signAlgorithm,
                "scope": scope,
                "userIDToCreateSubject": userIDToCreateSubject
            }

            return isvgAppliance.invoke_post(
                "Create a new openid entry", uri, openid_json)

    return isvgAppliance.create_return_object(changed=False)


def delete(isvgAppliance, name, check_mode=False, force=False):
    """
    Delete an openid entry
    """
    ret_obj = search(isvgAppliance, name, check_mode=check_mode, force=force)
    warnings = ret_obj['warnings']

    if force is True or ret_obj['data'] != {}:
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            uuid = ret_obj['data']['uuid']
            return isvgAppliance.invoke_delete(
                "Delete a openid entry", "{0}/{1}".format(uri, uuid), warnings=warnings)

    return isvgAppliance.create_return_object(warnings=warnings)


def update(isvgAppliance, name, clientID, secret, certAlias, domains, issuerIdentifier, redirectToRPHostPort, userRealm, authUrl, tokenUrl, jwkUrl, logoffUrl, discoveryUrl, advanced, signAlgorithm, userIDToCreateSubject, scope, check_mode=False, force=False):
    """
    Updating an openid entry
    """
    ret_obj = search(isvgAppliance, name, check_mode=check_mode, force=force)
    warnings = ret_obj['warnings']

    uuid = ret_obj['data']['uuid']

    needs_update = False

    # Create a simple json with just the attributes
    json_data = {
        "name": name,
        "uuid": uuid
    }

    if clientID is not None:
        json_data['clientID'] = clientID
    elif 'clientID' in ret_obj['data']:
        if ret_obj['data']['clientID'] is not None:
            json_data['clientID'] = ret_obj['data']['clientID']
        else:
            del ret_obj['data']['clientID']
    if secret is not None:
        json_data['secret'] = secret
    elif 'secret' in ret_obj['data']:
        if ret_obj['data']['secret'] is not None:
            json_data['secret'] = ret_obj['data']['secret']
        else:
            del ret_obj['data']['secret']
    if certAlias is not None:
        json_data['certAlias'] = certAlias
    elif 'certAlias' in ret_obj['data']:
        if ret_obj['data']['certAlias'] is not None:
            json_data['certAlias'] = ret_obj['data']['certAlias']
        else:
            del ret_obj['data']['certAlias']
    if domains is not None:
        json_data['domains'] = domains
    elif 'domains' in ret_obj['data']:
        if ret_obj['data']['domains'] is not None:
            json_data['domains'] = ret_obj['data']['domains']
        else:
            del ret_obj['data']['domains']
    if issuerIdentifier is not None:
        json_data['issuerIdentifier'] = issuerIdentifier
    elif 'issuerIdentifier' in ret_obj['data']:
        if ret_obj['data']['issuerIdentifier'] is not None:
            json_data['issuerIdentifier'] = ret_obj['data']['issuerIdentifier']
        else:
            del ret_obj['data']['issuerIdentifier']
    if redirectToRPHostPort is not None:
        json_data['redirectToRPHostPort'] = redirectToRPHostPort
    elif 'redirectToRPHostPort' in ret_obj['data']:
        if ret_obj['data']['redirectToRPHostPort'] is not None:
            json_data['redirectToRPHostPort'] = ret_obj['data']['redirectToRPHostPort']
        else:
            del ret_obj['data']['redirectToRPHostPort']
    if userRealm is not None:
        json_data['userRealm'] = userRealm
    elif 'userRealm' in ret_obj['data']:
        if ret_obj['data']['userRealm'] is not None:
            json_data['userRealm'] = ret_obj['data']['userRealm']
        else:
            del ret_obj['data']['userRealm']
    if authUrl is not None:
        json_data['authUrl'] = authUrl
    elif 'authUrl' in ret_obj['data']:
        if ret_obj['data']['authUrl'] is not None:
            json_data['authUrl'] = ret_obj['data']['authUrl']
        else:
            del ret_obj['data']['authUrl']
    if tokenUrl is not None:
        json_data['tokenUrl'] = tokenUrl
    elif 'tokenUrl' in ret_obj['data']:
        if ret_obj['data']['tokenUrl'] is not None:
            json_data['tokenUrl'] = ret_obj['data']['tokenUrl']
        else:
            del ret_obj['data']['tokenUrl']
    if logoffUrl is not None:
        json_data['logoffUrl'] = logoffUrl
    elif 'logoffUrl' in ret_obj['data']:
        if ret_obj['data']['logoffUrl'] is not None:
            json_data['logoffUrl'] = ret_obj['data']['logoffUrl']
        else:
            del ret_obj['data']['logoffUrl']
    if jwkUrl is not None:
        json_data['jwkUrl'] = jwkUrl
    elif 'jwkUrl' in ret_obj['data']:
        if ret_obj['data']['jwkUrl'] is not None:
            json_data['jwkUrl'] = ret_obj['data']['jwkUrl']
        else:
            del ret_obj['data']['jwkUrl']
    if discoveryUrl is not None:
        json_data['discoveryUrl'] = discoveryUrl
    elif 'discoveryUrl' in ret_obj['data']:
        if ret_obj['data']['discoveryUrl'] is not None:
            json_data['discoveryUrl'] = ret_obj['data']['discoveryUrl']
        else:
            del ret_obj['data']['discoveryUrl']
    if advanced is not None:
        json_data['advanced'] = advanced
    elif 'advanced' in ret_obj['data']:
        if ret_obj['data']['advanced'] is not None:
            json_data['advanced'] = ret_obj['data']['advanced']
        else:
            del ret_obj['data']['advanced']
    if signAlgorithm is not None:
        json_data['signAlgorithm'] = signAlgorithm
    elif 'signAlgorithm' in ret_obj['data']:
        if ret_obj['data']['signAlgorithm'] is not None:
            json_data['signAlgorithm'] = ret_obj['data']['signAlgorithm']
        else:
            del ret_obj['data']['signAlgorithm']
    if userIDToCreateSubject is not None:
        json_data['userIDToCreateSubject'] = userIDToCreateSubject
    elif 'userIDToCreateSubject' in ret_obj['data']:
        if ret_obj['data']['userIDToCreateSubject'] is not None:
            json_data['userIDToCreateSubject'] = ret_obj['data']['userIDToCreateSubject']
        else:
            del ret_obj['data']['userIDToCreateSubject']
    if scope is not None:
        json_data['scope'] = scope
    elif 'scope' in ret_obj['data']:
        if ret_obj['data']['scope'] is not None:
            json_data['scope'] = ret_obj['data']['scope']
        else:
            del ret_obj['data']['scope']

    sorted_ret_obj = tools.json_sort(ret_obj['data'])
    sorted_json_data = tools.json_sort(json_data)
    logger.debug("Sorted Existing Data:{0}".format(sorted_ret_obj))
    logger.debug("Sorted Desired  Data:{0}".format(sorted_json_data))
    if sorted_ret_obj != sorted_json_data:
        needs_update = True

    if force is True or needs_update is True:
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isvgAppliance.invoke_put(
                "Update an existing openid entry", "{0}/{1}".format(uri, uuid),
                json_data, warnings=warnings)

    return isvgAppliance.create_return_object(warnings=warnings)


def set(isvgAppliance, name, clientID, secret, certAlias, domains, issuerIdentifier, redirectToRPHostPort, userRealm, authUrl, tokenUrl, jwkUrl, logoffUrl, discoveryUrl, advanced, signAlgorithm="HS256", userIDToCreateSubject="sub", scope="openid", check_mode=False, force=False):
    """
    Creating or Modifying an openid entry
    """
    if (search(isvgAppliance, name))['data'] == {}:
        # Force the add - we already know object does not exist
        logger.info("Property {0} had no match, requesting to add new one.".format(name))
        return add(isvgAppliance, name, clientID, secret, certAlias, domains, issuerIdentifier, redirectToRPHostPort, userRealm, authUrl, tokenUrl, jwkUrl, logoffUrl, discoveryUrl, advanced, signAlgorithm, userIDToCreateSubject, scope, check_mode=check_mode, force=True)
    else:
        # Update request
        logger.info("Property {0} exists, requesting to update.".format(name))
        return update(isvgAppliance, name, clientID, secret, certAlias, domains, issuerIdentifier, redirectToRPHostPort, userRealm, authUrl, tokenUrl, jwkUrl, logoffUrl, discoveryUrl, advanced, signAlgorithm, userIDToCreateSubject, scope, check_mode=check_mode, force=force)
