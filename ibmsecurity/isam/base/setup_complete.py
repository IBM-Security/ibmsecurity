import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get(isamAppliance):
    """
    Get Set up complete status
    """
    return isamAppliance.invoke_get("Get Setup Complete Settings",
                                    "/setup_complete")


def set(isamAppliance, check_mode=False, force=False):
    """
    Setup complete
    """
    if force is False:
        ret_obj = get(isamAppliance)

    if force is True or ret_obj['data'].get('configured') is not True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Setup complete",
                "/setup_complete",
                {})

    return isamAppliance.create_return_object()
