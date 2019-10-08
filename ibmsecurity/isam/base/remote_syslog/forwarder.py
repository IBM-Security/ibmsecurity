import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/isam/rsyslog_forwarder"
requires_modules = None
requires_version = "9.0.2.1"

try:
    basestring
except NameError:
    basestring = (str, bytes)


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieve the current remote syslog forwarding policy
    """
    return isamAppliance.invoke_get("Retrieve the current remote syslog forwarding policy", uri,
                                    requires_modules=requires_modules, requires_version=requires_version)


def _find_forwarder(ret_obj, server, port, protocol):
    '''
    Will return None or the forwarder object found
    index returned will be length of array if no match
    '''
    existing_forwarder = None
    i = 0
    for obj in ret_obj['data']:
        if obj['server'] == server and obj['port'] == port and obj['protocol'] == protocol:
            existing_forwarder = obj
            logger.debug("Found Forwarder: {0}".format(obj))
            break
        i += 1

    return existing_forwarder, i


def get(isamAppliance, server, port, protocol, check_mode=False, force=False):
    """
    Retrieve a specific remote syslog forwarder
    """
    ret_obj = get_all(isamAppliance, check_mode, force)

    if isinstance(port, basestring):
        port = int(port)

    return_obj = isamAppliance.create_return_object()
    return_obj['data'], i = _find_forwarder(ret_obj, server, port, protocol)
    warnings = []
    if return_obj['data'] == None:
        warnings.append("No entry found for server {} port {} and protocol {}.".format(server, port, protocol))
        return_obj['warnings'] = warnings

    return return_obj


def delete(isamAppliance, server, port, protocol, check_mode=False, force=False):
    """
    Remove a specific remote syslog forwarder
    """
    ret_obj = get_all(isamAppliance, check_mode, force)

    if isinstance(port, basestring):
        port = int(port)

    existing_forwarder, i = _find_forwarder(ret_obj, server, port, protocol)

    json_to_post = ret_obj['data']
    if existing_forwarder is not None:
        if check_mode:
            return isamAppliance.create_return_object(changed=True)
        else:
            del json_to_post[i]
            return _update_forwarder_policy(isamAppliance, json_to_post)

    return isamAppliance.create_return_object()


def set(isamAppliance, server, port, protocol='udp', debug=False, keyfile=None, ca_certificate=None,
        client_certificate=None, permitted_peers=None, sources=[], check_mode=False, force=False):
    ret_obj = get_all(isamAppliance, check_mode, force)

    if isinstance(port, basestring):
        port = int(port)

    warnings = []
    existing_forwarder, i = _find_forwarder(ret_obj, server, port, protocol)
    if existing_forwarder is not None and sources == [] and existing_forwarder['sources'] != sources:
        sources = existing_forwarder['sources']
        warnings.append("No sources provided, using existing sources to set forwarder   .")

    json_data = {
        'server': server,
        'port': port,
        'protocol': protocol,
        'debug': debug,
        'sources': sources
    }
    if keyfile is not None and keyfile != '':
        json_data['keyfile'] = keyfile
    if ca_certificate is not None and ca_certificate != '':
        json_data['ca_certificate'] = ca_certificate
    if client_certificate is not None and client_certificate != '':
        json_data['client_certificate'] = client_certificate
    if permitted_peers is not None and permitted_peers != '':
        json_data['permitted_peers'] = permitted_peers
    update_required = False
    # Check of the given server/port/protocol exist - if not then we add it
    if existing_forwarder is None or force is True:
        json_to_post = ret_obj['data']
        json_to_post.append(json_data)
        update_required = True
    else:
        sorted_json_data = tools.json_sort(json_data)
        logger.debug("Sorted input: {0}".format(sorted_json_data))
        sorted_ret_obj = tools.json_sort(existing_forwarder)
        logger.debug("Sorted existing data: {0}".format(sorted_ret_obj))
        if sorted_ret_obj != sorted_json_data:
            logger.info("Changes detected, update needed.")
            ret_obj['data'][i] = json_data
            json_to_post = ret_obj['data']
            update_required = True

    if update_required:
        if check_mode:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return _update_forwarder_policy(isamAppliance, json_to_post, warnings=warnings)

    return isamAppliance.create_return_object(warnings=warnings)


def _update_forwarder_policy(isamAppliance, json_to_post, warnings=[]):
    return isamAppliance.invoke_put(
        "Update the current remote syslog forwarding policy", uri,
        json_to_post, requires_modules=requires_modules,
        requires_version=requires_version, warnings=warnings)


def compare(isamAppliance1, isamAppliance2):
    """
    Compare forwarder Policies between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    return tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
