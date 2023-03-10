"""
Explorative implement for un-documented ISVG RESTAPI (not functional as of now)
Preserved here for the future in case if support (RFE)
"""
import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get(isvgAppliance):
    """
    Get Set up complete status
    """
    return isvgAppliance.invoke_get("Get Setup Complete Settings",
                                    "/setup_complete")


def set(isvgAppliance, check_mode=False, force=False):
    """
    Setup complete
    """
    if force is False:
        ret_obj = get(isvgAppliance)

    if force is True or ret_obj['data'].get('configured') is not True:
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True)
        else:
            return isvgAppliance.invoke_put(
                "Setup complete",
                "/setup_complete",
                {})

    return isvgAppliance.create_return_object()
