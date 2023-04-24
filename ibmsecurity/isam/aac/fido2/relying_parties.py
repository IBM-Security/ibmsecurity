import logging
import json
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/iam/access/v8/fido2/relying-parties"
requires_modules = ["mga"]
requires_version = "9.0.7.0"

def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieve a list of all FIDO2 Relying Part
    """
    return isamAppliance.invoke_get("Retrieving the list of all FIDO2 Relying Parties", uri,
                                    requires_modules=requires_modules, requires_version=requires_version)

def get(isamAppliance, name, id=None, check_mode=False, force=False):
    """
    Retrieve a specific FIDO2 Relying Party

    Ignore the id if appliance is less than version 10.0.1
    """
    if id is None or tools.version_compare(isamAppliance.facts['version'], '10.0.1') < 0:
        ret_obj = search(isamAppliance, name=name, check_mode=check_mode, force=force)
        id = ret_obj['data']

    if id == {}:
        logger.info("FIDO2 Metadata {0} had no match, skipping retrieval.".format(name))
        return isamAppliance.create_return_object()
    else:
        return _get(isamAppliance, id)

def search(isamAppliance, name, force=False, check_mode=False):
    """
    Search FIDO2 Relying Party id by name
    """
    ret_obj = get_all(isamAppliance)
    return_obj = isamAppliance.create_return_object()

    for obj in ret_obj['data']:
        if obj['name'] == name:
            logger.info("Found FIDO2 relying party {0} id: {1}".format(name, obj['id']))
            return_obj['data'] = obj['id']
            return_obj['rc'] = 0

    return return_obj

def delete(isamAppliance, name, check_mode=False, force=False):
    """
    Delete a FIDO2 Relying Party
    """
    ret_obj = search(isamAppliance, name, check_mode=check_mode, force=force)
    id = ret_obj['data']

    if id == {}:
        logger.info("FIDO2 relying party {0} not found, skipping delete.".format(name))
    else:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Delete a FIDO2 relying party",
                "{0}/{1}".format(uri, id),
                requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()

def set(isamAppliance, name, rpId, fidoServerOptions, relyingPartyOptions, id=None, check_mode=False, force=False):
    """
    Create or Update a FIDO2 Relying Party
    """
    if (search(isamAppliance, name=name))['data'] == {}:
        # Force the add - we already know FIDO2 Relying Party does not exist
        logger.info("FIDO2 relying party {0} had no match, requesting to add new one.".format(name))
        return add(isamAppliance, name=name, rpId=rpId, fidoServerOptions=fidoServerOptions, relyingPartyOptions=relyingPartyOptions,
                   id=id, check_mode=check_mode, force=True)
    else:
        # Update request
        logger.info("FIDO2 relying party {0} exists, requesting to update.".format(name))
        return update(isamAppliance, name=name, rpId=rpId, fidoServerOptions=fidoServerOptions, relyingPartyOptions=relyingPartyOptions,
                      check_mode=check_mode, force=force)

def add(isamAppliance, name, rpId, fidoServerOptions, relyingPartyOptions, id=None, check_mode=False, force=False):
    """
    Create a new FIDO2 Relying Party

    The id parameter is ignored if appliance is less than version 10.0.1
    """
    if force is False:
        ret_obj = search(isamAppliance, name)
    if force is True or ret_obj['data'] == {}:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            json_data = {
                "name": name,
                "rpId": rpId,
                "fidoServerOptions": fidoServerOptions,
                "relyingPartyOptions": relyingPartyOptions
            }
            if id is not None and tools.version_compare(isamAppliance.facts['version'], '10.0.1') >= 0:
                json_data["id"] = id
            return isamAppliance.invoke_post(
                "Create a new FIDO2 relying party", uri, json_data, requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()

def update(isamAppliance, name, rpId, fidoServerOptions, relyingPartyOptions, check_mode=False, force=False):
    """
    Update a specific FIDO2 Relying Party
    """
    rp_id, update_required, json_data = _check(isamAppliance, name=name, rpId=rpId, fidoServerOptions=fidoServerOptions, relyingPartyOptions=relyingPartyOptions)
    if rp_id is None:
        from ibmsecurity.appliance.ibmappliance import IBMError
        raise IBMError("999", "Cannot update data for unknown FIDO2 relying party: {0}".format(name))

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Update a specific FIDO2 relying party",
                "{0}/{1}".format(uri, rp_id), json_data,
                requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object()

def _get(isamAppliance, id):
    return isamAppliance.invoke_get("Retrieve a specific FIDO2 relying party by id",
                                    f"{uri}/{id}")

def _extract_filename(upload_filename):
    """
    Extract filename from fully qualified path to use if no filename provided
    """
    import os.path
    return os.path.basename(upload_filename)

def _check(isamAppliance, name, rpId, fidoServerOptions, relyingPartyOptions):
    """
    Check and return True if update needed

    :param isamAppliance:
    :param name:
    :param rpId:
    :param fidoServerOptions:
    :param relyingPartyOptions:
    :return:
    """
    update_required = False
    json_data = {}
    ret_obj = get(isamAppliance, name)
    if ret_obj['data'] == {}:
        logger.info("FIDO2 relying party not found, returning no update required.")
        return None, update_required, json_data
    else:
        rp_id = ret_obj['data']['id']

        if name is not None:
            json_data["name"] = name

        if rpId is not None:
            json_data["rpId"] = rpId

        if fidoServerOptions is not None:
            json_data["fidoServerOptions"] = fidoServerOptions

        if relyingPartyOptions is not None:
            json_data["relyingPartyOptions"] = relyingPartyOptions

        # Remove id as this is server specific dynamic data. Not required for configuration comparison
        del ret_obj['data']['id']

        import ibmsecurity.utilities.tools
        sorted_json_data = ibmsecurity.utilities.tools.json_sort(json_data)
        logger.debug("Sorted input: {0}".format(sorted_json_data))
        sorted_ret_obj = ibmsecurity.utilities.tools.json_sort(ret_obj['data'])
        logger.debug("Sorted existing data: {0}".format(sorted_ret_obj))
        if sorted_ret_obj != sorted_json_data:
            logger.info("Changes detected, update needed.")
            update_required = True
        else:
            logger.info("No Changes detected, update NOT required.")
    return rp_id, update_required, json_data
