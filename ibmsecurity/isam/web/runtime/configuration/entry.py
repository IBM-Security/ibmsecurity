import logging
import ibmsecurity.utilities.tools

try:
    basestring
except NameError:
    basestring = (str, bytes)

logger = logging.getLogger(__name__)

# URI for this module
uri = "/isam/runtime"


def get_all(isamAppliance, resource_id, stanza_id, check_mode=False, force=False):
    """
    Retrieving all configuration entries for a stanza - Runtime Environment
    """
    try:
        return isamAppliance.invoke_get("Retrieving all configuration entries for a stanza - Runtime Environment",
                                        "{0}/{1}/configuration/stanza/{2}".format(uri,
                                                                                  resource_id,
                                                                                  stanza_id))
    except:
        # Return empty array - exception thrown if stanza has no entries or does not exist
        ret_obj = isamAppliance.create_return_object()
        ret_obj['data'] = {}
        return ret_obj


def get(isamAppliance, resource_id, stanza_id, entry_id, check_mode=False, force=False):
    """
    Retrieving a specific configuration entry - Runtime Environment
    """
    return isamAppliance.invoke_get("Retrieving a specific configuration entry - Runtime Environment",
                                    "{0}/{1}/configuration/stanza/{2}/entry_name/{3}".format(uri,
                                                                                             resource_id,
                                                                                             stanza_id,
                                                                                             entry_id))


def add(isamAppliance, resource_id, stanza_id, entries, check_mode=False, force=False):
    """
    Adding a configuration entry or entries by stanza - Runtime Environment
    """
    if (isinstance(entries, basestring)):
        import ast
        entries = ast.literal_eval(entries)

    exists = False

    if force is False:
        for entry in entries:
            exists, update_required, value = _check(isamAppliance, resource_id, stanza_id, entry[0], entry[1])
            if exists is True:
                logger.info('Atleast one of the entries being added exists already {0}/{1}/{2}/{3}!'.format(resource_id,
                                                                                                            stanza_id,
                                                                                                            entry[0],
                                                                                                            entry[1]))
                break

    if force is True or exists is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return _add(isamAppliance, resource_id, stanza_id, entries)

    return isamAppliance.create_return_object()


def _add(isamAppliance, resource_id, stanza_id, entries):
    return isamAppliance.invoke_post(
        "Adding a configuration entry or entries by stanza - Runtime Environment",
        "/isam/runtime/{0}/configuration/stanza/{1}/entry_name".format(resource_id, stanza_id),
        {'entries': entries})


def set(isamAppliance, resource_id, stanza_id, entries, check_mode=False, force=False):
    """
    Set a configuration entry or entries by stanza - Runtime Environment

    Note: entries has to be [['key', 'value1'], ['key', 'value2]], cannot provide [['key', ['value1', 'value2']]]
    get() returns the second format - thus lots of logic to handle this discrepancy.

    Smart enough to update only that which is needed.
    """
    set_update = False
    set_entries = []

    if force is False:
        for entry in _collapse_entries(entries):
            process_entry = False
            exists, update_required, cur_value = _check(isamAppliance, resource_id, stanza_id, entry[0], entry[1])
            if exists is False:  # Missing entries
                set_update = True
                process_entry = True
            elif update_required is True:  # Existing entries need to be updated
                set_update = True
                process_entry = True
                for val in cur_value:
                    # Force delete of existing values, new values will be added
                    logger.info(
                        'Deleting entry, will be re-added: {0}/{1}/{2}/{3}'.format(resource_id, stanza_id, entry[0],
                                                                                   val))
                    delete(isamAppliance, resource_id, stanza_id, entry[0], val, check_mode, True)
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
            return _add(isamAppliance, resource_id, stanza_id, set_entries)

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
            cur_key = entry[0]
            cur_value = [entry[1]]
            new_entry.append([cur_key, cur_value])

    new_entry.append([cur_key, cur_value])

    return new_entry


def delete(isamAppliance, resource_id, stanza_id, entry_id, value_id='', check_mode=False, force=False):
    """
    Deleting a value from a configuration entry - Runtime Environment
    """
    if force is False:
        exists, update_required, value = _check(isamAppliance, resource_id, stanza_id, entry_id, value_id)

    if force is True or exists is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            # URL being encoded primarily to handle spaces in them
            f_uri = "{0}/{1}/configuration/stanza/{2}/entry_name/{3}/value/{4}".format(uri, resource_id, stanza_id,
                                                                                       entry_id, value_id)
            try:
                # Assume Python3 and import package
                from urllib.parse import quote
            except ImportError:
                # Now try to import Python2 package
                from urllib import quote
            full_uri = quote(f_uri)
            return isamAppliance.invoke_delete(
                "Deleting a value from a configuration entry - Runtime Environment", full_uri)

    return isamAppliance.create_return_object()


def delete_all(isamAppliance, resource_id, stanza_id, entry_id, check_mode=False, force=False):
    """
    Deleting all values from a configuration entry - Runtime Environment
    """
    delete_required = False
    if force is False:
        try:
            ret_obj = get(isamAppliance, resource_id, stanza_id, entry_id)
            if ret_obj['data'] != {}:
                delete_required = True
        except:
            pass

    if force is True or delete_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            f_uri = "{0}/{1}/configuration/stanza/{2}/entry_name/{3}".format(uri, resource_id, stanza_id, entry_id)
            return isamAppliance.invoke_delete(
                "Deleting all values from a configuration entry - Runtime Environment", f_uri)

    return isamAppliance.create_return_object()


def update(isamAppliance, resource_id, stanza_id, entry_id, value_id, check_mode=False, force=False):
    """
    Updating a configuration entry or entries by stanza - Runtime Environment
    """
    if force is False:
        exists, update_required, value = _check(isamAppliance, resource_id, stanza_id, entry_id, value_id)

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Updating a configuration entry or entries by stanza - Runtime Environment",
                "{0}/{1}/configuration/stanza/{2}/entry_name/{3}".format(uri,
                                                                         resource_id,
                                                                         stanza_id,
                                                                         entry_id),
                {
                    'value': value_id
                })

    return isamAppliance.create_return_object()


def _check(isamAppliance, resource_id, stanza_id, entry_id, value_id):
    """
    Check if entry/value exists
    """
    try:
        ret_obj = get(isamAppliance, resource_id, stanza_id, entry_id)
    except:
        return False, True, None  # Exception means entry / stanza not found

    exists = True
    update_required = False
    value = ret_obj['data'][entry_id]
    logger.info("Entry found in resource:{0}, stanza:{1}, entryid:{2}, value:{3}".format(resource_id,
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


def compare(isamAppliance1, isamAppliance2, resource_id, stanza_id):
    """
    Compare suffixes in two appliances
    """
    ret_obj1 = get_all(isamAppliance1, resource_id, stanza_id)
    ret_obj2 = get_all(isamAppliance2, resource_id, stanza_id)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
