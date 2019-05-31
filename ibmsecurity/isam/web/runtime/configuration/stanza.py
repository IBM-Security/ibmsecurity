import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get(isamAppliance, resource_id, check_mode=False, force=False):
    """
    Retrieving a list of stanzas - Runtime Environment
    """
    return isamAppliance.invoke_get("Retrieving a list of stanzas - Runtime Environment",
                                    "/isam/runtime/{0}/configuration/stanza".format(resource_id))


def add(isamAppliance, resource_id, stanza_id, check_mode=False, force=False):
    """
    Adding a configuration stanza name - Runtime Environment
    """
    if force is True or _check(isamAppliance, resource_id, stanza_id) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post(
                "Adding a configuration stanza name - Runtime Environment",
                "/isam/runtime/{0}/configuration/stanza/{1}".format(resource_id, stanza_id),
                {})

    return isamAppliance.create_return_object()


def delete(isamAppliance, resource_id, stanza_id, check_mode=False, force=False):
    """
    Deleting a stanza - Runtime Environment
    """
    if force is True or _check(isamAppliance, resource_id, stanza_id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Deleting a stanza - Runtime Environment",
                "/isam/runtime/{0}/configuration/stanza/{1}".format(resource_id, stanza_id))

    return isamAppliance.create_return_object()


def _check(isamAppliance, resource_id, stanza_id):
    """
    Check if entry exists
    """
    ret_obj = get(isamAppliance, resource_id)

    for stanza in ret_obj['data']:
        if stanza == stanza_id:
            logger.info("Stanza found in resource: " + resource_id)
            return True

    logger.info("Stanza *not* found in resource: " + resource_id)
    return False


def compare(isamAppliance1, isamAppliance2, resource_id):
    """
    Compare stanzas within resource between two appliances
    """
    import ibmsecurity.isam.web.runtime.configuration.entry

    # The following array contains entries that will be ignored (across all configuration files/stanzas)
    ignore_entries = ['master-host', 'bind-pwd', 'listen-interface']

    # Retrieve all stanzas and corresponding entries for comparison
    ret_obj1 = get(isamAppliance1, resource_id)
    entries = {}
    for stanza in ret_obj1['data']:
        entries[stanza] = {}
        stanza_entries = ibmsecurity.isam.web.runtime.configuration.entry.get_all(isamAppliance1, resource_id, stanza)
        for k, v in stanza_entries['data'].items():
            if k not in ignore_entries:
                entries[stanza][str(k)] = v
    ret_obj1['data'] = entries

    ret_obj2 = get(isamAppliance2, resource_id)
    entries = {}
    for stanza in ret_obj2['data']:
        entries[stanza] = {}
        stanza_entries = ibmsecurity.isam.web.runtime.configuration.entry.get_all(isamAppliance2, resource_id, stanza)
        for k, v in stanza_entries['data'].items():
            if k not in ignore_entries:
                entries[stanza][str(k)] = v
    ret_obj2['data'] = entries

    return ibmsecurity.utilities.tools.json_compare(ret_obj1=ret_obj1, ret_obj2=ret_obj2, deleted_keys=[])
