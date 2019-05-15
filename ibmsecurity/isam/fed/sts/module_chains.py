import logging
import copy
from ibmsecurity.utilities import tools
from ibmsecurity.isam.fed.sts import templates
from ibmsecurity.isam.aac import mapping_rules

logger = logging.getLogger(__name__)

# URI for this module
uri = "/iam/access/v8/sts/chains"
requires_modules = ['federation']
requires_version = "9.0.1.0"


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieve a list of STS chains
    """
    return isamAppliance.invoke_get("Retrieve a list of STS chains", uri,
                                    requires_modules=requires_modules,
                                    requires_version=requires_version)


def search(isamAppliance, name, force=False, check_mode=False):
    """
    Search STS Chain by name
    """
    ret_obj = get_all(isamAppliance)
    return_obj = isamAppliance.create_return_object()

    for obj in ret_obj['data']:
        if obj['name'] == name:
            logger.info("Found STS Chain {0} id: {1}".format(name, obj['id']))
            return_obj['data'] = obj['id']
            return_obj['rc'] = 0

    return return_obj


def get(isamAppliance, name, check_mode=False, force=False):
    """
    Retrieve a specific STS chain
    """
    ret_obj = search(isamAppliance, name=name, check_mode=check_mode, force=force)
    id = ret_obj['data']

    if id == {}:
        warnings = ["STS Chain {0} had no match, skipping retrieval.".format(name)]
        return isamAppliance.create_return_object(warnings=warnings)
    else:
        return _get(isamAppliance, id)


def _get(isamAppliance, id):
    """
    Internal function to get data using "id" - used to avoid extra calls
    """
    return isamAppliance.invoke_get("Retrieve a specific STS chain", "{0}/{1}".format(uri, id),
                                    requires_modules=requires_modules,
                                    requires_version=requires_version)


def set(isamAppliance, name, chainName, requestType, description=None, tokenType=None, xPath=None, signResponses=None,
        signatureKey=None, validateRequests=None, validationKey=None, sendValidationConfirmation=None, issuer=None,
        appliesTo=None, properties=None, new_name=None, ignore_password_for_idempotency=False, check_mode=False,
        force=False):
    """
    Creating or Modifying an STS Chain
    """
    if (search(isamAppliance, name=name))['data'] == {}:
        # Force the add - we already know Chain does not exist
        logger.info("STS Chain {0} had no match, requesting to add new one.".format(name))
        return add(isamAppliance, name=name, chainName=chainName, requestType=requestType, description=description,
                   tokenType=tokenType, xPath=xPath, signResponses=signResponses, signatureKey=signatureKey,
                   validateRequests=validateRequests, validationKey=validationKey,
                   sendValidationConfirmation=sendValidationConfirmation, issuer=issuer, appliesTo=appliesTo,
                   properties=properties, check_mode=check_mode, force=True)
    else:
        # Update request
        logger.info("STS Chain {0} exists, requesting to update.".format(name))
        return update(isamAppliance, name=name, chainName=chainName, requestType=requestType, description=description,
                      tokenType=tokenType, xPath=xPath, signResponses=signResponses, signatureKey=signatureKey,
                      validateRequests=validateRequests, validationKey=validationKey,
                      sendValidationConfirmation=sendValidationConfirmation, issuer=issuer, appliesTo=appliesTo,
                      properties=properties, new_name=new_name,
                      ignore_password_for_idempotency=ignore_password_for_idempotency, check_mode=check_mode,
                      force=force)


def add(isamAppliance, name, chainName, requestType, description=None, tokenType=None, xPath=None, signResponses=None,
        signatureKey=None, validateRequests=None, validationKey=None, sendValidationConfirmation=None, issuer=None,
        appliesTo=None, properties=None, check_mode=False, force=False):
    """
    Create an STS chain
    """
    warnings = []
    if force is False:
        ret_obj = search(isamAppliance, name)

    if force is True or ret_obj['data'] == {}:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            ret_obj = templates.search(isamAppliance, name=chainName)
            if ret_obj['data'] == {}:
                warnings.append("Unable to find a valid STS Chain Template for {0}".format(chainName))
            else:
                chainId = ret_obj['data']
                json_data = {
                    "name": name,
                    "chainId": chainId,
                    "requestType": requestType
                }
                if description is not None:
                    json_data['description'] = description
                if tokenType is not None:
                    json_data['tokenType'] = tokenType
                if xPath is not None:
                    json_data['xPath'] = xPath
                if signResponses is not None:
                    json_data['signResponses'] = signResponses
                if signatureKey is not None:
                    json_data['signatureKey'] = signatureKey
                if validateRequests is not None:
                    json_data['validateRequests'] = validateRequests
                if validationKey is not None:
                    json_data['validationKey'] = validationKey
                if sendValidationConfirmation is not None:
                    json_data['sendValidationConfirmation'] = sendValidationConfirmation
                if issuer is not None:
                    json_data['issuer'] = issuer
                if appliesTo is not None:
                    json_data['appliesTo'] = appliesTo
                if properties is not None:
                    for idx, x in enumerate(properties['self']):
                        if "map.rule.reference.names" in x['name']:
                            ret_obj1 = mapping_rules.search(isamAppliance, x['value'][0])
                            properties['self'].append(
                                {"name": x['prefix'] + ".map.rule.reference.ids", "value": [ret_obj1['data']]})
                            del properties['self'][idx]
                    json_data['properties'] = properties
                return isamAppliance.invoke_post(
                    "Create an STS chain", uri, json_data,
                    requires_modules=requires_modules,
                    requires_version=requires_version, warnings=warnings)

    return isamAppliance.create_return_object(warnings=warnings)


def delete(isamAppliance, name, check_mode=False, force=False):
    """
    Delete a specific STS chain
    """
    ret_obj = search(isamAppliance, name, check_mode=check_mode, force=force)
    chain_id = ret_obj['data']

    if chain_id == {}:
        logger.info("STS Chain {0} not found, skipping delete.".format(name))
    else:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Delete a specific STS chain",
                "{0}/{1}".format(uri, chain_id),
                requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object()


def update(isamAppliance, name, chainName, requestType, description=None, tokenType=None, xPath=None,
           signResponses=None, signatureKey=None, validateRequests=None, validationKey=None,
           sendValidationConfirmation=None, issuer=None, appliesTo=None, properties=None, new_name=None,
           ignore_password_for_idempotency=False, check_mode=False, force=False):
    """
    Update a specific STS chain
    """
    warnings = []
    chain_id, update_required, json_data = _check(isamAppliance, name, chainName, requestType, description, tokenType,
                                                  xPath, signResponses, signatureKey, validateRequests, validationKey,
                                                  sendValidationConfirmation, issuer, appliesTo, properties, new_name,
                                                  ignore_password_for_idempotency)
    if chain_id is None:
        warnings.append("Cannot update data for unknown STS Chain (or template): {0}".format(name))
    else:
        if force is True or update_required is True:
            if check_mode is True:
                return isamAppliance.create_return_object(changed=True)
            else:
                return isamAppliance.invoke_put(
                    "Update a specific STS chain",
                    "{0}/{1}".format(uri, chain_id), json_data,
                    requires_modules=requires_modules,
                    requires_version=requires_version)

    return isamAppliance.create_return_object(warnings=warnings)


def _check(isamAppliance, name, chainName, requestType, description, tokenType, xPath, signResponses, signatureKey,
           validateRequests, validationKey, sendValidationConfirmation, issuer, appliesTo, properties, new_name,
           ignore_password_for_idempotency):
    """
    Check and return True if update needed
    """
    update_required = False
    json_data = {
        "name": name,
        "requestType": requestType
    }
    ret_obj = templates.search(isamAppliance, name=chainName)
    if ret_obj['data'] == {}:
        logger.info("Unable to find a valid STS Chain Template for {0}".format(chainName))
        return None, update_required, json_data
    else:
        json_data['chainId'] = ret_obj['data']
    ret_obj = get(isamAppliance, name)
    if ret_obj['data'] == {}:
        logger.info("STS Chain not found, returning no update required.")
        return None, update_required, json_data
    else:
        if (ignore_password_for_idempotency and ret_obj['data']['properties']):
            if (ret_obj['data']['properties']['self'] == []):
                del ret_obj['data']['properties']['self']
            else:
                for idx, x in enumerate(ret_obj['data']['properties']['self']):
                    if "password" in x['name']:
                        del ret_obj['data']['properties']['self'][idx]
            if (ret_obj['data']['properties']['partner'] == []):
                del ret_obj['data']['properties']['partner']
            else:
                for idx, x in enumerate(ret_obj['data']['properties']['partner']):
                    if "password" in x['name']:
                        del ret_obj['data']['properties']['partner'][idx]
        chain_id = ret_obj['data']['id']
        del ret_obj['data']['id']
        if new_name is not None:
            json_data['name'] = new_name
        if description is not None:
            json_data['description'] = description
        elif 'description' in ret_obj['data']:
            del ret_obj['data']['description']
        if tokenType is not None:
            json_data['tokenType'] = tokenType
        if xPath is not None:
            json_data['xPath'] = xPath
        if signResponses is not None:
            json_data['signResponses'] = signResponses
        if signatureKey is not None:
            json_data['signatureKey'] = signatureKey
        if validateRequests is not None:
            json_data['validateRequests'] = validateRequests
        if validationKey is not None:
            json_data['validationKey'] = validationKey
        if sendValidationConfirmation is not None:
            json_data['sendValidationConfirmation'] = sendValidationConfirmation
        if issuer is not None:
            json_data['issuer'] = issuer
        if appliesTo is not None:
            json_data['appliesTo'] = appliesTo
        if properties is not None:
            for idx, x in enumerate(properties['self']):
                if "map.rule.reference.names" in x['name']:
                    ret_obj1 = mapping_rules.search(isamAppliance, x['value'][0])
                    properties['self'].append(
                        {"name": x['prefix'] + ".map.rule.reference.ids", "value": [ret_obj1['data']]})
                    del properties['self'][idx]
            json_data['properties'] = properties

        if ignore_password_for_idempotency:
            temp = copy.deepcopy(
                json_data)  # deep copy neccessary: otherwise password parameter would be removed from desired config dict 'json_data'
            if ('self' in temp['properties']):
                for idx, x in enumerate(temp['properties']['self']):
                    if "password" in x['name']:
                        del temp['properties']['self'][idx]
            if ('partner' in temp['properties']):
                for idx, x in enumerate(temp['properties']['partner']):
                    if "password" in x['name']:
                        del temp['properties']['partner'][idx]
        else:
            temp = json_data
        sorted_json_data = tools.json_sort(temp)
        logger.debug("Sorted input: {0}".format(sorted_json_data))
        sorted_ret_obj = tools.json_sort(ret_obj['data'])
        logger.debug("Sorted existing data: {0}".format(sorted_ret_obj))
        if sorted_ret_obj != sorted_json_data:
            logger.info("Changes detected, update needed.")
            update_required = True

    return chain_id, update_required, json_data


def compare(isamAppliance1, isamAppliance2):
    """
    Compare Module Chains between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    for obj in ret_obj1['data']:
        del obj['id']
    for obj in ret_obj2['data']:
        del obj['id']

    return tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['id'])
