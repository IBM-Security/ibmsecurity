import logging
from ibmsecurity.isam.base.remote_syslog import forwarder
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

try:
    basestring
except NameError:
    basestring = (str, bytes)


def get_all(isamAppliance, server, port, protocol, check_mode=False, force=False):
    """
    Retrieve the remote syslog forwarding sources
    """
    ret_obj = forwarder.get(isamAppliance=isamAppliance, server=server, port=port, protocol=protocol,
                            check_mode=check_mode, force=force)

    try:
        ret_obj['data'] = ret_obj['data']['sources']
    except:
        ret_obj['data'] = {}

    return ret_obj


def _find_forwarder_source(ret_obj, server, port, protocol, name):
    '''
    Will return None or the forwarder object found
    index returned will be length of array if no match
    '''
    existing_forwarder, i = forwarder._find_forwarder(ret_obj, server, port, protocol)

    existing_forwarder_source, j = None, 0
    if existing_forwarder is not None:
        try:
            for src in existing_forwarder['sources']:
                if src['name'] == name:
                    existing_forwarder_source = src
                    break
                j += 1
        except:
            pass

    return existing_forwarder, i, existing_forwarder_source, j


def get(isamAppliance, server, port, protocol, name, check_mode=False, force=False):
    """
    Retrieve the remote syslog forwarding source
    """
    ret_obj = forwarder.get_all(isamAppliance=isamAppliance, check_mode=check_mode, force=force)

    if isinstance(port, basestring):
        port = int(port)

    existing_forwarder, i, existing_forwarder_source, j = _find_forwarder_source(ret_obj, server, port, protocol, name)

    return_obj = isamAppliance.create_return_object()
    return_obj['data'] = existing_forwarder_source

    return return_obj


def delete(isamAppliance, server, port, protocol, name, check_mode=False, force=False):
    """
    Delete a remote syslog forwarding source
    """
    ret_obj = forwarder.get_all(isamAppliance=isamAppliance, check_mode=check_mode, force=force)
    json_to_post = ret_obj['data']

    if isinstance(port, basestring):
        port = int(port)

    existing_forwarder, i, existing_forwarder_source, j = _find_forwarder_source(ret_obj, server, port, protocol, name)
    if existing_forwarder is not None and existing_forwarder_source is not None:
        if check_mode:
            return isamAppliance.create_return_object(changed=True)
        else:
            del json_to_post[i]['sources'][j]
            return forwarder._update_forwarder_policy(isamAppliance, json_to_post)

    return isamAppliance.create_return_object()


def set(isamAppliance, server, port, protocol, name, tag, facility, severity, check_mode=False, force=False):
    """
    Set a remote syslog forwarding source
    """
    ret_obj = forwarder.get_all(isamAppliance=isamAppliance, check_mode=check_mode, force=force)

    if isinstance(port, basestring):
        port = int(port)

    existing_forwarder, i, existing_forwarder_source, j = _find_forwarder_source(ret_obj, server, port, protocol, name)

    json_data = {
        'name': name,
        'tag': tag,
        'facility': facility,
        'severity': severity
    }

    warnings = []
    update_required = False
    if existing_forwarder is None:
        warnings.append("Unable to find forwarder for {} {} {}".format(server, port, protocol))
    else:
        if existing_forwarder_source is None:
            json_to_post = ret_obj['data']
            json_to_post[i]['sources'].append(json_data)
            update_required = True
        else:
            sorted_json_data = tools.json_sort(json_data)
            logger.debug("Sorted input: {0}".format(sorted_json_data))
            sorted_ret_obj = tools.json_sort(existing_forwarder_source)
            logger.debug("Sorted existing data: {0}".format(sorted_ret_obj))
            if sorted_ret_obj != sorted_json_data:
                logger.info("Changes detected, update needed.")
                ret_obj['data'][i]['sources'][j] = json_data
                json_to_post = ret_obj['data']
                update_required = True

    if update_required:
        if check_mode:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return forwarder._update_forwarder_policy(isamAppliance, json_to_post, warnings=warnings)

    return isamAppliance.create_return_object(warnings=warnings)
