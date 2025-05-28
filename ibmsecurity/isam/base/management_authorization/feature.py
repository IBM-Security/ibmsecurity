import logging

logger = logging.getLogger(__name__)


def get_all(isamAppliance):
    """
    Get all features
    """
    return isamAppliance.invoke_get("Get all features",
                                    "/authorization/features/v1")


def get_user(isamAppliance, user):
    """
    Get permitted features for user
    NOTE: Getting an unexplained error for this function, URL maybe wrong
    """
    return isamAppliance.invoke_get("Get permitted features for user",
                                    f"/authorization/features/users/{user}/v1")


def get_current(isamAppliance):
    """
    Get permitted features for current user
    """
    return isamAppliance.invoke_get("Get permitted features for current user",
                                    "/permissions/v1")
