import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the LMI trace specification
    """
    return isamAppliance.invoke_get("Retrieving the LMI trace specification", "/admin_cfg/lmi_tracing")


def set(isamAppliance, trace_specification, check_mode=False, force=False):
    """
    Updating the LMI trace specification
    """
    current_obj = get(isamAppliance)
    current_specs = current_obj['data']['trace_specification']

    old_specs = current_specs.split(":")
    new_specs = trace_specification.split(":")

    old_specs.sort()
    new_specs.sort()

    if old_specs != new_specs or force is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Updating the LMI trace specification",
                "/admin_cfg/lmi_tracing", {'trace_specification': trace_specification})

    return isamAppliance.create_return_object()


def delete(isamAppliance, check_mode=False, force=False):
    """
    Resetting the LMI trace specification
    """
    current_obj = get(isamAppliance)
    current_specs = current_obj['data']['trace_specification']

    if force is True or current_specs != "*=config=enabled":
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Resetting the LMI trace specification",
                "/admin_cfg/lmi_tracing",
            )

    return isamAppliance.create_return_object()


def compare(isamAppliance1, isamAppliance2):
    """
    Compare lmi tracing between two appliances
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    return tools.json_compare(ret_obj1, ret_obj2)
