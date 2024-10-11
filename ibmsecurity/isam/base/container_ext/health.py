import logging

logger = logging.getLogger(__name__)

uri = "/isam/container_ext/health"

requires_version = "10.0.7.0"
requires_model = "Appliance"


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieving health for all (running?) containers TODO: THIS FAILS
    ./testisam_cmd.py --hostname=${ISAM_LMI} --method=ibmsecurity.isam.base.container_ext.health.get_all

    """
    return isamAppliance.invoke_get(
        "Retrieving health for all containers",
        f"{uri}",
        requires_model=requires_model,
        requires_version=requires_version,
    )


def get(isamAppliance, container_id, check_mode=False, force=False):
    """
    Get health for a specific container
    """
    return isamAppliance.invoke_get(
        "Retrieving health for container",
        f"{uri}/{container_id}",
        requires_model=requires_model,
        requires_version=requires_version,
    )
