import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)

uri = "/setup_complete_guided"

def get(isvgAppliance, check_mode=False, force=False):
    """
    Get Set up complete status
    """
    return isvgAppliance.invoke_get("Get Setup Complete Settings", "/")


def complete(isvgAppliance, check_mode=False, force=False):
    """
    Setup complete
    """
    if force is False:
        ret_obj = get(isvgAppliance)

    #
    # if the guided setup is complete, fetching data at '/' will return non-empty JSON payload
    if force is True or len(ret_obj['data']) == 0:
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True)
        else:
            return isvgAppliance.invoke_post(
                "Setup complete",
                uri,
                {})

    return isvgAppliance.create_return_object()
