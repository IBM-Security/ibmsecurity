import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get(isamAppliance, reverseproxy_id, check_mode=False, force=False):
    """
    Retrieving a list of stanzas - Reverse Proxy
    """
    return isamAppliance.invoke_get("Retrieving a list of stanzas - Reverse Proxy",
                                    "/wga/reverseproxy/{0}/configuration/stanza".format(reverseproxy_id))


def add(isamAppliance, reverseproxy_id, stanza_id, check_mode=False, force=False):
    """
    Adding a configuration stanza name - Reverse Proxy
    """
    if force is True or _check(isamAppliance, reverseproxy_id, stanza_id) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post(
                "Adding a configuration stanza name - Reverse Proxy",
                "/wga/reverseproxy/{0}/configuration/stanza/{1}".format(reverseproxy_id, stanza_id),
                {})

    return isamAppliance.create_return_object()


def delete(isamAppliance, reverseproxy_id, stanza_id, check_mode=False, force=False):
    """
    Deleting a stanza - Reverse Proxy
    """
    if force is True or _check(isamAppliance, reverseproxy_id, stanza_id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Deleting a stanza - Reverse Proxy",
                "/wga/reverseproxy/{0}/configuration/stanza/{1}".format(reverseproxy_id, stanza_id))

    return isamAppliance.create_return_object()


def _check(isamAppliance, reverseproxy_id, stanza_id):
    """
    Check if entry exists
    """
    ret_obj = get(isamAppliance, reverseproxy_id)

    for stanza in ret_obj['data']:
        if stanza == stanza_id:
            logger.info("Stanza found in resource: " + reverseproxy_id)
            return True

    logger.info("Stanza *not* found in resource: " + reverseproxy_id)
    return False


def compare(isamAppliance1, isamAppliance2, reverseproxy_id, reverseproxy_id2=None):
    """
    Compare stanzas within reverse proxy configuration between two appliances
    """
    if reverseproxy_id2 is None or reverseproxy_id2 == '':
        reverseproxy_id2 = reverseproxy_id

    import ibmsecurity.isam.web.reverse_proxy.configuration.entry

    # The following array contains entries that will be ignored across all stanzas
    ignore_entries = ['azn-server-name', 'pd-user-pwd', 'bind-pwd', 'network-interface', 'server-name',
                      'listen-interface']

    # Retrieve all stanzas and corresponding entries for comparison
    ret_obj1 = get(isamAppliance1, reverseproxy_id)
    entries = {}
    for stanza in ret_obj1['data']:
        entries[stanza] = {}
        stanza_entries = ibmsecurity.isam.web.reverse_proxy.configuration.entry.get_all(isamAppliance1, reverseproxy_id,
                                                                                        stanza)
        for k, v in stanza_entries['data'].items():
            if k not in ignore_entries:
                entries[stanza][str(k)] = v
    ret_obj1['data'] = entries

    ret_obj2 = get(isamAppliance2, reverseproxy_id2)
    entries = {}
    for stanza in ret_obj2['data']:
        entries[stanza] = {}
        stanza_entries = ibmsecurity.isam.web.reverse_proxy.configuration.entry.get_all(isamAppliance2, reverseproxy_id,
                                                                                        stanza)
        for k, v in stanza_entries['data'].items():
            if k not in ignore_entries:
                entries[stanza][str(k)] = v
    ret_obj2['data'] = entries

    return ibmsecurity.utilities.tools.json_compare(ret_obj1=ret_obj1, ret_obj2=ret_obj2, deleted_keys=ignore_entries)
