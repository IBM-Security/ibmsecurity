import logging

logger = logging.getLogger(__name__)


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the complete list of MMFA endpoints
    """
    return isamAppliance.invoke_get("Retrieving the complete list of MMFA endpoints",
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
    return isamAppliance.invoke_post(
                "Set MMFA endpoint configuration",
                "/iam/access/v8/mmfa-config/", json_data)

def mmfa_config_webseal(isamAppliance, instanceid, lmi, runtime, reuse_certs, reuse_acls, reuse_pops,  check_mode=False, force=False):
    """
    Configure WebSEAL for MMFA
    """
    json_data = {
        "lmi": lmi,
        "runtime": runtime,
        "reuse_certs": reuse_certs,
        "reuse_acls": reuse_acls,
        "reuse_pops": reuse_pops
    }
    return isamAppliance.invoke_post(
                "Configure WebSEAL for MMFA",
                "/wga/reverseproxy/{0}/mmfa_config".format(instanceid), json_data)

