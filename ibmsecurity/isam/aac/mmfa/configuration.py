import logging

logger = logging.getLogger(__name__)
uri = "/iam/access/v8/mmfa-config"
requires_modules = None
requires_version = None


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieve MMFA endpoint details
    """
    return isamAppliance.invoke_get("Retrieve MMFA endpoint details",
                                    "/iam/access/v8/mmfa-config")


def set(isamAppliance, client_id, options, endpoints, discovery_mechanisms, check_mode=False, force=False):
    """
    Set MMFA endpoint configuration
    """
    json_data = {
        "client_id": client_id,
        "options": options,
        "endpoints": endpoints,
        "discovery_mechanisms": discovery_mechanisms
    }
    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:
        return isamAppliance.invoke_post(
            "Set MMFA endpoint configuration",
            "/iam/access/v8/mmfa-config/", json_data)


def delete(isamAppliance, check_mode=False, force=False):
    """
    Unconfigure MMFA endpoint details
    """
    ret_obj = get(isamAppliance)

    if force is True or ret_obj['data'] != {}:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Unconfigure MMFA endpoint details",
                "{0}".format(uri),
                requires_modules=requires_modules, requires_version=requires_version
            )

    return isamAppliance.create_return_object()
