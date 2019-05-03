import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get(isamAppliance, check_mode=False, force=False):
    """
    Get existing activations
    """
    return isamAppliance.invoke_get("Retrieving activations",
                                    "/isam/capabilities/v1")


def get_activation(isamAppliance, name=None, id=None, check_mode=False, force=False):
    """
    Retrieve a specified activation offering
    """
    if id == None:
        if name != None:
            id = _get_id(isamAppliance, name)

    return isamAppliance.invoke_get("Retrieve a specified activation offering",
                                    "/isam/capabilities/{0}/v1".format(id))


def update(isamAppliance, enabled, name=None, id=None, check_mode=False, force=False):
    """
    Update an activation offering
    """

    if id == None:
        if name != None:
            id = _get_id(isamAppliance, name)

    if force is True or check(isamAppliance, id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put("Update an activation offering",
                                            "/isam/capabilities/{0}/v1".format(id),
                                            {'enabled': enabled}
                                            )

    return isamAppliance.create_return_object()


def set(isamAppliance, id, code, check_mode=False, force=False):
    """
    Activate an ISAM module
    """
    if force is True or check(isamAppliance, id) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            ret_obj = isamAppliance.invoke_post(
                "Activating a Module",
                "/isam/capabilities/v1",
                {
                    'code': code
                })
            # Update 'facts', with newly activated module
            if 'activations' not in isamAppliance.facts:
                isamAppliance.facts['activations'] = []
            isamAppliance.facts['activations'].append(id)
            return ret_obj

    return isamAppliance.create_return_object()


def delete(isamAppliance, id, check_mode=False, force=False):
    """
    Delete activation of an ISAM module
    """
    if force is True or check(isamAppliance, id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            ret_obj = isamAppliance.invoke_delete(
                "Deleting activation of Module",
                "/isam/capabilities/{0}/v1".format(id))
            # Update 'facts', remove module
            isamAppliance.facts['activations'].remove(id)
            return ret_obj

    return isamAppliance.create_return_object()


def check(isamAppliance, id):
    """
    Check if ISAM module is already activated
    """
    ret_obj = get(isamAppliance)

    for activation in ret_obj['data']:
        if id == activation['id']:
            logger.info("This module is already activated: " + id)
            return True

    return False


def compare(isamAppliance1, isamAppliance2):
    """
    Compare activations of ISAM modules between two appliances
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])


def _get_id(isamAppliance, name):
    ret_obj = get(isamAppliance)
    for activation in ret_obj['data']:
        if name == activation['name']:
            objid = activation['id']
            return objid
