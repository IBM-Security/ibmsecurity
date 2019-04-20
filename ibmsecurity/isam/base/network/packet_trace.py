import logging
import os.path

logger = logging.getLogger(__name__)


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the general configuration
    """
    return isamAppliance.invoke_get("Retrieving the general configuration", "/isam/packet_tracing")


def execute(isamAppliance, operation, enabled, filter=None, interface=None, max_size=None, check_mode=False,
            force=False):
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
                    "enable": enabled,
                    "filter": filter,
                    "interface": interface,
                    "max_size": max_size
                }, warnings=warnings)

    return isamAppliance.create_return_object(warnings=warnings)


def delete(isamAppliance, check_mode=False, force=False):
    """
    Execute an operation (start, stop or restart) on packet tracing
    """
    warnings = ["No idempotency check coded yet."]

    if force is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_delete(
                "Executing  delete operation on packet trace", "/isam/packet_tracing/", warnings=warnings)

    return isamAppliance.create_return_object(warnings=warnings)


def export_file(isamAppliance, filepath, filename, check_mode=False, force=False):
    """
    Exporting the packet tracing PCAP file
    """
    if force is True or os.path.exists(filepath) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_get_file(
                "Exporting the packet tracing PCAP file",
                "/isam/packet_tracing/pcap/{0}?export".format(filename), filepath
            )

    return isamAppliance.create_return_object()


def _check(isamAppliance, enabled):
    ret_obj = get(isamAppliance)

    return ret_obj['data']['enabled'] == enabled
