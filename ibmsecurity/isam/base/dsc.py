import logging
import copy
import ibmsecurity.utilities.tools
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

uri = "/isam/dsc/config²"
requires_modules = None
requires_version = None


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieve the current cluster configuration
    """
    return isamAppliance.invoke_get("Retrieve the current dsc configuration", uri,
                                    requires_modules=requires_modules, requires_version=requires_version)


def set(isamAppliance, service_port=443, replication_port=444, worker_threads=64, max_session_lifetime=3600, client_grace=600,
        ignore_password_for_idempotency=False, servers=None, force=False):
    """
    Set DSC configuration
    """
    warnings = []
    # Create a simple json with just the main client attributes
    dsc_json = {
        "worker_threads": worker_threads,
        "max_session_lifetime": max_session_lifetime,
        "client_grace": client_grace,
        "service_port": service_port,
        "replication_port": replication_port
    }
    if servers is not None:
        dsc_json["servers@"]=servers

    if force is True or _check(isamAppliance, dsc_json, ignore_password_for_idempotency) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_post("Set dsc configuration", uri, _json,
                                             requires_modules=requires_modules, requires_version=requires_version,
                                             warnings=warnings)

    return isamAppliance.create_return_object(warnings=warnings)


def _check(isamAppliance, cluster_json, ignore_password_for_idempotency):
    """
    Check if provided json values match the configuration on appliance

    :param isamAppliance:
    :param cluster_json:
    :return:
    """
    ret_obj = get(isamAppliance)
    sorted_ret_obj = tools.json_sort(ret_obj['data'])
    sorted_json_data = tools.json_sort(cluster_json)
    logger.debug("Sorted Existing Data:{0}".format(sorted_ret_obj))
    logger.debug("Sorted Desired  Data:{0}".format(sorted_json_data))

    if ignore_password_for_idempotency:
        temp = copy.deepcopy(
            cluster_json)  # deep copy neccessary: otherwise password parameter would be removed from desired config dict 'cluster_json'. Comparison is done with temp<>ret_obj object
        for idx, x in enumerate(cluster_json):
            if "password" in x:
                logger.debug("Ignoring JSON password entry: '{0}' to satisfy idempotency.".format(x))
                del temp[x]
        logger.debug("Passwordless JSON to Apply: {0}".format(temp))
    else:
        temp = cluster_json

    for key, value in temp.iteritems():
        try:
            if isinstance(value, list):
                if ibmsecurity.utilities.tools.json_sort(
                        ret_obj['data'][key] != ibmsecurity.utilities.tools.json_sort(value)):
                    logger.debug(
                        "For key: {0}, values: {1} and {2} do not match.".format(key, value, ret_obj['data'][key]))
                    return False
            else:
                if ret_obj['data'][key] != value:
                    logger.debug(
                        "For key: {0}, values: {1} and {2} do not match.".format(key, value, ret_obj['data'][key]))
                    return False
        except:  # In case there is an error looking up the key in existing configuration (missing)
            logger.debug("Exception processing Key: {0} Value: {1} - missing key in current config?".format(key, value))
            return False

    logger.debug("JSON provided already is contained in current appliance configuration.")
    return True


def compare(isamAppliance1, isamAppliance2):
    """
    Compare cluster configuration between two appliances
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
