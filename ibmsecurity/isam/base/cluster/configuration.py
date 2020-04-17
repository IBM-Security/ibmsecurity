import logging
import copy
import ibmsecurity.utilities.tools
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

uri = "/isam/cluster/v2"
requires_modules = None
requires_version = None
requires_model = "Appliance"

try:
    basestring
except NameError:
    basestring = (str, bytes)


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieve the current cluster configuration
    """
    return isamAppliance.invoke_get("Retrieve the current cluster configuration", uri,
                                    requires_modules=requires_modules, requires_version=requires_version,
                                    requires_model=requires_model)


def set(isamAppliance, primary_master='127.0.0.1', secondary_master=None, master_ere=None, tertiary_master=None,
        quaternary_master=None, dsc_external_clients=False, dsc_port=None, dsc_use_ssl=None, dsc_ssl_keyfile=None,
        dsc_ssl_label=None, dsc_worker_threads=64, dsc_maximum_session_lifetime=3600, dsc_client_grace_period=600,
        hvdb_embedded=True, hvdb_max_size=None, hvdb_db_type=None, hvdb_address=None, hvdb_port=None, hvdb_user=None,
        hvdb_password=None, hvdb_db2_alt_address=None, hvdb_db2_alt_port=None, hvdb_db_name=None, hvdb_db_secure=None,
        hvdb_driver_type=None, hvdb_solid_tc=None, cfgdb_embedded=True, cfgdb_db_type=None, cfgdb_address=None,
        cfgdb_port=None, cfgdb_user=None, cfgdb_password=None, cfgdb_db2_alt_address=None, cfgdb_db2_alt_port=None,
        cfgdb_db_name=None, cfgdb_db_secure=None, cfgdb_driver_type=None, cfgdb_solid_tc=None, first_port=2020,
        cfgdb_fs=None, dsc_trace_level=None, ignore_password_for_idempotency=False, check_mode=False, force=False):
    """
    Set cluster configuration
    """

    warnings = []
    # Create a simple json with just the main client attributes
    cluster_json = {
        "primary_master": primary_master,
        "dsc_external_clients": dsc_external_clients,
        "dsc_worker_threads": dsc_worker_threads,
        "dsc_maximum_session_lifetime": dsc_maximum_session_lifetime,
        "dsc_client_grace_period": dsc_client_grace_period,
        "hvdb_embedded": hvdb_embedded,
        "cfgdb_embedded": cfgdb_embedded,
        "first_port": first_port
    }
    # Add attributes that have been supplied... otherwise skip them.
    if secondary_master is not None:
        cluster_json["secondary_master"] = secondary_master
    if master_ere is not None:
        cluster_json["master_ere"] = master_ere
    if tertiary_master is not None:
        cluster_json["tertiary_master"] = tertiary_master
    if quaternary_master is not None:
        cluster_json["quaternary_master"] = quaternary_master
    if dsc_port is not None:
        cluster_json["dsc_port"] = dsc_port
    if dsc_use_ssl is not None:
        cluster_json["dsc_use_ssl"] = dsc_use_ssl
    if dsc_ssl_keyfile is not None:
        cluster_json["dsc_ssl_keyfile"] = dsc_ssl_keyfile
    if dsc_ssl_label is not None:
        cluster_json["dsc_ssl_label"] = dsc_ssl_label
    if hvdb_max_size is not None:
        cluster_json["hvdb_max_size"] = hvdb_max_size
    if hvdb_db_type is not None:
        cluster_json["hvdb_db_type"] = hvdb_db_type
    if hvdb_address is not None:
        cluster_json["hvdb_address"] = hvdb_address
    if hvdb_port is not None:
        cluster_json["hvdb_port"] = hvdb_port
    if hvdb_user is not None:
        cluster_json["hvdb_user"] = hvdb_user
    if hvdb_password is not None:
        if ignore_password_for_idempotency:
            warnings.append("Request made to ignore hvdb_password for idempotency check.")
        else:
            warnings.append("Since existing hvdb_password cannot be read - this call will not be idempotent.")
        cluster_json["hvdb_password"] = hvdb_password
    if hvdb_db2_alt_address is not None:
        cluster_json["hvdb_db2_alt_address"] = hvdb_db2_alt_address
    if hvdb_db2_alt_port is not None:
        cluster_json["hvdb_db2_alt_port"] = hvdb_db2_alt_port
    if hvdb_db_name is not None:
        cluster_json["hvdb_db_name"] = hvdb_db_name
    if hvdb_db_secure is not None:
        cluster_json["hvdb_db_secure"] = hvdb_db_secure
    if hvdb_driver_type is not None:
        cluster_json["hvdb_driver_type"] = hvdb_driver_type
    if hvdb_solid_tc is not None:
        if (isinstance(hvdb_solid_tc, basestring)):
            import ast
            hvdb_solid_tc = ast.literal_eval(hvdb_solid_tc)
        cluster_json["hvdb_solid_tc"] = hvdb_solid_tc
    if cfgdb_db_type is not None:
        cluster_json["cfgdb_db_type"] = cfgdb_db_type
    if cfgdb_address is not None:
        cluster_json["cfgdb_address"] = cfgdb_address
    if cfgdb_port is not None:
        cluster_json["cfgdb_port"] = cfgdb_port
    if cfgdb_user is not None:
        cluster_json["cfgdb_user"] = cfgdb_user
    if cfgdb_password is not None:
        if ignore_password_for_idempotency:
            warnings.append("Request made to ignore cfgdb_password for idempotency check.")
        else:
            warnings.append("Since existing cfgdb_password cannot be read - this parameter is ignored for idempotency.")
        cluster_json["cfgdb_password"] = cfgdb_password
    if cfgdb_db2_alt_address is not None:
        cluster_json["cfgdb_db2_alt_address"] = cfgdb_db2_alt_address
    if cfgdb_db2_alt_port is not None:
        cluster_json["cfgdb_db2_alt_port"] = cfgdb_db2_alt_port
    if cfgdb_db_name is not None:
        cluster_json["cfgdb_db_name"] = cfgdb_db_name
    if cfgdb_db_secure is not None:
        cluster_json["cfgdb_db_secure"] = cfgdb_db_secure
    if cfgdb_driver_type is not None:
        cluster_json["cfgdb_driver_type"] = cfgdb_driver_type
    if cfgdb_solid_tc is not None:
        if (isinstance(cfgdb_solid_tc, basestring)):
            import ast
            cfgdb_solid_tc = ast.literal_eval(cfgdb_solid_tc)
        cluster_json["cfgdb_solid_tc"] = cfgdb_solid_tc
    if cfgdb_fs is not None:
        if ibmsecurity.utilities.tools.version_compare(isamAppliance.facts["version"], "9.0.2.0") < 0:
            warnings.append(
                "Appliance at version: {0}, cfgdb_fs: {1} is not supported. Needs 9.0.2.0 or higher. Ignoring cfgdb_fs for this call.".format(
                    isamAppliance.facts["version"], cfgdb_fs))
        else:
            cluster_json["cfgdb_fs"] = cfgdb_fs
    if dsc_trace_level is not None:
        cluster_json["dsc_trace_level"] = dsc_trace_level

    check_obj =  _check(isamAppliance, cluster_json, ignore_password_for_idempotency)
    warnings.append(check_obj['warnings'])
    if force is True or check_obj['value'] is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_post("Set cluster configuration", uri, cluster_json,
                                             requires_modules=requires_modules, requires_version=requires_version,
                                             requires_model=requires_model,
                                             warnings=warnings)

    return isamAppliance.create_return_object(warnings=warnings)


def _check(isamAppliance, cluster_json, ignore_password_for_idempotency):
    """
    Check if provided json values match the configuration on appliance

    :param isamAppliance:
    :param cluster_json:
    :return:
    """

    check_obj = {'value': True, 'warnings':""}

    ret_obj = get(isamAppliance)
    check_obj['warnings'] = ret_obj['warnings']
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

    for key, value in temp.items():
        try:
            if isinstance(value, list):
                if ibmsecurity.utilities.tools.json_sort(
                        ret_obj['data'][key] != ibmsecurity.utilities.tools.json_sort(value)):
                    logger.debug(
                        "For key: {0}, values: {1} and {2} do not match.".format(key, value, ret_obj['data'][key]))
                    check_obj['value']=False
                    return check_obj
            else:
                if ret_obj['data'][key] != value:
                    logger.debug(
                        "For key: {0}, values: {1} and {2} do not match.".format(key, value, ret_obj['data'][key]))
                    check_obj['value']=False
                    return check_obj
        except:  # In case there is an error looking up the key in existing configuration (missing)
            logger.debug("Exception processing Key: {0} Value: {1} - missing key in current config?".format(key, value))
            check_obj['value']=False
            return check_obj

    logger.debug("JSON provided already is contained in current appliance configuration.")
    check_obj['value']=True
    return check_obj


def compare(isamAppliance1, isamAppliance2):
    """
    Compare cluster configuration between two appliances
    """

    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
