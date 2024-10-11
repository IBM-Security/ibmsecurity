import logging
import ibmsecurity.isam.base.container_ext.container as container

logger = logging.getLogger(__name__)

uri = "/isam/container_ext/health"

requires_version = "10.0.7.0"
requires_model = "Appliance"


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieving health for all (running?) containers TODO: THIS FAILS IN 10.0.8
    ./testisam_cmd.py --hostname=${ISAM_LMI} --method=ibmsecurity.isam.base.container_ext.health.get_all

    """
    return isamAppliance.invoke_get(
        "Retrieving health for all containers",
        f"{uri}",
        requires_model=requires_model,
        requires_version=requires_version,
    )


def get(isamAppliance, name=None, container_id=None, check_mode=False, force=False):
    """
    Get health for a specific container TODO: THIS FAILS IN 10.0.8
    Supply either name or id.
    ./testisam_cmd.py --hostname=${ISAM_LMI} --method=ibmsecurity.isam.base.container_ext.health.get --method_options="container_id=a6252734-87d3-11ef-bec6-000c29d80c72"
    """
    if container_id is None and name is not None:
        container_id = container.search(isamAppliance, name)
        container_id = container_id.get('data', None)

    if container_id is not None:
        return isamAppliance.invoke_get(
            "Retrieving health for container",
            f"{uri}/{container_id}",
            requires_model=requires_model,
            requires_version=requires_version,
        )
    else:
        return isamAppliance.create_return_object()
