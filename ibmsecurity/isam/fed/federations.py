import logging
import json
from ibmsecurity.utilities import tools
from io import open

logger = logging.getLogger(__name__)

# URI for this module
uri = "/iam/access/v8/federations"
requires_modules = ["federation"]
requires_version = "9.0.1.0"


def get_all(isamAppliance, count=None, start=None, filter=None, check_mode=False, force=False):
    """
    Retrieve a list of federations
    """
    return isamAppliance.invoke_get("Retrieve a list of federations",
                                    "{0}/{1}".format(uri, tools.create_query_string(count=count, start=start,
                                                                                    filter=filter)),
                                    requires_modules=requires_modules,
                                    requires_version=requires_version)


def get(isamAppliance, name, check_mode=False, force=False):
    """
    Retrieve a federation
    """
    ret_obj = search(isamAppliance, name=name, check_mode=check_mode, force=force)
    id = ret_obj['data']

    if id == {}:
        logger.info("Federation {0} had no match, skipping retrieval.".format(name))
        return isamAppliance.create_return_object()
    else:
        return _get(isamAppliance, id)


def get_templates(isamAppliance, name, check_mode=False, force=False):
    """
    Retrieve the templates for a federation
    """
    ret_obj = search(isamAppliance, name=name, check_mode=check_mode, force=force)
    id = ret_obj['data']

    if id == {}:
        logger.info("Federation {0} had no match, skipping templates retrieval.".format(name))
        return isamAppliance.create_return_object()
    else:
        return isamAppliance.invoke_get("Retrieve the templates for a federation",
                                        "{0}/{1}/templates".format(uri, id),
                                        requires_modules=requires_modules,
                                        requires_version=requires_version)


def _get(isamAppliance, id):
    """
    Internal function to get data using "id" - used to avoid extra calls

    :param isamAppliance:
    :param id:
    :return:
    """
    return isamAppliance.invoke_get("Retrieve a specific federation",
                                    "{0}/{1}".format(uri, id),
                                    requires_modules=requires_modules,
                                    requires_version=requires_version)


def set(isamAppliance, name, protocol, configuration, role=None, templateName=None, new_name=None, check_mode=False,
        force=False):
    """
    Creating or Modifying a Federation
    """
    if (search(isamAppliance, name=name))['data'] == {}:
        # Force the add - we already know federation does not exist
        isamAppliance.logger.info("Federation {0} had no match, requesting to add new one.".format(name))
        return add(isamAppliance, name=name, protocol=protocol, role=role, configuration=configuration,
                   templateName=templateName, check_mode=check_mode, force=True)
    else:
        # Update request
        isamAppliance.logger.info("Federation {0} exists, requesting to update.".format(name))
        return update(isamAppliance, name=name, protocol=protocol, role=role, configuration=configuration, templateName=templateName,
                      new_name=new_name, check_mode=check_mode, force=force)


def set_file(isamAppliance, name, protocol, filename, mapping_id, role=None, templateName=None, new_name=None,
             check_mode=False, force=False):
    """
    Creating or Modifying a Federation from a JSON file
    """
    with open(filename, 'r') as infile:
        file_lines = json.load(infile)

    # update mapping_id
    if file_lines.get('configuration', None) is not None:
        file_lines = file_lines['configuration']
    file_lines['identityMapping']['properties']['identityMappingRuleReference'] = str(mapping_id)

    return set(isamAppliance=isamAppliance, name=name, protocol=protocol, configuration=file_lines, role=role,
               templateName=templateName, new_name=new_name, check_mode=check_mode, force=force)


def add(isamAppliance, name, protocol, configuration, role=None, templateName=None, check_mode=False,
        force=False):
    """
    Create a new federation

    :param isamAppliance:
    :param name:
    :param protocol: SAML2_0 or OIDC or OIDC10 (OIDC deprecated on v10) or WSFED
    :param role: ip | sp | op | rp (not required on OIDC10)
    :param configuration: protocol specific configuration data in JSON format
    :param templateName: template id (optional)
    :param check_mode:
    :param force:
    :return:
    """
    if force is False:
        ret_obj = search(isamAppliance, name)

    if force is True or ret_obj['data'] == {}:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            json_data = {
                "name": name,
                "protocol": protocol,
                "configuration": configuration
            }
            if role is not None:
                json_data['role'] = role
            if templateName is not None:
                json_data['templateName'] = templateName
            return isamAppliance.invoke_post(
                "Create a new federation",
                uri, json_data,
                requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object()


def delete(isamAppliance, name, check_mode=False, force=False):
    """
    Delete a federation
    """
    ret_obj = search(isamAppliance, name, check_mode=check_mode, force=force)
    fed_id = ret_obj['data']

    if fed_id == {}:
        logger.info("Federation {0} not found, skipping delete.".format(name))
    else:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Delete a federation",
                "{0}/{1}".format(uri, fed_id),
                requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object()


def update(isamAppliance, name, role=None, protocol=None, configuration=None, templateName=None, new_name=None, check_mode=False,
           force=False):
    """
    Update a specific federation
    """
    fed_id, update_required, json_data = _check(isamAppliance, name, role, protocol, configuration, templateName, new_name)
    if fed_id is None:
        from ibmsecurity.appliance.ibmappliance import IBMError
        raise IBMError("999", "Cannot update data for unknown federation: {0}".format(name))

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Update a specific federation",
                "{0}/{1}".format(uri, fed_id), json_data,
                requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object()


def _check(isamAppliance, name, role, protocol, configuration, templateName=None, new_name=None):
    """
    Check and return True if update needed

    :param isamAppliance:
    :param name:
    :param role:
    :param protocol:
    :param configuration:
    :param templateName:
    :return:
    """
    update_required = False
    json_data = {}
    ret_obj = get(isamAppliance, name)
    if ret_obj['data'] == {}:
        logger.info("Federation not found, returning no update required.")
        return None, update_required, json_data
    else:
        fed_id = ret_obj['data']['id']
        if new_name is not None:
            json_data['name'] = new_name
        else:
            json_data['name'] = name
        # Only added parameters passed, remove everything else
        if role is not None:
            json_data['role'] = role
        else:
            del ret_obj['data']['role']
        if templateName is not None:
            json_data['templateName'] = templateName
        else:
            ret_obj['data'].pop('templateName')
        if configuration is not None:
            json_data['configuration'] = configuration
            # Check to see if configuration data contains mapping rule reference id
            # So special logic to see if mapping rule has changed
            # TODO: WHY ????
            new_map_rule_id, new_map_rule = None, None
            exist_map_rule_id, exist_map_rule = None, None

            new_map_rule_id = configuration['identityMapping']['properties'].get('identityMappingRuleReference', None)
            new_map_rule = configuration['identityMapping']['properties'].get('identityMappingRule', None)

            exist_map_rule_id = ret_obj['data']['configuration']['identityMapping']['properties'].get('identityMappingRuleReference', None)
            exist_map_rule = ret_obj['data']['configuration']['identityMapping']['properties'].get('identityMappingRule', None)

            logger.debug("New Mapping data: {0}/{1}".format(new_map_rule_id, new_map_rule))
            logger.debug("Existing Mapping data: {0}/{1}".format(exist_map_rule_id, exist_map_rule))
            if new_map_rule_id is not None:
                # Mapping rule id provided in update, check if we need to extract actual rules and compare
                if exist_map_rule_id is None and exist_map_rule is not None:
                    import ibmsecurity.isam.aac.mapping_rules
                    new_map_obj = ibmsecurity.isam.aac.mapping_rules._get(isamAppliance, new_map_rule_id)
                    if new_map_obj['data'] != {}:
                        if new_map_obj['data']['content'].strip() != exist_map_rule.strip():
                            logger.info("Mapping Rule is different, need to update.")
                            return fed_id, True, json_data
                # Allow mapping rule id to be compared - not actual rules contents
                elif exist_map_rule_id is not None:
                    logger.debug("Comparing mapping rule ids and ignoring actual rule contents.")
                    if exist_map_rule is not None:
                        del ret_obj['data']['configuration']['identityMapping']['properties']['identityMappingRule']
                    if new_map_rule is not None:
                        del json_data['configuration']['identityMapping']['properties']['identityMappingRule']
        else:
            json_data['configuration'] = {}
        # Potential for missing mapping rule - so add configuration back
        if configuration is not None:
            json_data['configuration'] = configuration

        ret_obj['data'].pop('id')
        if protocol is not None:
            json_data['protocol'] = protocol
        _providerUri = None
        if not json_data['configuration'].get('providerId', None):
            if protocol is not None:
                if protocol == "OIDC10":
                    _providerUri = "/oidc/rp/" + json_data['name']
                    json_data['configuration']['providerId'] = json_data['configuration']['pointOfContactUrl'] + _providerUri
                elif protocol == "SAML2_0":
                    _providerUri = "/" + json_data['name'] + "/saml20"
                    json_data['configuration']['providerId'] = json_data['configuration']['pointOfContactUrl'] + _providerUri
                elif protocol == "WSFED":
                    #  _providerUri = "/wsfed/wsf" #not correct
                    logger.debug("Ignore wsfed for this")

        if protocol == "SAML2_0" and role == 'sp':
            if not json_data['configuration'].get('manageNameIDService', None):
                json_data['configuration']['manageNameIDService'] = []
            if not json_data['configuration'].get('sessionStateHeaders', None):
                json_data['configuration']['sessionStateHeaders'] = []
            if not json_data['configuration'].get('attributeMapping', None):
                json_data['configuration']['attributeMapping'] = {"map": []}
            if not json_data['configuration'].get('wayfCookieLifetime', None):
                json_data['configuration']['wayfCookieLifetime'] = 86400
            if json_data['configuration'].get('authnReqMapping', None):
                # remove javascript
                if json_data['configuration']['authnReqMapping'].get('properties', None):
                    if json_data['configuration']['authnReqMapping']['properties'].get('ruleType', None):
                        del json_data['configuration']['authnReqMapping']['properties']['ruleType']
            else:
                # default
                if tools.version_compare(isamAppliance.facts["version"], "10.0.3") >= 0:
                    json_data['configuration']['authnReqMapping'] = {"activeDelegateId": "skip-authn-request-map"}
            if json_data['configuration'].get('extensionMapping', None):
                # remove javascript
                if json_data['configuration']['extensionMapping'].get('properties', None):
                    if json_data['configuration']['extensionMapping']['properties'].get('ruleType', None):
                        del json_data['configuration']['extensionMapping']['properties']['ruleType']
            else:
                if tools.version_compare(isamAppliance.facts["version"], "10.0.1") >= 0:
                    json_data['configuration']['extensionMapping'] = {"activeDelegateId": "skip-extension-map"}
            # artifactResolutionService bindings url
            if json_data['configuration'].get('artifactResolutionService', None):
                for i in json_data['configuration']['artifactResolutionService']:
                    if not i.get('url', None):
                        # put in a default value : point of contact + federation
                        i['url'] = f"{json_data['configuration']['providerId']}/soap"

            # assertionConsumerService binding url
            if json_data['configuration'].get('assertionConsumerService', None):
                for i in json_data['configuration']['assertionConsumerService']:
                    if not i.get('url', None):
                        # put in a default value : point of contact + federation
                        i['url'] = f"{json_data['configuration']['providerId']}/login"
            # isamAppliance.logger.debug('singlelogoutblabla')
            if json_data['configuration'].get('singleLogoutService', None):
                for i in json_data['configuration']['singleLogoutService']:
                    if not i.get('url', None):
                        # put in a default value : point of contact + federation
                        i['url'] = f"{json_data['configuration']['providerId']}/slo"
            # nameid supported
            if json_data['configuration'].get('nameIDFormat', None):
                if not json_data['configuration']['nameIDFormat'].get('supported', None):
                    if ret_obj['data']['configuration']['nameIDFormat'].get('supported', None):
                        logger.debug("Ignoring supported nameIDFormat for comparison")
                        ret_obj['data']['configuration']['nameIDFormat'].pop('supported')

        sorted_json_data = json.dumps(json_data, skipkeys=True, sort_keys=True)
        # isamAppliance.logger.debug(f"\nSorted Desired:\n\n {sorted_json_data}\n")
        logger.debug(f"\nSorted Desired:\n\n {sorted_json_data}\n")
        sorted_ret_obj = json.dumps(ret_obj['data'], skipkeys=True, sort_keys=True)
        # isamAppliance.logger.debug(f"\nSorted Current:\n\n {sorted_ret_obj}\n")
        logger.debug(f"\nSorted Desired:\n\n {sorted_json_data}\n")
        if sorted_ret_obj != sorted_json_data:
            # parameters that are necessary for compare, but not for update
            json_data.pop('protocol')
            isamAppliance.logger.info("Changes detected, update needed.")
            update_required = True

    return fed_id, update_required, json_data


def export_metadata(isamAppliance, name, filename, check_mode=False, force=False):
    """
    Export a federation
    """
    ret_obj = search(isamAppliance, name)
    fed_id = ret_obj['data']
    if fed_id == {}:
        from ibmsecurity.appliance.ibmappliance import IBMError
        raise IBMError("999", "Cannot export data from unknown federation: {0}".format(name))
    import os.path

    if force is True or (fed_id != {} and os.path.exists(filename) is False):
        if check_mode is False:  # No point downloading a file if in check_mode
            return isamAppliance.invoke_get_file(
                "Export a federation",
                "{0}/{1}/metadata".format(uri, fed_id),
                filename,
                requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object()


def search(isamAppliance, name, force=False, check_mode=False):
    """
    Search federation ID by name
    """
    ret_obj = get_all(isamAppliance)
    return_obj = isamAppliance.create_return_object()

    for obj in ret_obj['data']:
        if obj['name'] == name:
            logger.info("Found federation {0} id: {1}".format(name, obj['id']))
            return_obj['data'] = obj['id']
            return_obj['rc'] = 0

    return return_obj


def compare(isamAppliance1, isamAppliance2):
    """
    Compare Federations between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    for obj in ret_obj1['data']:
        del obj['id']
    for obj in ret_obj2['data']:
        del obj['id']

    return tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['id'])
