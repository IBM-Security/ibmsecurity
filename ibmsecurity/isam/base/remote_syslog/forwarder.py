import logging
import ibmsecurity.utilities.tools
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/isam/rsyslog_forwarder"
requires_modules = None
requires_version = "9.0.2.1"
warnings = []

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
            logger.debug(f"Found Forwarder: {obj}")
            break
        i += 1

    return existing_forwarder, i


def get(isamAppliance, server=None, port=None, protocol=None, id=None, check_mode=False, force=False):
    """
    Retrieve a specific remote syslog forwarder
    needs server/port/protocol OR id
    id takes precedence (so server/port/protocol is ignored if id is passed)
    """
    if id is None:
        ret_obj = get_all(isamAppliance, check_mode, force)

        if isinstance(port, basestring):
            port = int(port)

        return_obj = isamAppliance.create_return_object()
        return_obj['data'], i = _find_forwarder(ret_obj, server, port, protocol)
        warnings = []
        if return_obj['data'] == None:
            warnings.append(f"No entry found for server {server} port {port} and protocol {protocol}.")
            return_obj['warnings'] = warnings

        return return_obj
    else:
        ret_obj = isamAppliance.invoke_get("Retrieve the current remote syslog forwarding policy based on id", f"{uri}/{id}",
                                        ignore_error=True,
                                        requires_modules=requires_modules, requires_version='11.0.2.0')
        rc = ret_obj.get('rc', -1)
        if rc >= 400 and rc < 600:
            warnings.append(f"No entry found for server {id}.  Return code {rc}")
            return isamAppliance.create_return_object(warnings=warnings)
        return ret_obj


def delete(isamAppliance, server=None, port=None, protocol=None, id=None, check_mode=False, force=False):
    """
    Remove a specific remote syslog forwarder
    """
    if id is None:
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
    else:
        ret_obj = isamAppliance.invoke_delete(
            "Delete specific rsyslog forwarding policy",
            f"{uri}/{id}",
            ignore_error=True,
            requires_modules=requires_modules, requires_version='11.0.2.0'
        )
        # the policy may not exist
        rc = ret_obj.get('rc', -1)
        if rc == 400:
            warnings.append(f"{ret_obj.get('data', {}).get('message', 'unknown error')}")
            return isamAppliance.create_return_object(warnings=warnings)
        if rc == 500:
            warnings.append(f"Internal error occurred: {ret_obj.get('data', {}).get('message', 'unknown error')}")
            return isamAppliance.create_return_object(warnings=warnings)
        return ret_obj


def set(isamAppliance, server=None, port=None, protocol='udp', id=None, debug=False, keyfile=None, ca_certificate=None,
        client_certificate=None, permitted_peers=None, sources=[], format=None, check_mode=False, force=False):
    """
    Update or create a specific remote syslog forwarder
    """
    warnings = []
    json_data = {
        'server': server,
        'port': port,
        'protocol': protocol,
        'debug': debug,
    }
    update_required = False
    if id is None:
        ret_obj = get_all(isamAppliance, check_mode, force)

        if isinstance(port, basestring):
            port = int(port)

        existing_forwarder, i = _find_forwarder(ret_obj, server, port, protocol)
        if existing_forwarder is not None and sources == [] and existing_forwarder['sources'] != sources:
            sources = existing_forwarder['sources']
            warnings.append("No sources provided, using existing sources to set forwarder.")
        json_data['sources'] = sources
        if keyfile is not None and keyfile != '':
            json_data['keyfile'] = keyfile
        if ca_certificate is not None and ca_certificate != '':
            json_data['ca_certificate'] = ca_certificate
        if client_certificate is not None and client_certificate != '':
            json_data['client_certificate'] = client_certificate
        if permitted_peers is not None and permitted_peers != '':
            json_data['permitted_peers'] = permitted_peers

        # Check of the given server/port/protocol exist - if not then we add it
        if existing_forwarder is None or force:
            if format is not None:
                if ibmsecurity.utilities.tools.version_compare(isamAppliance.facts['version'], "10.0.2.0") < 0:
                    warnings.append(f"Appliance at version: {isamAppliance.facts['version']}, format requires 10.0.2.0")
                else:
                    json_data["format"] = format
            json_to_post = ret_obj['data']
            json_to_post.append(json_data)
            update_required = True
            warnings.append("existing_forwarder is None")
        else:
            if format is not None:
                if ibmsecurity.utilities.tools.version_compare(isamAppliance.facts['version'], "10.0.2.0") < 0:
                    warnings.append(f"Appliance at version: {isamAppliance.facts['version']}, format requires 10.0.2.0")
                else:
                    json_data["format"] = format
            elif 'format' in ret_obj['data'][i]:
                del ret_obj['data'][i]['format']
            sorted_json_data = tools.json_sort(json_data)
            logger.debug(f"Sorted input: {sorted_json_data}")
            sorted_ret_obj = tools.json_sort(existing_forwarder)
            logger.debug(f"Sorted existing data: {sorted_ret_obj}")
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
    else:
        existing_forwarder = get(isamAppliance, id=id)
        if existing_forwarder is None or not existing_forwarder['data']:
           # new ... not sure this is valid
           return set(isamAppliance, server=server, port=port, protocol=protocol, id=None, debug=debug,
               keyfile=keyfile,
               ca_certificate=ca_certificate,
               client_certificate=client_certificate,
               permitted_peers=permitted_peers, sources=sources, format=format, check_mode=check_mode, force=force)
        else:
            existing_forwarder = existing_forwarder['data']
            if existing_forwarder is not None and sources == [] and existing_forwarder['sources'] != sources:
                sources = existing_forwarder['sources']
                warnings.append("No sources provided, using existing sources to set forwarder.")
            if keyfile is not None and keyfile != '':
                json_data['keyfile'] = keyfile
            if ca_certificate is not None and ca_certificate != '':
                json_data['ca_certificate'] = ca_certificate
            if client_certificate is not None and client_certificate != '':
                json_data['client_certificate'] = client_certificate
            if permitted_peers is not None and permitted_peers != '':
                json_data['permitted_peers'] = permitted_peers
            if format is not None:
                json_data["format"] = format
            json_data["id"] = id
            json_data["sources"] = sources

            if tools.json_equals(existing_forwarder, json_data, ignore_keys_not_in_new=True, skipkeys=True, sort_keys=True):
                update_required = False
            else:
                update_required = True

            if update_required:
                if check_mode:
                    return isamAppliance.create_return_object(changed=True, warnings=warnings)
                else:
                    return isamAppliance.invoke_put(
                            "Update the current remote syslog forwarding policy", f"{uri}/{id}",
                            json_to_post, requires_modules=requires_modules,
                            requires_version='11.0.2.0', warnings=warnings)


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
