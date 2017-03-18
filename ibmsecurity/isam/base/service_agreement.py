import logging

logger = logging.getLogger(__name__)


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the service agreement settings
    """
    return isamAppliance.invoke_get("Retrieving the service agreement settings", "/setup_service_agreements/accepted")


def set(isamAppliance, check_mode=False, force=False):
    """
    Accept Service Agreement
    """

    if force is True or _check(isamAppliance) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Accept service agreements",
                "/setup_service_agreements/accepted",
                {
                    "accepted": True
                })

    return isamAppliance.create_return_object(changed=False)


def _check(isamAppliance):

    ret_obj = get(isamAppliance)

    rc = False

    if ret_obj['data']['accepted']:
        logger.info("service agreements already accepted")
        rc = True

    return rc


