import logging
from ibmsecurity.utilities import tools
from ibmsecurity.utilities.tools import json_sort

logger = logging.getLogger(__name__)

# URI for this module
uri = "/iam/access/v8/push-notification"
requires_modules = ["mga"]
requires_version = None


def get_all(isamAppliance, filter=None, sortBy=None, check_mode=False, force=False):
    """
    Retrieve a list of push notification registrations
    """
    return isamAppliance.invoke_get("Retrieve a list of push notification registrations",
                                    "{0}".format(uri),
                                    requires_modules=requires_modules, requires_version=requires_version)


def get(isamAppliance, app_id, check_mode=False, force=False):
    """
    Retrieve a push notification registration
    """
    ret_obj = search(isamAppliance, app_id, check_mode=False, force=False)
    id = ret_obj['data']

    if id == {}:
        logger.info("Push notification registration '{0}' had no match, skipping retrieval.".format(app_id))
        warnings = ["Push notification registration '{0}' had no match, skipping retrieval.".format(app_id)]
        return isamAppliance.create_return_object(warnings=warnings)
    else:
        return _get(isamAppliance, id)


def add(isamAppliance, app_id, platform, provider, check_mode=False, force=False):
    """
    Create a push notification registration
    """
    ret_obj = search(isamAppliance, app_id, check_mode=False, force=False)
    id = ret_obj['data']

    if id != {}:
        logger.info("Push notification registration '{0}' already exists.  Skipping add.".format(app_id))

    if force is True or id == {}:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:

            return isamAppliance.invoke_post(
                "Create a push notification registration",
                "{0}".format(uri),
                {
                    'app_id': app_id,
                    'platform': platform,
                    'provider': provider
                },
                requires_modules=requires_modules, requires_version=requires_version
            )

    return isamAppliance.create_return_object()


def update(isamAppliance, app_id, platform, provider, new_app_id=None, check_mode=False, force=False):
    """
    Update a push notification registration
    """
    ret_obj = search(isamAppliance, app_id=app_id)
    id = ret_obj['data']

    update_required = False

    if id != {}:
        ret_obj = _get(isamAppliance, id=id)

        json_data = {
            'platform': platform,
            'provider': provider
        }
        if new_app_id is not None:
            json_data['app_id'] = new_app_id,
        else:
            json_data['app_id'] = app_id

        sorted_json_data = json_sort(json_data)

        logger.debug("Sorted input: {0}".format(sorted_json_data))

        del ret_obj['data']['push_id']
        sorted_ret_obj = json_sort(ret_obj['data'])

        logger.debug("Sorted existing data: {0}".format(sorted_ret_obj))

        if sorted_json_data != sorted_ret_obj:
            update_required = True
        else:
            logger.info(
                "Input is the same as current Push notification registration '{0}'.  Skipping update.".format(app_id))
    else:
        logger.info("Push notification registration '{0}' does not exists.  Skipping update.".format(app_id))
        warnings = ["Push notification registration '{0}' does not exists.  Skipping update.".format(app_id)]
        return isamAppliance.create_return_object(warnings=warnings)

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Update a push notification registration",
                "{0}/{1}".format(uri, id),
                json_data,
                requires_modules=requires_modules, requires_version=requires_version
            )

    return isamAppliance.create_return_object()


def set(isamAppliance, app_id, platform, provider, new_app_id=None, check_mode=False,
        force=False):
    """
    Creating or Modifying a Database PIP
    """
    ret_obj = search(isamAppliance, app_id=app_id)
    id = ret_obj['data']

    if id == {}:
        # If no id was found, Force the add
        return add(isamAppliance, app_id=app_id, platform=platform, provider=provider, check_mode=check_mode,
                   force=True)
    else:
        # Update PIP
        return update(isamAppliance, app_id=app_id, platform=platform, provider=provider, new_app_id=new_app_id,
                      check_mode=check_mode, force=force)


def delete(isamAppliance, app_id, check_mode=False, force=False):
    """
    Delete a push notification registration
    """
    ret_obj = search(isamAppliance, app_id, check_mode=False, force=False)
    id = ret_obj['data']

    if force is True or id != {}:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:

            return isamAppliance.invoke_delete(
                "Delete a push notification registration",
                "{0}/{1}".format(uri, id),
                requires_modules=requires_modules, requires_version=requires_version
            )

    if id == {}:
        logger.info("Push notification registration '{0}' does not exists, skipping delete.".format(app_id))

    return isamAppliance.create_return_object()


def compare(isamAppliance1, isamAppliance2):
    """
    Compare access policies between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    for obj in ret_obj1['data']:
        del obj['push_id']

    for obj in ret_obj2['data']:
        del obj['push_id']

    return tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['push_id'])


def search(isamAppliance, app_id, force=False, check_mode=False):
    """
    Retrieve ID for named Push notification registration
    """
    ret_obj = get_all(isamAppliance)

    ret_obj_new = isamAppliance.create_return_object()

    for obj in ret_obj['data']:
        if obj['app_id'] == app_id:
            logger.info("Found Push notification registration '{0}' id: '{1}'".format(app_id, obj['push_id']))
            ret_obj_new['data'] = obj['push_id']

    return ret_obj_new


def _get(isamAppliance, id):
    return isamAppliance.invoke_get("Retrieve a specific Push notification registration",
                                    "{0}/{1}".format(uri, id))
