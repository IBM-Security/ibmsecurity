import logging

logger = logging.getLogger(__name__)


def get(isamAppliance, check_mode=False, force=False):
    """
    Get the status of the geolocation database load
    """
    return isamAppliance.invoke_get("Retrieving geolocation DB settings...",
                                    "/iam/access/v8/geolocation-db/status")


def load(isamAppliance, file=None, check_mode=False, force=False):
    """
    Load new geolocation database
    """
    warnings = ["No idempotency check coded yet."]

    if check_mode is True:
        return isamAppliance.create_return_object(changed=True, warnings=warnings)
    else:
        return isamAppliance.invoke_put("Load new GEO Database",
                                        "/iam/access/v8/geolocation-db",
                                        {'file': file}, warnings=warnings)

    return isamAppliance.create_return_object()


def compare():
    """
    Need to code a compare logic
    :return: 
    """
    pass