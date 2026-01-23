import logging

logger = logging.getLogger(__name__)

uri = "/wga/common_configuration"
requires_modules = ["wga"]
requires_version = None


def get_all(isamAppliance, reverseproxy_id, check_mode=False, force=False):
    """
    Retrieving all common configuration for reverse proxy
    """
    return isamAppliance.invoke_get("Retrieving the all common configuration for reverse proxy",
                                    f"{uri}/{reverseproxy_id}",
                                    requires_modules=requires_modules,
                                    requires_version=requires_version)


def get(isamAppliance, reverseproxy_id, configuration_id, check_mode=False, force=False):
    """
    Retrieving value of specified configuration id from reverse proxy common configuration
    """
    ret_object = get_all(isamAppliance, reverseproxy_id, check_mode, force)

    logger.debug(f"Looking for {configuration_id} value in reverse proxy {reverseproxy_id}")

    ret_obj = isamAppliance.create_return_object()

    try:
        ret_obj['data'] = ret_object['data'][configuration_id]
    except:
        logger.error(f"Invalid configuration_id: {configuration_id}")

    return ret_obj
