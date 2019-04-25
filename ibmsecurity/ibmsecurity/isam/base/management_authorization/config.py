import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get(isamAppliance, check_mode=False, force=False):
    """
    Get management authorization - config
    """
    return isamAppliance.invoke_get("Get management authorization - config",
                                    "/authorization/v1")


def _check(isamAppliance):
    """
    Check if management authorization is enabled
    """
    ret_obj = get(isamAppliance)

    return ret_obj['data']['config']['enforcing']


def set(isamAppliance, enforcing=True, check_mode=False, force=False):
    """
    Set remote management authorization
    """
    if force is True or _check(isamAppliance) != enforcing:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Set management authorization - config",
                "/authorization/config/v1",
                {
                    'enforcing': enforcing
                })

    return isamAppliance.create_return_object()


def compare(isamAppliance1, isamAppliance2):
    """
    Compare management authorization config settings
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
