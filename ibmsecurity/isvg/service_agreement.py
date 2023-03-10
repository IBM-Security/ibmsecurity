"""
Explorative implement for un-documented ISVG RESTAPI (not functional as of now)
Preserved here for the future in case if support (RFE)
"""
import logging

logger = logging.getLogger(__name__)
uri = "/setup_service_agreements"


def get(isvgAppliance, check_mode=False, force=False):
    """
    Retrieving the service agreement settings
    """
    return isvgAppliance.invoke_get("Retrieving the service agreement settings", "/setup_service_agreements/accepted")


def set(isvgAppliance, check_mode=False, force=False):
    """
    Accept Service Agreement
    """

    if force is True or _check(isvgAppliance) is False:
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True)
        else:
            return isvgAppliance.invoke_put(
                "Accept service agreements",
                "/setup_service_agreements/accepted",
                {
                    "accepted": True
                })

    return isvgAppliance.create_return_object(changed=False)


def get_non_ibm(isvgAppliance, offering, check_mode=False, force=False):
    """
    Reading non-IBM the software license agreement terms
    """
    return isvgAppliance.invoke_get("Reading non-IBM the software license agreement terms",
                                    "{0}/non_ibm_text/{1}".format(uri, offering))


def get_terms(isvgAppliance, check_mode=False, force=False):
    """
    Reading the software license agreement terms
    """
    return isvgAppliance.invoke_get("Reading the software license agreement terms", "{0}/".format(uri))


def _check(isvgAppliance):
    ret_obj = get(isvgAppliance)

    rc = False

    if ret_obj['data']['accepted']:
        logger.info("service agreements already accepted")
        rc = True

    return rc
