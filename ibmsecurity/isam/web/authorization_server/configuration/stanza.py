import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)
uri = "/isam/authzserver"
requires_model = "Appliance"


def get(isamAppliance, id, check_mode=False, force=False):
    """
    Retrieving a list of stanzas - Authorization Server
    """
    return isamAppliance.invoke_get(description="Retrieving a list of stanzas - Authorization Server",
                                    uri="{0}/{1}/configuration/stanza/v1".format(uri, id),
                                    requires_model=requires_model)


def add(isamAppliance, id, stanza_id, check_mode=False, force=False):
    """
    Add Stanza name - Authorization Server
    """
    stanza_exists, warnings = _check(isamAppliance, id, stanza_id)

    if not warnings:
        if force is True or stanza_exists is False:
            if check_mode is True:
                return isamAppliance.create_return_object(changed=True, warnings=warnings)
            else:
                return isamAppliance.invoke_post(
                    description="Add stanza name - Authorization Server",
                    uri="{0}/{1}/configuration/stanza/{2}/v1".format(uri, id, stanza_id),
                    data={}, requires_model=requires_model)

    return isamAppliance.create_return_object(warnings=warnings)


def delete(isamAppliance, id, stanza_id, check_mode=False, force=False):
    """
    Delete Authorization Server configuration stanza
    """
    stanza_exists, warnings = _check(isamAppliance, id, stanza_id)

    if not warnings:
        if force is True or stanza_exists is True:
            if check_mode is True:
                return isamAppliance.create_return_object(changed=True, warnings=warnings)
            else:
                return isamAppliance.invoke_delete(
                    description="Delete Authorization Server configuration stanza",
                    uri="{0}/{1}/configuration/stanza/{2}/v1".format(uri, id, stanza_id),
                    requires_model=requires_model)

    return isamAppliance.create_return_object(warnings=warnings)


def _check(isamAppliance, id, stanza_id):
    """
    Check if stanza exists
    """
    ret_obj = get(isamAppliance, id)
    stanza_exists, warnings = False, ret_obj['warnings']

    if not warnings:
        for stanza in ret_obj['data']:
            if stanza == stanza_id:
                logger.info("Stanza found in resource: " + id)
                stanza_exists = True
        logger.info("Stanza *not* found in resource: " + id)
    return stanza_exists, warnings


def compare(isamAppliance1, isamAppliance2, id, id2=None):
    """
    Compare stanzas within authorization server configuration between two appliances
    """
    if id2 is None or id2 == '':
        id2 = id

    import ibmsecurity.isam.web.authorization_server.configuration.entry

    # The following array contains entries that will be ignored across all stanzas
    ignore_entries = ['azn-app-host', 'azn-server-name', 'pd-user-pwd', 'bind-pwd', 'network-interface', 'server-name',
                      'listen-interface']

    # Retrieve all stanzas and corresponding entries for comparison
    ret_obj1 = get(isamAppliance1, id)
    warnings = ret_obj1['warnings']
    if warnings and 'Docker' in warnings[0]:
        return isamAppliance.create_return_object(warnings=ret_obj1['warnings'])

    entries = {}
    for stanza in ret_obj1['data']:
        entries[stanza] = {}
        stanza_entries = ibmsecurity.isam.web.authorization_server.configuration.entry.get_all(isamAppliance1, id,
                                                                                               stanza)
        for k, v in stanza_entries['data'].items():
            if k not in ignore_entries:
                entries[stanza][str(k)] = v
    ret_obj1['data'] = entries

    ret_obj2 = get(isamAppliance2, id2)
    entries = {}
    for stanza in ret_obj2['data']:
        entries[stanza] = {}
        stanza_entries = ibmsecurity.isam.web.authorization_server.configuration.entry.get_all(isamAppliance2, id,
                                                                                               stanza)
        for k, v in stanza_entries['data'].items():
            if k not in ignore_entries:
                entries[stanza][str(k)] = v
    ret_obj2['data'] = entries

    return ibmsecurity.utilities.tools.json_compare(ret_obj1=ret_obj1, ret_obj2=ret_obj2, deleted_keys=ignore_entries)
