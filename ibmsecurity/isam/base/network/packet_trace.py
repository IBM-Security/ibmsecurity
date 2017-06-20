import json
import logging

logger = logging.getLogger(__name__)


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the general configuration
    """
    return isamAppliance.invoke_get("Retrieving the general configuration", "/isam/packet_tracing")


# def start(isamAppliance, enable=False, filter,interface,max_size,check_mode=False, force=False):
#     """
#     Updating the general configuration
#     """
#     if force is True or _check(isamAppliance, hostname) is False:
#         if check_mode is True:
#             return isamAppliance.create_return_object(changed=True)
#         else:
#             return isamAppliance.invoke_put("Updating the general configuration", "isam/packet_tracing",
#                                             {
#                                                 'hostName': hostname
#                                             })

#     return isamAppliance.create_return_object()


def execute(isamAppliance, operation, enabled, filter=None, interface=None,max_size=None,check_mode=False, force=False):
    """
    Execute an operation (start, stop or restart) on packet tracing
    """
    warnings = []

    if force is True or _check(isamAppliance, enabled) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_put(
                "Executing an operation on packet trace", "/isam/packet_tracing/",
                {
                     "enable":enabled,
                    "filter":filter,
                    "interface":interface,
                    "max_size":max_size
                })

    return isamAppliance.create_return_object()


def delete(isamAppliance, check_mode=False, force=False):
    """
    Execute an operation (start, stop or restart) on packet tracing
    """
    warnings = []

    if force is True :
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
    else:
        return isamAppliance.invoke_delete(
        "Executing  delete operation on packet trace", "/isam/packet_tracing/")

    return isamAppliance.create_return_object()


def _check(isamAppliance, enabled):
    ret_obj = get(isamAppliance)
    print ret_obj
    return ret_obj['data']['enabled'] == enabled