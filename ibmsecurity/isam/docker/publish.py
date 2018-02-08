import logging

logger = logging.getLogger(__name__)


def publish_changes(isamAppliance, check_mode=False, force=False):
    """
    Publish configuration changes
    """
    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:
        return isamAppliance.invoke_put("Publishing configuration changes", "/docker/publish", {})
