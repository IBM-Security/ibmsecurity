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


def set(isamAppliance, name, protocol, role, configuration, templateName=None, new_name=None, check_mode=False,
        force=False):
    """
    Creating or Modifying a Federation
    """
    if (search(isamAppliance, name=name))['data'] == {}:
        # Force the add - we already know federation does not exist
        logger.info("Federation {0} had no match, requesting to add new one.".format(name))
        return add(isamAppliance, name=name, protocol=protocol, role=role, configuration=configuration,
                   templateName=templateName, check_mode=check_mode, force=True)
    else:
        # Update request
        logger.info("Federation {0} exists, requesting to update.".format(name))
        return update(isamAppliance, name=name, role=role, configuration=configuration, templateName=templateName,
                      new_name=new_name, check_mode=check_mode, force=force)


def set_file(isamAppliance, name, protocol, role, filename, mapping_id, templateName=None, new_name=None,
             check_mode=False, force=False):
    """
    Creating or Modifying a Federation from a JSON file
    """
    with open(filename, 'r') as infile:
        file_lines = json.load(infile)

    # update mapping_id
    file_lines['identityMapping']['properties']['identityMappingRuleReference'] = str(mapping_id)

    return set(isamAppliance, name, protocol, role, file_lines, templateName, new_name, check_mode, force)


def add(isamAppliance, name, protocol, role, configuration, templateName=None, check_mode=False,
        force=False):
    """
    Create a new federation

    :param isamAppliance:
    :param name:
    :param protocol: SAML2_0 or OIDC
    :param role: ip | sp | op | rp
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
                "role": role,
                "configuration": configuration
            }
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


def update(isamAppliance, name, role=None, configuration=None, templateName=None, new_name=None, check_mode=False,
           force=False):
    """
    Update a specific federation
    """
    fed_id, update_required, json_data = _check(isamAppliance, name, role, configuration, templateName, new_name)
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


def _check(isamAppliance, name, role, configuration, templateName, new_name=None):
    """
    Check and return True if update needed

    :param isamAppliance:
    :param name:
    :param role:
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
            # May not exist so skip any exceptions when deleting
            try:
                del ret_obj['data']['templateName']
            except:
                pass
        if configuration is not None:
            json_data['configuration'] = configuration
            # Check to see if configuration data contains mapping rule reference id
            # So special logic to see if mapping rule has changed
            new_map_rule_id, new_map_rule = None, None
            exist_map_rule_id, exist_map_rule = None, None
            try:
                new_map_rule_id = configuration['identityMapping']['properties']['identityMappingRuleReference']
            except:
                pass  # Ignore any lookup errors because of missing key/values
            try:
                new_map_rule = configuration['identityMapping']['properties']['identityMappingRule']
            except:
                pass  # Ignore any lookup errors because of missing key/values
            try:
                exist_map_rule_id = ret_obj['data']['configuration']['identityMapping']['properties'][
                    'identityMappingRuleReference']
            except:
                pass  # Ignore any lookup errors because of missing key/values
            try:
                exist_map_rule = ret_obj['data']['configuration']['identityMapping']['properties'][
                    'identityMappingRule']
            except:
                pass  # Ignore any lookup errors because of missing key/values
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
                    logger.debug("Comapring mapping rule ids and ignoring actual rule contents.")
                    if exist_map_rule is not None:
                        del ret_obj['data']['configuration']['identityMapping']['properties']['identityMappingRule']
                    if new_map_rule is not None:
                        del json_data['configuration']['identityMapping']['properties']['identityMappingRule']
        else:
            del ret_obj['data']['configuration']
        del ret_obj['data']['id']
        del ret_obj['data']['protocol']
        import ibmsecurity.utilities.tools
        sorted_json_data = ibmsecurity.utilities.tools.json_sort(json_data)
        logger.debug("Sorted input: {0}".format(sorted_json_data))
        sorted_ret_obj = ibmsecurity.utilities.tools.json_sort(ret_obj['data'])
        logger.debug("Sorted existing data: {0}".format(sorted_ret_obj))
        if sorted_ret_obj != sorted_json_data:
            logger.info("Changes detected, update needed.")
            update_required = True
        # Potential for missing mapping rule - so add configuration back
        if configuration is not None:
            json_data['configuration'] = configuration

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
