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
    try:
        ret_obj = isamAppliance.invoke_get("Retrieving all configuration entries for a stanza - Reverse Proxy",
                                           "{0}/{1}/configuration/stanza/{2}".format(uri,
                                                                                     reverseproxy_id,
                                                                                     stanza_id))
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
    f_uri = "{0}/{1}/configuration/stanza/{2}/entry_name/{3}".format(uri, reverseproxy_id,
                                                                     stanza_id, entry_id)
    # Replace % with %25 if it is not encoded already
    import re
    ruri = re.sub("%(?![0-9a-fA-F]{2})", "%25", f_uri)
    # URL encode
    try:
        # Assume Python3 and import package
        from urllib.parse import quote
    except ImportError:
        # Now try to import Python2 package
        from urllib import quote

    full_uri = quote(ruri)
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

    if force is False:
        add_entries = []
        for entry in entries:
            exists, update_required, value = _check(isamAppliance, reverseproxy_id, stanza_id, entry[0], entry[1])
            if exists is True:
                logger.debug(
                    'Entries exists {0}/{1}/{2}/{3}! Will be ignored.'.format(reverseproxy_id, stanza_id, entry[0],
                                                                              entry[1]))
            else:
                add_entries.append(entry)
                add_required = True
        entries = add_entries

    if force is True or add_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return _add(isamAppliance, reverseproxy_id, stanza_id, entries)

    return isamAppliance.create_return_object()


def _add(isamAppliance, reverseproxy_id, stanza_id, entries):
    return isamAppliance.invoke_post(
        "Adding a configuration entry or entries by stanza - Reverse Proxy",
        "{0}/{1}/configuration/stanza/{2}/entry_name".format(uri, reverseproxy_id, stanza_id),
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
            delete_all(isamAppliance, reverseproxy_id, stanza_id, entry[0], check_mode, True)
        if check_mode is True:
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
        return []
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
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            # URL being encoded primarily to handle request-log-format that has "%" values in them
            f_uri = "{0}/{1}/configuration/stanza/{2}/entry_name/{3}/value/{4}".format(uri, reverseproxy_id, stanza_id,
                                                                                       entry_id, value_id)
            # Replace % with %25 if it is not encoded already
            import re
            ruri = re.sub("%(?![0-9a-fA-F]{2})", "%25", f_uri)
            # URL encode
            try:
                # Assume Python3 and import package
                from urllib.parse import quote
            except ImportError:
                # Now try to import Python2 package
                from urllib import quote

            full_uri = quote(ruri)
            # Workaround for value_id encoding in 9.0.7.1
            if ibmsecurity.utilities.tools.version_compare(isamAppliance.facts['version'], '9.0.7.1') >= 0:
                uri_parts = full_uri.split('/value/')
                uri_parts[1] = uri_parts[1].replace('/', '%2F')
                full_uri = '/value/'.join(uri_parts)
            return isamAppliance.invoke_delete(
                "Deleting a value from a configuration entry - Reverse Proxy", full_uri)

    return isamAppliance.create_return_object()


def delete_all(isamAppliance, reverseproxy_id, stanza_id, entry_id, check_mode=False, force=False):
    """
    Deleting all values from a configuration entry - Reverse Proxy
    """
    delete_required = False
    if force is False:
        try:
            ret_obj = get(isamAppliance, reverseproxy_id, stanza_id, entry_id)
            if ret_obj['data'] != {}:
                delete_required = True
        except:
            pass

    if force is True or delete_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            # URL being encoded primarily to handle request-log-format that has "%" values in them
            f_uri = "{0}/{1}/configuration/stanza/{2}/entry_name/{3}".format(uri, reverseproxy_id, stanza_id, entry_id)

            # Replace % with %25 if it is not encoded already
            import re
            ruri = re.sub("%(?![0-9a-fA-F]{2})", "%25", f_uri)
            # URL encode
            try:
                # Assume Python3 and import package
                from urllib.parse import quote
            except ImportError:
                # Now try to import Python2 package
                from urllib import quote

            full_uri = quote(ruri)

            return isamAppliance.invoke_delete(
                "Deleting all values from a configuration entry - Reverse Proxy", full_uri)

    return isamAppliance.create_return_object()


def update(isamAppliance, reverseproxy_id, stanza_id, entry_id, value_id, check_mode=False, force=False):
    """
    Updating a configuration entry or entries by stanza - Reverse Proxy
    """
    if force is False:
        exists, update_required, cur_value = _check(isamAppliance, reverseproxy_id, stanza_id, entry_id, value_id)

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            # URL being encoded primarily to handle request-log-format that has "%" values in them
            f_uri = "{0}/{1}/configuration/stanza/{2}/entry_name/{3}".format(uri, reverseproxy_id,
                                                                             stanza_id, entry_id)
            # Replace % with %25 if it is not encoded already
            import re
            ruri = re.sub("%(?![0-9a-fA-F]{2})", "%25", f_uri)
            # URL encode
            try:
                # Assume Python3 and import package
                from urllib.parse import quote
            except ImportError:
                # Now try to import Python2 package
                from urllib import quote

            full_uri = quote(ruri)
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

    logger.info("Entry found in rp:{0}, stanza:{1}, entryid:{2}, value:{3}".format(reverseproxy_id,
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


def compare(isamAppliance1, isamAppliance2, reverseproxy_id, stanza_id, reverseproxy_id2=None):
    """
    Compare stanza/entries in two appliances reverse proxy configuration
    """
    if reverseproxy_id2 is None or reverseproxy_id2 == '':
        reverseproxy_id2 = reverseproxy_id

    ret_obj1 = get_all(isamAppliance1, reverseproxy_id, stanza_id)
    ret_obj2 = get_all(isamAppliance2, reverseproxy_id2, stanza_id)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
