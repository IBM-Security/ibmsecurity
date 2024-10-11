import logging

logger = logging.getLogger(__name__)

uri = "/isam/container_ext/metadata"

requires_version = "10.0.7.0"
requires_model = "Appliance"


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieving all metadata
    ./testisam_cmd.py --hostname=${ISAM_LMI} --method=ibmsecurity.isam.base.container_ext.metadata.get_all

    """
    return isamAppliance.invoke_get(
        "Retrieving metadata",
        f"{uri}",
        requires_model=requires_model,
        requires_version=requires_version,
    )


def get(isamAppliance, metadata_name, check_mode=False, force=False):
    """
    Get specific metadata for a specific container
    ./testisam_cmd.py --hostname=${ISAM_LMI} --method=ibmsecurity.isam.base.container_ext.metadata.get --method_options="metadata_name=ibm-application-gateway"
    """
    return isamAppliance.invoke_get(
        "Retrieving metadata",
        f"{uri}/{metadata_name}",
        requires_model=requires_model,
        requires_version=requires_version,
    )
