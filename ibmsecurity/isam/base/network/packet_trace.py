import logging
import os.path

from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

requires_model = "Appliance"


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the general configuration
    """
    return isamAppliance.invoke_get("Retrieving the general configuration", "/isam/packet_tracing",
                                    requires_model=requires_model)


def execute(isamAppliance, enabled, filter=None, interface=None, max_size=None, check_mode=False,
            force=False, snaplen=None):
    """
    Execute an operation (start, stop or restart) on packet tracing
    """

    check_value, warnings = _check(isamAppliance, enabled)
    json_data = {"enable": enabled}

    if filter is not None:
        json_data['filter'] = filter

    if interface is not None:
        json_data['interface'] = interface

    if max_size is not None:
        json_data['max_size'] = interface

    if snaplen is not None:
        if tools.version_compare(isamAppliance.facts["version"], "9.0.6.0") < 0:
            warnings.append(
                "Appliance at version: {}, snaplen: {1} is not supported. Needs 9.0.6.0 or higher.  Ignoring snaplen for this call.".format(
                    isamAppliance.facts["version"], snaplen
                )
            )
        else:
            json_data["snaplen"] = snaplen

    if force is True or check_value is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_put(
                "Executing an operation on packet trace", "/isam/packet_tracing/", json_data,
                requires_model=requires_model, warnings=warnings)

    return isamAppliance.create_return_object(warnings=warnings)


def delete(isamAppliance, check_mode=False, force=False):
    """
    Clearing the packet tracing PCAP files
    """

    ret_obj = get(isamAppliance)

    if force is True or ret_obj['data']['files'] != []:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=ret_obj['warnings'])
        else:
            return isamAppliance.invoke_delete(
                "Clearing the packet tracing PCAP files", "/isam/packet_tracing/", requires_model=requires_model)

    return isamAppliance.create_return_object(warnings=ret_obj['warnings'])


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
                "/isam/packet_tracing/pcap/{0}?export".format(filename), filepath, requires_model=requires_model
            )

    return isamAppliance.create_return_object()


def _check(isamAppliance, enabled):
    ret_obj = get(isamAppliance)
    warnings = ret_obj['warnings']

    if 'enabled' in ret_obj['data']:
        return ret_obj['data']['enabled'] == enabled, warnings
    else:
        return True, warnings
