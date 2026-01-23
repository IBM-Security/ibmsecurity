from urllib.parse import quote_plus
from urllib.parse import unquote_plus

import logging
import ibmsecurity.utilities.tools
from ibmsecurity.utilities.tools import jsonSortedListEncoder
import json

try:
    basestring
except NameError:
    basestring = (str, bytes)

logger = logging.getLogger(__name__)

# URI for this module
uri = "/wga/reverseproxy"


def get_all(isamAppliance, reverseproxy_id, stanza_id, check_mode=False, force=False):
    """
    Retrieving all configuration entries for a stanza - Reverse Proxy
    """
    stanza_id = quote_plus(stanza_id)
    try:
        ret_obj = isamAppliance.invoke_get("Retrieving all configuration entries for a stanza - Reverse Proxy",
                                           f"{uri}/{reverseproxy_id}/configuration/stanza/{stanza_id}")
        logger.debug(f"Get All {stanza_id}:\n {ret_obj}")
    except:
        # Return empty array - exception thrown if stanza has no entries or does not exist
        ret_obj = isamAppliance.create_return_object()
        ret_obj['data'] = {}

    return ret_obj


def get(isamAppliance, reverseproxy_id, stanza_id, entry_id, check_mode=False, force=False):
    """
    Retrieving a specific configuration entry - Reverse Proxy
    """
    # URL being encoded primarily to handle request-log-format that has "%" values in them
    stanza_id = quote_plus(stanza_id)
    entry_id = quote_plus(entry_id)
    full_uri = f"{uri}/{reverseproxy_id}/configuration/stanza/{stanza_id}/entry_name/{entry_id}"

    return isamAppliance.invoke_get("Retrieving a specific configuration entry - Reverse Proxy",
                                    full_uri)


def add(isamAppliance, reverseproxy_id, stanza_id, entries, check_mode=False, force=False):
    """
    Adding a configuration entry or entries by stanza - Reverse Proxy
    """
    if isinstance(entries, basestring):
        import ast
        entries = ast.literal_eval(entries)

    add_required = False

    if not force:
        add_entries = []
        for entry in entries:
            exists, update_required, value = _check(isamAppliance, reverseproxy_id, stanza_id, entry[0], entry[1])
            if exists:
                logger.debug(
                    f'Entries exists {reverseproxy_id}/{stanza_id}/{entry[0]}/{entry[1]}! Will be ignored.')
            else:
                add_entries.append(entry)
                add_required = True
        entries = add_entries

    if force or add_required:
        if check_mode:
            return isamAppliance.create_return_object(changed=True)
        else:
            return _add(isamAppliance, reverseproxy_id, stanza_id, entries)

    return isamAppliance.create_return_object()


def _add(isamAppliance, reverseproxy_id, stanza_id, entries):
    stanza_id = quote_plus(stanza_id)
    return isamAppliance.invoke_post(
        "Adding a configuration entry or entries by stanza - Reverse Proxy",
        f"{uri}/{reverseproxy_id}/configuration/stanza/{stanza_id}/entry_name",
        {"entries": entries})


def set(isamAppliance, reverseproxy_id, stanza_id, entries, check_mode=False, force=False):
    """
    Set a configuration entry or entries by stanza - Reverse Proxy

    Note: entries has to be [['key', 'value1'], ['key', 'value2]], cannot provide [['key', ['value1', 'value2']]]
    get() returns the second format - thus lots of logic to handle this discrepancy.

    This version will update all entries in the stanza if a single one changes.  But it should be a lot faster and
    idempotent.

    """
    if isinstance(entries, basestring):
        import ast
        entries = ast.literal_eval(entries)
    # get all entries for the stanza
    currentEntries = get_all(isamAppliance, reverseproxy_id, stanza_id)
    currentEntries = currentEntries['data']
    # make currentEntries into a similar list of dicts
    newEntries = _collapse_entries_obj(entries)
    # Filter the current entries to only include the requested entry (keys)
    fCurrentEntries = {k: v for k, v in currentEntries.items() if k in newEntries.keys()}
    # compare using json_sort
    newEntriesJSON = json.dumps(newEntries, skipkeys=True, sort_keys=True, cls=jsonSortedListEncoder)
    logger.debug(f"\nSorted Desired  Stanza {stanza_id}:\n\n {newEntriesJSON}\n")
    currentEntriesJSON = json.dumps(fCurrentEntries, skipkeys=True, sort_keys=True, cls=jsonSortedListEncoder)
    logger.debug(f"\nSorted Existing Stanza {stanza_id}:\n\n {currentEntriesJSON}\n")

    if force or (newEntriesJSON != currentEntriesJSON):
        for entry in entries:
            logger.info(f"Deleting entry, will be re-added: {reverseproxy_id}/{stanza_id}/{entry[0]}")
            if not check_mode:
               delete_all(isamAppliance, reverseproxy_id, stanza_id, entry[0], check_mode, True)
        if check_mode:
            return isamAppliance.create_return_object(changed=True)
        else:
            return _add(isamAppliance, reverseproxy_id, stanza_id, entries)

    return isamAppliance.create_return_object()


def _collapse_entries_obj(entries):
    """
   Convert [['key', 'value1'], ['key', 'value2]] to {'key': ['value1', 'value2'], ...}
   the value is an array if multiple values, but a string if it's a single value

   Also converts all values to str for easy compare
   """
    if entries is None or len(entries) < 1:
        return {}
    else:
        prev_key = ""
        new_entry = {}

    for entry in entries:
        if entry[0] == prev_key:
            if isinstance(new_entry.get(entry[0], ""), list):
                existing_value = new_entry.get(entry[0], [])
            else:
                existing_value = [new_entry.get(entry[0], "")]
            if isinstance(entry[1], list):
                new_entry[entry[0]] = existing_value + str(entry[1])
            else:
                new_entry[entry[0]] = existing_value + [str(entry[1])]
        else:
            new_entry[entry[0]] = str(entry[1])
        prev_key = entry[0]
    return new_entry


def delete(isamAppliance, reverseproxy_id, stanza_id, entry_id, value_id='', check_mode=False, force=False):
    """
    Deleting a value from a configuration entry - Reverse Proxy
    """

    if value_id == '' or value_id is None:
        return delete_all(isamAppliance=isamAppliance, reverseproxy_id=reverseproxy_id, stanza_id=stanza_id,
                          entry_id=entry_id, check_mode=check_mode, force=force)

    if not force:
        exists, update_required, value = _check(isamAppliance, reverseproxy_id, stanza_id, entry_id, value_id)

    if force or exists:
        if check_mode:
            return isamAppliance.create_return_object(changed=True)
        else:
            # URL being encoded primarily to handle request-log-format that has "%" values in them
            stanza_id = quote_plus(stanza_id)
            entry_id = quote_plus(entry_id)
            value_id = quote_plus(value_id)
            full_uri = f"{uri}/{reverseproxy_id}/configuration/stanza/{stanza_id}/entry_name/{entry_id}/value/{value_id}"

            # Workaround for value_id encoding in 9.0.7.1
            #if ibmsecurity.utilities.tools.version_compare(isamAppliance.facts['version'], '9.0.7.1') >= 0:
            #    uri_parts = full_uri.split('/value/')
            #    uri_parts[1] = uri_parts[1].replace('/', '%2F')
            #    full_uri = '/value/'.join(uri_parts)
            return isamAppliance.invoke_delete(
                "Deleting a value from a configuration entry - Reverse Proxy", full_uri)

    return isamAppliance.create_return_object()


def delete_all(isamAppliance, reverseproxy_id, stanza_id, entry_id, check_mode=False, force=False):
    """
    Deleting all values from a configuration entry - Reverse Proxy
    """
    delete_required = False
    if not force:
        try:
            ret_obj = get(isamAppliance, reverseproxy_id, stanza_id, entry_id)
            if ret_obj['data'] != {}:
                delete_required = True
        except Exception:
            pass

    if force or delete_required:
        if check_mode:
            return isamAppliance.create_return_object(changed=True)
        else:
            # URL being encoded primarily to handle request-log-format that has "%" values in them
            stanza_id = quote_plus(stanza_id)
            entry_id = quote_plus(entry_id)
            full_uri = f"{uri}/{reverseproxy_id}/configuration/stanza/{stanza_id}/entry_name/{entry_id}"
            return isamAppliance.invoke_delete(
                "Deleting all values from a configuration entry - Reverse Proxy", full_uri)

    return isamAppliance.create_return_object()


def update(isamAppliance, reverseproxy_id, stanza_id, entry_id, value_id, check_mode=False, force=False):
    """
    Updating a configuration entry or entries by stanza - Reverse Proxy
    """
    if not force:
        exists, update_required, cur_value = _check(isamAppliance, reverseproxy_id, stanza_id, entry_id, value_id)

    if force or update_required:
        if check_mode:
            return isamAppliance.create_return_object(changed=True)
        else:
            # URL being encoded primarily to handle request-log-format that has "%" values in them
            # make sure stanza_id and entry_id are url safe
            stanza_id = quote_plus(stanza_id)
            entry_id = quote_plus(entry_id)
            full_uri = f"{uri}/{reverseproxy_id}/configuration/stanza/{stanza_id}/entry_name/{entry_id}"

            return isamAppliance.invoke_put(
                "Updating a configuration entry or entries by stanza - Reverse Proxy",
                full_uri,
                {
                    'value': value_id
                })

    return isamAppliance.create_return_object()


def _check(isamAppliance, reverseproxy_id, stanza_id, entry_id, value_id):
    """
    Check if entry/value exists and if exists then if update is required
    """
    try:
        ret_obj = get(isamAppliance, reverseproxy_id, stanza_id, entry_id)
        exists = True
        update_required = False
        value = ret_obj['data'][entry_id]
    except:
        return False, True, None  # Exception means entry / stanza not found

    logger.info(f"Entry found in rp:{reverseproxy_id}, stanza:{stanza_id}, entryid:{entry_id}, value:{value}")
    logger.debug(f"Existing Value(s): {value}")
    logger.debug(f"Value to update  : {value_id}")

    if isinstance(value_id, list):
        if value != value_id:  # Comparing list with no sorting... sequence of values is of importance
            logger.debug("Value arrays do not match!")
            update_required = True
    else:  # assuming base string provided for value_id
        if len(value) == 1:
            if str(value_id) != str(value[0]):
                logger.debug("Single value does not match!")
                update_required = True
                exists = False  # to satisfy delete call
        else:  # base string will not match a zero length array or multiple values in it
            logger.debug("Current non-single value does not match provided single value!")
            update_required = True
            if value_id not in value:
                logger.debug("Current non-single value does not contain provided single value!")
                exists = False

    return exists, update_required, value


def compare(isamAppliance1, isamAppliance2, reverseproxy_id, stanza_id, reverseproxy_id2=None):
    """
    Compare stanza/entries in two appliances reverse proxy configuration
    """
    if reverseproxy_id2 is None or reverseproxy_id2 == '':
        reverseproxy_id2 = reverseproxy_id

    ret_obj1 = get_all(isamAppliance1, reverseproxy_id, stanza_id)
    ret_obj2 = get_all(isamAppliance2, reverseproxy_id2, stanza_id)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
