import logging

from ibmsecurity.isam.fed import attribute_source
from ibmsecurity.utilities import tools
from ibmsecurity.isam.aac import access_policy

logger = logging.getLogger(__name__)

# URI for this module
uri = "/iam/access/v8/definitions"
requires_modules = ["mga", "federation"]
requires_version = None

try:
    basestring
except NameError:
    basestring = (str, bytes)


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieve a list of API protection definitions
    """
    return isamAppliance.invoke_get("Retrieve a list of API protection definitions", uri,
                                    requires_modules=requires_modules,
                                    requires_version=requires_version)


def get(isamAppliance, name, check_mode=False, force=False):
    """
    Retrieve a specific API protection definition
    """
    ret_obj = search(isamAppliance, name=name, check_mode=check_mode, force=force)
    defn_id = ret_obj['data']
    warnings = ret_obj["warnings"]

    if defn_id == {}:
        logger.info(f"Definition {name} had no match, skipping retrieval.")
        warnings.append(f"Definition Name {name} had no match.")
        return isamAppliance.create_return_object(warnings=warnings)
    else:
        return _get(isamAppliance, defn_id)


def _get(isamAppliance, defn_id):
    return isamAppliance.invoke_get("Retrieve a specific API protection definition",
                                    f"{uri}/{defn_id}", requires_modules=requires_modules,
                                    requires_version=requires_version)


def search(isamAppliance, name, check_mode=False, force=False):
    """
    Search definition id by name
    """
    ret_obj = get_all(isamAppliance)
    return_obj = isamAppliance.create_return_object()
    return_obj["warnings"] = ret_obj["warnings"]

    for obj in ret_obj['data']:
        if obj['name'] == name:
            logger.info(f"Found definition {name} id: {obj['id']}")
            return_obj['data'] = obj['id']
            return_obj['rc'] = 0

    return return_obj


def add(isamAppliance, name, description="", accessPolicyName=None, grantTypes=["AUTHORIZATION_CODE"],
        tcmBehavior="NEVER_PROMPT",
        accessTokenLifetime=3600, accessTokenLength=20, enforceSingleUseAuthorizationGrant=False,
        authorizationCodeLifetime=300, authorizationCodeLength=30, issueRefreshToken=True, refreshTokenLength=40,
        maxAuthorizationGrantLifetime=604800, enforceSingleAccessTokenPerGrant=False,
        enableMultipleRefreshTokensForFaultTolerance=False, pinPolicyEnabled=False, pinLength=4,
        tokenCharSet="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", oidc=None, check_mode=False,
        force=False):
    """
    Create an API protection definition
    """
    if (isinstance(grantTypes, basestring)):
        import ast
        grantTypes = ast.literal_eval(grantTypes)

    ret_obj = search(isamAppliance, name=name, check_mode=check_mode, force=force)
    warnings = ret_obj["warnings"]

    if force is True or ret_obj["data"] == {}:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            json_data = {
                "name": name,
                "description": description,
                "grantTypes": grantTypes,
                "tcmBehavior": tcmBehavior,
                "accessTokenLifetime": int(accessTokenLifetime),
                "accessTokenLength": int(accessTokenLength),
                "enforceSingleUseAuthorizationGrant": enforceSingleUseAuthorizationGrant,
                "authorizationCodeLifetime": int(authorizationCodeLifetime),
                "authorizationCodeLength": int(authorizationCodeLength),
                "issueRefreshToken": issueRefreshToken,
                "refreshTokenLength": int(refreshTokenLength),
                "maxAuthorizationGrantLifetime": int(maxAuthorizationGrantLifetime),
                "enforceSingleAccessTokenPerGrant": enforceSingleAccessTokenPerGrant,
                "enableMultipleRefreshTokensForFaultTolerance": enableMultipleRefreshTokensForFaultTolerance,
                "pinPolicyEnabled": pinPolicyEnabled,
                "pinLength": int(pinLength),
                "tokenCharSet": tokenCharSet
            }
            if accessPolicyName is not None:
                if tools.version_compare(isamAppliance.facts["version"], "9.0.4.0") < 0:
                    warnings.append(
                        f"Appliance at version: {isamAppliance.facts['version']}, access policy: {oidc} is not supported. Needs 9.0.4.0 or higher. Ignoring access policy for this call.")
                    accessPolicyName = None
                else:
                    ap_ret_obj = access_policy.search(isamAppliance, accessPolicyName, check_mode=check_mode, force=force)
                    if ap_ret_obj['data'] == {}:
                        warnings = ap_ret_obj["warnings"]
                        warnings.append(
                            f"Access Policy {accessPolicyName} is not found. Cannot add definition.")
                        return isamAppliance.create_return_object(warnings=warnings)
                    else:
                        json_data["accessPolicyId"] = int(ap_ret_obj['data'])

            if oidc is not None:
                if tools.version_compare(isamAppliance.facts["version"], "9.0.4.0") < 0:
                    warnings.append(
                        f"Appliance at version: {isamAppliance.facts['version']}, oidc: {oidc} is not supported. Needs 9.0.4.0 or higher. Ignoring oidc for this call.")
                else:
                    if 'attributeSources' in oidc:
                        oidc['attributeSources'] = _map_oidc_attributeSources(isamAppliance, oidc['attributeSources'], check_mode, force)
                    json_data["oidc"] = oidc
                if 'dynamicClients' in json_data['oidc']:
                    if tools.version_compare(isamAppliance.facts["version"], "9.0.5.0") < 0:
                        warnings.append(
                            f"Appliance at version: {isamAppliance.facts['version']}, dynamicClients: {json_data['oidc']['dynamicClients']} is not supported. Needs 9.0.5.0 or higher. Ignoring dynamicClients for this call.")
                        del json_data['oidc']['dynamicClients']
                if 'issueSecret' in json_data['oidc']:
                    if tools.version_compare(isamAppliance.facts["version"], "9.0.5.0") < 0:
                        warnings.append(
                            f"Appliance at version: {isamAppliance.facts['version']}, issueSecret: {json_data['oidc']['issueSecret']} is not supported. Needs 9.0.5.0 or higher. Ignoring issueSecret for this call.")
                        json_data['oidc'].pop('issueSecret', None)
                if 'includeIssInAuthResp' in json_data['oidc']:
                    if tools.version_compare(isamAppliance.facts["version"], "10.0.8.0") < 0:
                        warnings.append(
                            f"Appliance at version: {isamAppliance.facts['version']}, issueSecret: {json_data['oidc']['includeIssInAuthResp']} is not supported. Needs 10.0.8.0 or higher. Ignoring includeIssInAuthResp for this call.")
                        json_data['oidc'].pop('includeIssInAuthResp', None)

            return isamAppliance.invoke_post(
                "Create an API protection definition", uri,
                json_data, requires_modules=requires_modules, requires_version=requires_version, warnings=warnings)

    return isamAppliance.create_return_object(warnings=warnings)


def delete(isamAppliance, name, check_mode=False, force=False):
    """
    Delete an API protection definition
    """
    ret_obj = search(isamAppliance, name, check_mode=check_mode, force=force)
    defn_id = ret_obj['data']
    warnings = ret_obj["warnings"]

    if defn_id == {}:
        logger.info(f"Definition {name} not found, skipping delete.")
    else:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_delete(
                "Delete an API protection definition",
                f"{uri}/{defn_id}", requires_modules=requires_modules,
                requires_version=requires_version, warnings=warnings)

    return isamAppliance.create_return_object(warnings=warnings)


def update(isamAppliance, name, description="", accessPolicyName=None, grantTypes=["AUTHORIZATION_CODE"],
           tcmBehavior="NEVER_PROMPT",
           accessTokenLifetime=3600, accessTokenLength=20, enforceSingleUseAuthorizationGrant=False,
           authorizationCodeLifetime=300, authorizationCodeLength=30, issueRefreshToken=True, refreshTokenLength=40,
           maxAuthorizationGrantLifetime=604800, enforceSingleAccessTokenPerGrant=False,
           enableMultipleRefreshTokensForFaultTolerance=False, pinPolicyEnabled=False, pinLength=4,
           tokenCharSet="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", oidc=None, check_mode=False,
           force=False):
    """
    Update a specified API protection definition
    """
    ret_obj = get(isamAppliance, name)
    warnings = ret_obj["warnings"]

    if ret_obj["data"] == {}:
        warnings.append(f"Definiton {name} not found, skipping update.")
        return isamAppliance.create_return_object(warnings=warnings)
    else:
        defn_id = ret_obj["data"]["id"]

    needs_update = False
    json_data = {
        "name": name,
        "description": description,
        "grantTypes": grantTypes,
        "tcmBehavior": tcmBehavior,
        "accessTokenLifetime": int(accessTokenLifetime),
        "accessTokenLength": int(accessTokenLength),
        "enforceSingleUseAuthorizationGrant": enforceSingleUseAuthorizationGrant,
        "authorizationCodeLifetime": int(authorizationCodeLifetime),
        "authorizationCodeLength": int(authorizationCodeLength),
        "issueRefreshToken": issueRefreshToken,
        "refreshTokenLength": int(refreshTokenLength),
        "maxAuthorizationGrantLifetime": int(maxAuthorizationGrantLifetime),
        "enforceSingleAccessTokenPerGrant": enforceSingleAccessTokenPerGrant,
        "enableMultipleRefreshTokensForFaultTolerance": enableMultipleRefreshTokensForFaultTolerance,
        "pinPolicyEnabled": pinPolicyEnabled,
        "pinLength": int(pinLength),
        "tokenCharSet": tokenCharSet
    }
    if accessPolicyName is not None:
        if tools.version_compare(isamAppliance.facts["version"], "9.0.4.0") < 0:
            warnings.append(
                f"Appliance at version: {isamAppliance.facts['version']}, access policy: {oidc} is not supported. Needs 9.0.4.0 or higher. Ignoring access policy for this call.")
            accessPolicyName = None
        else:
            ap_ret_obj = access_policy.search(isamAppliance, accessPolicyName, check_mode=check_mode, force=force)
            if ap_ret_obj['data'] == {}:
                warnings = ap_ret_obj["warnings"]
                warnings.append(
                    f"Access Policy {accessPolicyName} is not found. Cannot update definition.")
                return isamAppliance.create_return_object(warnings=warnings)
            else:
                json_data["accessPolicyId"] = int(ap_ret_obj['data'])

    if oidc is not None:
        if tools.version_compare(isamAppliance.facts["version"], "9.0.4.0") < 0:
            warnings.append(
                f"Appliance at version: {isamAppliance.facts['version']}, oidc: {oidc} is not supported. Needs 9.0.4.0 or higher. Ignoring oidc for this call.")
            oidc = None
        else:
            if 'attributeSources' in oidc:
                oidc['attributeSources'] = _map_oidc_attributeSources(isamAppliance, oidc['attributeSources'], check_mode, force)
            json_data["oidc"] = oidc

    if not force:

        ret_obj['data'].pop('datecreated', None)
        ret_obj['data'].pop('id', None)
        ret_obj['data'].pop('lastmodified', None)
        ret_obj['data'].pop('mappingRules', None)

        # Inspecting oidcConfig and remove missing or None attributes in returned object
        if oidc is not None and 'oidc' in ret_obj['data']:
            if 'enabled' in ret_obj['data']['oidc'] and ret_obj['data']['oidc']['enabled'] is None:
                del ret_obj['data']['oidc']['enabled']
            if 'iss' in ret_obj['data']['oidc'] and ret_obj['data']['oidc']['iss'] is None:
                del ret_obj['data']['oidc']['iss']
            if 'poc' in ret_obj['data']['oidc'] and ret_obj['data']['oidc']['poc'] is None:
                del ret_obj['data']['oidc']['poc']
            if 'lifetime' in ret_obj['data']['oidc'] and ret_obj['data']['oidc']['lifetime'] is None:
                del ret_obj['data']['oidc']['lifetime']
            if 'alg' in ret_obj['data']['oidc'] and ret_obj['data']['oidc']['alg'] is None:
                del ret_obj['data']['oidc']['alg']
            if 'db' in ret_obj['data']['oidc'] and ret_obj['data']['oidc']['db'] is None:
                del ret_obj['data']['oidc']['db']
            if 'cert' in ret_obj['data']['oidc'] and ret_obj['data']['oidc']['cert'] is None:
                del ret_obj['data']['oidc']['cert']
            if 'attributeSources' in ret_obj['data']['oidc'] and ret_obj['data']['oidc']['attributeSources'] is None:
                del ret_obj['data']['oidc']['attributeSources']

            # Inspecting oidcEncConfig and remove missing or None attributes in returned object
            if 'enc' in ret_obj['data']['oidc'] and ret_obj['data']['oidc']['enc'] is not None:
                if 'enabled' in ret_obj['data']['oidc']['enc'] and ret_obj['data']['oidc']['enc']['enabled'] is None:
                    del ret_obj['data']['oidc']['enc']['enabled']
                if 'alg' in ret_obj['data']['oidc']['enc'] and ret_obj['data']['oidc']['enc']['alg'] is None:
                    del ret_obj['data']['oidc']['enc']['alg']
                if 'enc' in ret_obj['data']['oidc']['enc'] and ret_obj['data']['oidc']['enc']['enc'] is None:
                    del ret_obj['data']['oidc']['enc']['enc']

            # For dynamicClients & issueSecret parameters
            #
            # If the values for dynamicClients or issueSecret are missing, then they are
            # considered to be of the value "false" by the appliance, this allows for old
            # configuration to be forward compatible, without the function of the
            # definition being changed by the same payload.
            if 'dynamicClients' in json_data['oidc']:
                if tools.version_compare(isamAppliance.facts["version"], "9.0.5.0") < 0:
                    warnings.append(
                        f"Appliance at version: {isamAppliance.facts['version']}, dynamicClients: {json_data['oidc']['dynamicClients']} is not supported. Needs 9.0.5.0 or higher. Ignoring dynamicClients for this call.")
                    del json_data['oidc']['dynamicClients']
            else:
                if tools.version_compare(isamAppliance.facts["version"], "9.0.5.0") >= 0:
                    if 'dynamicClients' in ret_obj['data']['oidc'] and ret_obj['data']['oidc'][
                        'dynamicClients'] is False:
                        del ret_obj['data']['oidc']['dynamicClients']

            if 'issueSecret' in json_data['oidc']:
                if tools.version_compare(isamAppliance.facts["version"], "9.0.5.0") < 0:
                    warnings.append(
                        f"Appliance at version: {isamAppliance.facts['version']}, issueSecret: {json_data['oidc']['issueSecret']} is not supported. Needs 9.0.5.0 or higher. Ignoring issueSecret for this call.")
                    del json_data['oidc']['issueSecret']
            else:
                if tools.version_compare(isamAppliance.facts["version"], "9.0.5.0") >= 0:
                    if 'issueSecret' in ret_obj['data']['oidc'] and ret_obj['data']['oidc']['issueSecret'] is False:
                        del ret_obj['data']['oidc']['issueSecret']

            if 'fapiCompliant' in ret_obj['data']['oidc'] and 'fapiCompliant' not in json_data['oidc']:
                del ret_obj['data']['oidc']['fapiCompliant']
            if 'oidcCompliant' in ret_obj['data']['oidc'] and 'oidcCompliant' not in json_data['oidc']:
                del ret_obj['data']['oidc']['oidcCompliant']

        if oidc is None and 'oidc' in ret_obj['data']:
            del ret_obj['data']['oidc']

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
                "Update a specified API protection definition",
                f"{uri}/{defn_id}", json_data, requires_modules=requires_modules,
                requires_version=requires_version, warnings=warnings)

    return isamAppliance.create_return_object(warnings=warnings)


def set(isamAppliance, name, description="", accessPolicyName=None, grantTypes=["AUTHORIZATION_CODE"],
        tcmBehavior="NEVER_PROMPT",
        accessTokenLifetime=3600, accessTokenLength=20, enforceSingleUseAuthorizationGrant=False,
        authorizationCodeLifetime=300, authorizationCodeLength=30, issueRefreshToken=True, refreshTokenLength=40,
        maxAuthorizationGrantLifetime=604800, enforceSingleAccessTokenPerGrant=False,
        enableMultipleRefreshTokensForFaultTolerance=False, pinPolicyEnabled=False, pinLength=4,
        tokenCharSet="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", oidc=None, check_mode=False,
        force=False):
    """
    Creating or Modifying an API Protection Definition
    """
    ### Fix for issue #252 ###
    if oidc is not None and 'lifetime' in oidc and oidc['lifetime'] is not None:
        oidc['lifetime'] = int(oidc['lifetime'])

    if (search(isamAppliance, name=name))['data'] == {}:
        # Force the add - we already know policy does not exist
        logger.info(f"Definition {name} had no match, requesting to add new one.")
        return add(isamAppliance=isamAppliance, name=name, description=description, accessPolicyName=accessPolicyName,
                   grantTypes=grantTypes, tcmBehavior=tcmBehavior,
                   accessTokenLifetime=accessTokenLifetime, accessTokenLength=accessTokenLength,
                   enforceSingleUseAuthorizationGrant=enforceSingleUseAuthorizationGrant,
                   authorizationCodeLifetime=authorizationCodeLifetime, authorizationCodeLength=authorizationCodeLength,
                   issueRefreshToken=issueRefreshToken, refreshTokenLength=refreshTokenLength,
                   maxAuthorizationGrantLifetime=maxAuthorizationGrantLifetime,
                   enforceSingleAccessTokenPerGrant=enforceSingleAccessTokenPerGrant,
                   enableMultipleRefreshTokensForFaultTolerance=enableMultipleRefreshTokensForFaultTolerance,
                   pinPolicyEnabled=pinPolicyEnabled, pinLength=pinLength,
                   tokenCharSet=tokenCharSet, oidc=oidc, check_mode=check_mode, force=True)
    else:
        # Update request
        logger.info(f"Definition {name} exists, requesting to update.")
        return update(isamAppliance=isamAppliance, name=name, description=description,
                      accessPolicyName=accessPolicyName,
                      grantTypes=grantTypes, tcmBehavior=tcmBehavior,
                      accessTokenLifetime=accessTokenLifetime, accessTokenLength=accessTokenLength,
                      enforceSingleUseAuthorizationGrant=enforceSingleUseAuthorizationGrant,
                      authorizationCodeLifetime=authorizationCodeLifetime,
                      authorizationCodeLength=authorizationCodeLength, issueRefreshToken=issueRefreshToken,
                      refreshTokenLength=refreshTokenLength,
                      maxAuthorizationGrantLifetime=maxAuthorizationGrantLifetime,
                      enforceSingleAccessTokenPerGrant=enforceSingleAccessTokenPerGrant,
                      enableMultipleRefreshTokensForFaultTolerance=enableMultipleRefreshTokensForFaultTolerance,
                      pinPolicyEnabled=pinPolicyEnabled, pinLength=pinLength,
                      tokenCharSet=tokenCharSet, oidc=oidc, check_mode=check_mode, force=force)


def _map_oidc_attributeSources(isamAppliance, attributeSources, check_mode=False, force=False):
    """
     Maps OIDC definition attributeSources from a string name to an ID
     :param isamAppliance: ISAM Appliance to act on
     :param attributeSources: Attribute sources to convert from string to integer
     :param check_mode: Ignored
     :param force: Ignored
     :return: attributeSources with attribute id mapped from attribute name
    """

    if attributeSources is not None:
        attr_lookup = None
        for source in attributeSources:
            # Only perform mapping if attributeSourceId is not an integer (this provides backwards compatibility)
            if not source['attributeSourceId'].isdigit():
                if not attr_lookup:
                    attr_lookup = attribute_source.get_all(isamAppliance, check_mode=check_mode, force=force)['data']
                for attr in attr_lookup:
                    if attr['name'] == source['attributeSourceId']:
                        source['attributeSourceId'] = attr['id']

    return attributeSources


def compare(isamAppliance1, isamAppliance2):
    """
    Compare API Protection Definitions between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    for obj in ret_obj1['data']:
        del obj['id']
        del obj['datecreated']
        del obj['lastmodified']
        for rules in obj['mappingRules']:
            del rules['id']
    for obj in ret_obj2['data']:
        del obj['id']
        del obj['datecreated']
        del obj['lastmodified']
        for rules in obj['mappingRules']:
            del rules['id']

    return tools.json_compare(ret_obj1, ret_obj2,
                              deleted_keys=['id', 'datecreated', 'lastmodified',
                                            'mappingRules/id'])
