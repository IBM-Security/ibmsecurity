import logging
import ibmsecurity.utilities.tools

try:
    basestring
except NameError:
    basestring = (str, bytes)

logger = logging.getLogger(__name__)

# URI for this module
uri = "/isam/authzserver"
requires_model = "Appliance"
docker_warning = ['API invoked requires model: Appliance, appliance is of deployment model: Docker.']


def get_all(isamAppliance, id, stanza_id, check_mode=False, force=False):
    """
    Retrieving all configuration entries for a stanza - Authorization Server
    """
    try:
        return isamAppliance.invoke_get(
            description="Retrieving all configuration entries for a stanza - Authorization Server",
            uri="{0}/{1}/configuration/stanza/{2}/v1".format(uri,
                                                             id,
                                                             stanza_id), requires_model=requires_model)
    except:
        # Return empty array - exception thrown if stanza has no entries or does not exist
        ret_obj = isamAppliance.create_return_object()
        ret_obj['data'] = {}
        return ret_obj


def get(isamAppliance, id, stanza_id, entry_id, check_mode=False, force=False):
    """
    Retrieving a specific configuration entry - Authorization Server
    """
    return isamAppliance.invoke_get(description="Retrieving a specific configuration entry - Authorization Server",
                                    uri="{0}/{1}/configuration/stanza/{2}/entry_name/{3}/v1".format(uri,
                                                                                                    id, stanza_id,
                                                                                                    entry_id),
                                    requires_model=requires_model)


def add(isamAppliance, id, stanza_id, entries, check_mode=False, force=False):
    """
    Add configuration entry by stanza - Authorization Server
    """
    if _isDocker(isamAppliance, id, stanza_id):
        return isamAppliance.create_return_object(warnings=docker_warning)

    if isinstance(entries, basestring):
        import ast
        entries = ast.literal_eval(entries)

    add_required = False

    if force is False:
        add_entries = []
        for entry in entries:
            exists, update_required, value = _check(isamAppliance, id, stanza_id, entry[0], entry[1])
            if exists is True:
                logger.debug(
                    'Entries exists {0}/{1}/{2}/{3}! Will be ignored.'.format(id, stanza_id, entry[0],
                                                                              entry[1]))
            else:
                add_entries.append(entry)
                add_required = True
        entries = add_entries

    if force is True or add_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return _add(isamAppliance, id, stanza_id, entries)

    return isamAppliance.create_return_object()


def _add(isamAppliance, id, stanza_id, entries):
    return isamAppliance.invoke_post(
        description="Add configuration entry by stanza - Authorization Server",
        uri="{0}/{1}/configuration/stanza/{2}/entry_name/v1".format(uri, id, stanza_id),
        data={"entries": entries}, requires_model=requires_model)


def _isDocker(isamAppliance, id, stanza_id):
    ret_obj = get_all(isamAppliance, id, stanza_id)
    warnings = ret_obj['warnings']
    if warnings and 'Docker' in warnings[0]:
        return True
    else:
        return False


def set(isamAppliance, id, stanza_id, entries, check_mode=False, force=False):
    """
    Set a configuration entry or entries by stanza - Authorization Server

    Note: entries has to be [['key', 'value1'], ['key', 'value2]], cannot provide [['key', ['value1', 'value2']]]
    get() returns the second format - thus lots of logic to handle this discrepancy.

    Smart enough to update only that which is needed.
    """
    if _isDocker(isamAppliance, id, stanza_id):
        return isamAppliance.create_return_object(warnings=docker_warning)

    if isinstance(entries, basestring):
        import ast
        entries = ast.literal_eval(entries)

    set_update = False
    set_entries = []

    if force is False:
        for entry in _collapse_entries(entries):
            process_entry = False
            exists, update_required, cur_value = _check(isamAppliance, id, stanza_id, entry[0], entry[1])
            if exists is False:
                set_update = True
                process_entry = True
            elif update_required is True:
                set_update = True
                process_entry = True
                for val in cur_value:
                    # Force delete of existing values, new values will be added
                    delete(isamAppliance, id, stanza_id, entry[0], val, check_mode, True)
                    logger.info(
                        'Deleting entry, will be re-added: {0}/{1}/{2}/{3}'.format(id, stanza_id, entry[0],
                                                                                   val))
            if process_entry is True:
                if isinstance(entry[1], list):
                    for v in entry[1]:
                        set_entries.append([entry[0], v])
                else:
                    set_entries.append([entry[0], entry[1]])

    if force is True or set_update is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return _add(isamAppliance, id, stanza_id, set_entries)

    return isamAppliance.create_return_object()


def _collapse_entries(entries):
    """
    Convert [['key', 'value1'], ['key', 'value2]] to [['key', ['value1', 'value2']]]
    Expect key values to be consecutive. Will maintain order as provided.
    """
    if entries is None or len(entries) < 1:
        return []
    else:
        cur_key = entries[0][0]
        cur_value = []
        new_entry = []

    for entry in entries:
        if entry[0] == cur_key:
            cur_value.append(entry[1])
        else:
            new_entry.append([cur_key, cur_value])
            # reset current key
            cur_key = entry[0]
            cur_value = [entry[1]]

    new_entry.append([cur_key, cur_value])

    return new_entry


def delete(isamAppliance, id, stanza_id, entry_id, value_id='', check_mode=False, force=False):
    """
    Deleting a value from a configuration entry - Authorization Server
    """
    if _isDocker(isamAppliance, id, stanza_id):
        return isamAppliance.create_return_object(warnings=docker_warning)

    exists = False
    if force is False:
        exists, update_required, value = _check(isamAppliance, id, stanza_id, entry_id, value_id)

    if force is True or exists is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            # URL being encoded primarily to handle request-log-format that has "%" values in them
            f_uri = "{0}/{1}/configuration/stanza/{2}/entry_name/{3}/value/{4}/v1".format(uri, id,
                                                                                          stanza_id, entry_id, value_id)
            # Replace % with %25 if it is not encoded already
            import re
            ruri = re.sub("%(?![0-9a-fA-F]{2})", "%25", f_uri)
            # URL encode
            import urllib.parse
            full_uri = urllib.parse.quote(ruri)
            return isamAppliance.invoke_delete(
                description="Deleting a value from a configuration entry - Authorization Server",
                uri=full_uri, requires_model=requires_model)

    return isamAppliance.create_return_object()


def delete_all(isamAppliance, id, stanza_id, entry_id, check_mode=False, force=False):
    """
    Deleting all values from a configuration entry - Authorization Server
    """

    delete_required = False
    if force is False:
        try:
            ret_obj = get(isamAppliance, id, stanza_id, entry_id)
            warnings = ret_obj['warnings']
            if warnings and 'Docker' in warnings[0]:
                return isamAppliance.create_return_object(warnings=ret_obj['warnings'])

            if ret_obj['data'] != {}:
                delete_required = True
        except:
            pass

    if force is True or delete_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            f_uri = "{0}/{1}/configuration/stanza/{2}/entry_name/{3}/v1".format(uri, id, stanza_id, entry_id)
            return isamAppliance.invoke_delete(
                description="Deleting all values from a configuration entry - Authorization Server", uri=f_uri,
                requires_model=requires_model)

    return isamAppliance.create_return_object()


def update(isamAppliance, id, stanza_id, entry_name_id, value_id, check_mode=False, force=False):
    """
    Updating a configuration entry or entries by stanza - Authorization Server
    """
    if _isDocker(isamAppliance, id, stanza_id):
        return isamAppliance.create_return_object(warnings=docker_warning)

    if force is False:
        exists, update_required, cur_value = _check(isamAppliance, id, stanza_id, entry_name_id, value_id)

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                description="Updating a configuration entry or entries by stanza - Authorization Server",
                uri="{0}/{1}/configuration/stanza/{2}/entry_name/{3}/v1".format(uri,
                                                                                id,
                                                                                stanza_id,
                                                                                entry_name_id),
                data={
                    'value': value_id
                }, requires_model=requires_model)

    return isamAppliance.create_return_object()


def _check(isamAppliance, id, stanza_id, entry_id, value_id):
    """
    Check if entry/value exists and if exists then if update is required
    """
    try:
        ret_obj = get(isamAppliance, id, stanza_id, entry_id)
        exists = True
        update_required = False
        value = ret_obj['data'][entry_id]
    except:
        return False, True, None  # Exception means entry / stanza not found

    logger.info("Entry found in acld:{0}, stanza:{1}, entryid:{2}, value:{3}".format(id,
                                                                                     stanza_id,
                                                                                     entry_id,
                                                                                     value))
    logger.debug("Existing Value(s): {0}".format(value))
    logger.debug("Value to update  : {0}".format(value_id))

    if isinstance(value_id, list):
        if value != value_id:  # Comparing list with no sorting... sequence of values is of importance
            logger.debug("Value arrays do not match!")
            update_required = True
    else:  # assuming base string provided for value_id
        if len(value) == 1:
            if str(value_id) != str(value[0]):
                logger.debug("Single value do not match!")
                update_required = True
                exists = False  # to satisfy delete call
        else:  # base string will not match a zero length array or multiple values in it
            logger.debug("Current non-single value does not match provided single value!")
            update_required = True
            if value_id not in value:
                logger.debug("Current non-single value does not contain provided single value!")
                exists = False

    return exists, update_required, value


def compare(isamAppliance1, isamAppliance2, id, stanza_id, id2=None):
    """
    Compare stanza/entries in two appliances authorization server configuration
    """
    if id2 is None or id2 == '':
        id2 = id

    ret_obj1 = get_all(isamAppliance1, id, stanza_id)
    ret_obj2 = get_all(isamAppliance2, id2, stanza_id)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
