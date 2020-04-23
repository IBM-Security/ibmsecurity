import logging

logger = logging.getLogger(__name__)

requires_model = "Docker"


def publish_changes(isamAppliance, check_mode=False, force=False):
    """
    Publish configuration changes
    """
    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:
        return isamAppliance.invoke_put("Publishing configuration changes", "/docker/publish", {},
                                        requires_model=requires_model)


def stop(isamAppliance, check_mode=False, force=False):
    """
    Stopping the configuration container
    """
    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:
        return isamAppliance.invoke_put("Stopping the configuration container", "/core/docker/stop", {},
                                        requires_model=requires_model)
