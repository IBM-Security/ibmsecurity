import json
import logging

logger = logging.getLogger(__name__)


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the general configuration
    """
    return isamAppliance.invoke_get("Retrieving the general configuration", "/net/general")


def set(isamAppliance, hostname, check_mode=False, force=False):
    """
    Updating the general configuration
    """
    if force is True or _check(isamAppliance, hostname) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put("Updating the general configuration", "/net/general",
                                            {
                                                'hostName': hostname
                                            })

    return isamAppliance.create_return_object()


def _check(isamAppliance, hostname):
    ret_obj = get(isamAppliance)
    return ret_obj['data']['hostName'] == hostname
