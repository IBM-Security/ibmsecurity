import logging
import ibmsecurity.isam.fed.federations
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/iam/access/v8/federations"
requires_modules = ["federation"]
requires_version = "9.0.1.0"


def get_all(isamAppliance, federation_name, count=None, start=None, check_mode=False, force=False):
    """
    Retrieve a list of partners
    """
    ret_obj = ibmsecurity.isam.fed.federations.search(isamAppliance, name=federation_name, check_mode=check_mode,
                                                      force=force)
    fed_id = ret_obj['data']

    if fed_id == {}:
        logger.info("Federation {0}, not found. Skipping get.".format(federation_name))
        return isamAppliance.create_return_object()
    else:
        return _get_all(isamAppliance, fed_id, tools.create_query_string(count=count, start=start))


def _get_all(isamAppliance, fed_id, query_str=''):
    return isamAppliance.invoke_get("Retrieve a list of partners",
                                    "{0}/{1}/partners{2}".format(uri, fed_id, query_str),
                                    requires_modules=requires_modules,
                                    requires_version=requires_version)


def get(isamAppliance, federation_name, partner_name, check_mode=False, force=False):
    """
    Retrieve a partner
    """
    ret_obj = search(isamAppliance, federation_name, partner_name, check_mode=check_mode, force=force)
    fed_id, partner_id = ret_obj['data']

    if fed_id == {} or partner_id is None:
        logger.info(
            "Federation/Partner {0}/{1} had no match, skipping retrieval.".format(federation_name, partner_name))
        return isamAppliance.create_return_object()
    else:
        return _get(isamAppliance, fed_id, partner_id)


def _get(isamAppliance, federation_id, partner_id):
    """
    Internal function to get data using "id" - used to avoid extra calls
    """
    return isamAppliance.invoke_get("Retrieve a partner",
                                    "{0}/{1}/partners/{2}".format(uri, federation_id, partner_id),
                                    requires_modules=requires_modules,
                                    requires_version=requires_version)


def search(isamAppliance, federation_name, partner_name, force=False, check_mode=False):
    """
    Search Federation and Partner ID by name
    """
    ret_obj = ibmsecurity.isam.fed.federations.search(isamAppliance, name=federation_name, check_mode=check_mode,
                                                      force=force)
    fed_id = ret_obj['data']
    partner_id = None
    return_obj = isamAppliance.create_return_object()

    if fed_id != {}:
        logger.info("Federation {0} found!".format(federation_name))
        ret_obj = _get_all(isamAppliance, fed_id)
        for obj in ret_obj['data']:
            if obj['name'] == partner_name:
                logger.info(
                    "Found Federation/Partner {0}/{1} - id: {2}".format(federation_name, partner_name, obj['id']))
                partner_id = obj['id']
    else:
        logger.info('Federation {0} not found!'.format(federation_name))

    return_obj['data'] = fed_id, partner_id

    return return_obj


def import_metadata(isamAppliance, federation_name, partner_name, filename, check_mode=False, force=False):
    """
    Import a new partner
    """
    ret_obj = search(isamAppliance, federation_name, partner_name, check_mode, force)
    fed_id, partner_id = ret_obj['data']

    if fed_id == {}:
        from ibmsecurity.appliance.ibmappliance import IBMError
        raise IBMError("999", "Cannot import data into unknown federation: {0}".format(federation_name))
    else:
        if partner_id is not None:
            logger.info("Federation / Partner {0}/{1} already exists.".format(federation_name, partner_name))
        if force is True or partner_id is None:
            if check_mode is True:
                return isamAppliance.create_return_object(changed=True)
            else:
                json_data = {}
                # Override partner name in metadata file - if provided
                if partner_name is not None:
                    json_data['name'] = partner_name
                return isamAppliance.invoke_post_files(
                    "Import a new partner",
                    "{0}/{1}/partners/metadata".format(uri, fed_id),
                    [
                        {
                            'file_formfield': 'metadata',
                            'filename': filename,
                            'mimetype': 'application/octet-stream'
                        }
                    ], json_data,
                    requires_modules=requires_modules,
                    requires_version=requires_version)

    return isamAppliance.create_return_object()


def set(isamAppliance, federation_name, partner_name, enabled, role, configuration, templateName=None, new_name=None,
        check_mode=False, force=False):
    """
    Creating or Modifying a Partner
    """
    ret_obj = search(isamAppliance, federation_name, partner_name)
    fed_id, partner_id = ret_obj['data']

    if fed_id == {}:
        logger.info("Federation {0} not found, skipping add/update.".format(federation_name))
    else:
        if partner_id is None:
            # Force the add - we already know partner does not exist
            return add(isamAppliance, federation_name, partner_name, enabled, role, configuration, templateName,
                       check_mode, True)
        else:
            # Update request
            return update(isamAppliance, federation_name, partner_name, enabled, configuration, role, templateName,
                          new_name, check_mode, force)


def add(isamAppliance, federation_name, partner_name, enabled, role, configuration, templateName=None, check_mode=False,
        force=False):
    """
    Create a new partner
    """
    ret_obj = search(isamAppliance, federation_name, partner_name, check_mode, force)
    fed_id, partner_id = ret_obj['data']
    if fed_id == {}:
        from ibmsecurity.appliance.ibmappliance import IBMError
        raise IBMError("999", "Cannot add partner into unknown federation: {0}".format(federation_name))
    else:
        if partner_id is not None:
            logger.info("Federation / Partner {0}/{1} already exists.".format(federation_name, partner_name))

        if force is True or partner_id is None:
            if check_mode is True:
                return isamAppliance.create_return_object(changed=True)
            else:
                json_data = {
                    "name": partner_name,
                    "enabled": enabled,
                    "role": role,
                    "configuration": configuration
                }
                if templateName is not None:
                    json_data['templateName'] = templateName
                return isamAppliance.invoke_post(
                    "Create a new partner",
                    "{0}/{1}/partners".format(uri, fed_id), json_data,
                    requires_modules=requires_modules,
                    requires_version=requires_version)

    return isamAppliance.create_return_object()


def delete(isamAppliance, federation_name, partner_name, check_mode=False, force=False):
    """
    Delete a partner
    """
    ret_obj = search(isamAppliance, federation_name, partner_name, check_mode=check_mode, force=force)
    fed_id, partner_id = ret_obj['data']
    if fed_id == {}:
        from ibmsecurity.appliance.ibmappliance import IBMError
        raise IBMError("999", "Cannot add partner into unknown federation: {0}".format(federation_name))
    else:
        if partner_id is None:
            logger.info("In federation: {0}, Partner {1} no longer exists.".format(federation_name, partner_name))
        else:
            if check_mode is True:
                return isamAppliance.create_return_object(changed=True)
            else:
                return isamAppliance.invoke_delete(
                    "Delete a partner",
                    "{0}/{1}/partners/{2}".format(uri, fed_id, partner_id),
                    requires_modules=requires_modules,
                    requires_version=requires_version)

    return isamAppliance.create_return_object()


def update(isamAppliance, federation_name, partner_name, enabled, configuration, role=None, templateName=None,
           new_name=None, check_mode=False, force=False):
    """
    Update a specific partner
    """
    fed_id, partner_id, update_required, json_data = _check(isamAppliance, federation_name, partner_name, enabled,
                                                            configuration, role, templateName, new_name)
    if fed_id is None:
        from ibmsecurity.appliance.ibmappliance import IBMError
        raise IBMError("999", "Cannot update partner in unknown federation: {0}".format(federation_name))

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Update a specific partner",
                "{0}/{1}/partners/{2}".format(uri, fed_id, partner_id), json_data,
                requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object()


def _check(isamAppliance, federation_name, partner_name, enabled, configuration, role, templateName, new_name):
    """
    Check and return True if update needed
    """
    update_required = False
    json_data = {
        "enabled": enabled,
        "configuration": configuration
    }
    ret_obj = search(isamAppliance, federation_name, partner_name)
    fed_id, partner_id = ret_obj['data']
    if fed_id == {} or partner_id is None:
        logger.info("Federation/Partner not found, returning no update required.")
        return None, None, update_required, json_data
    else:
        ret_obj = get(isamAppliance, federation_name, partner_name)
        if ret_obj['data'] == {}:
            from ibmsecurity.appliance.ibmappliance import IBMError
            raise IBMError("999", "Search() found partner, but get() failed. Something seriously wrong!")
        else:
            if new_name is not None:
                json_data['name'] = new_name
            else:
                json_data['name'] = partner_name
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
            del ret_obj['data']['id']
            import ibmsecurity.utilities.tools
            sorted_json_data = ibmsecurity.utilities.tools.json_sort(json_data)
            logger.debug("Sorted input: {0}".format(sorted_json_data))
            sorted_ret_obj = ibmsecurity.utilities.tools.json_sort(ret_obj['data'])
            logger.debug("Sorted existing data: {0}".format(sorted_ret_obj))
            if sorted_ret_obj != sorted_json_data:
                logger.info("Changes detected, update needed.")
                update_required = True
            json_data['configuration'] = configuration

    return fed_id, partner_id, update_required, json_data
