import logging
import copy
import json
from ibmsecurity.utilities.tools import version_compare
from ibmsecurity.utilities.tools import json_compare
from ibmsecurity.utilities.tools import jsonSortedListEncoder

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
       cfgdb_fs=None, dsc_trace_level=None, cfgdb_db_truststore=None,
       dsc_connection_idle_timeout=None, hvdb_failover_servers=None, cfgdb_failover_servers=None, hvdb_db_truststore=None,
       ignore_password_for_idempotency=False, check_mode=False, force=False):
    """
    Set cluster configuration
    """

    warnings = []
    # Create a simple json with just the main client attributes
    cluster_json = {
        "primary_master": primary_master,
        "dsc_external_clients": bool(dsc_external_clients),
        "dsc_worker_threads": int(dsc_worker_threads),
        "dsc_maximum_session_lifetime": int(dsc_maximum_session_lifetime),
        "dsc_client_grace_period": int(dsc_client_grace_period),
        "hvdb_embedded": bool(hvdb_embedded),
        "cfgdb_embedded": bool(cfgdb_embedded),
        "first_port": int(first_port)
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
        cluster_json["dsc_port"] = int(dsc_port)
    if dsc_use_ssl is not None:
        cluster_json["dsc_use_ssl"] = bool(dsc_use_ssl)
    if dsc_ssl_keyfile is not None:
        cluster_json["dsc_ssl_keyfile"] = dsc_ssl_keyfile
    if dsc_ssl_label is not None:
        cluster_json["dsc_ssl_label"] = dsc_ssl_label
    if dsc_connection_idle_timeout is not None:
        cluster_json["dsc_connection_idle_timeout"] = int(dsc_connection_idle_timeout)
    if hvdb_max_size is not None and hvdb_embedded:
        cluster_json["hvdb_max_size"] = int(hvdb_max_size)
    if hvdb_db_type is not None:
        cluster_json["hvdb_db_type"] = hvdb_db_type
    if hvdb_address is not None:
        cluster_json["hvdb_address"] = hvdb_address
    if hvdb_port is not None:
        cluster_json["hvdb_port"] = int(hvdb_port)
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
        cluster_json["hvdb_db2_alt_port"] = int(hvdb_db2_alt_port)
    if hvdb_db_name is not None:
        cluster_json["hvdb_db_name"] = hvdb_db_name
    if hvdb_db_secure is not None:
        cluster_json["hvdb_db_secure"] = bool(hvdb_db_secure)
    if hvdb_driver_type is not None and hvdb_db_type == "oracle":
        #Oracle only
        cluster_json["hvdb_driver_type"] = hvdb_driver_type
    if hvdb_solid_tc is not None:
        if isinstance(hvdb_solid_tc, basestring):
            import ast
            hvdb_solid_tc = ast.literal_eval(hvdb_solid_tc)
        cluster_json["hvdb_solid_tc"] = hvdb_solid_tc
    if hvdb_db_truststore is not None and hvdb_db_truststore != "":
        cluster_json["hvdb_db_truststore"] = hvdb_db_truststore
    if hvdb_failover_servers is not None:
        #Only if the db_type is Postgresql.  This is an array [{"address": "postgresql2.domain.com", "port": 5432, "order": 0}]
        if hvdb_db_type is not None and hvdb_db_type == "postgresql":
            cluster_json["hvdb_failover_servers"] = hvdb_failover_servers
    if cfgdb_failover_servers is not None:
        #Only if the dbtype isPostgresql.  This is an array [{"address": "postgresql2.domain.com", "port": 5432, "order": 0}]
        if cfgdb_db_type is not None and cfgdb_db_type == "postgresql":
            cluster_json["cfgdb_failover_servers"] = cfgdb_failover_servers
    if cfgdb_db_type is not None:
        cluster_json["cfgdb_db_type"] = cfgdb_db_type
    if cfgdb_address is not None:
        cluster_json["cfgdb_address"] = cfgdb_address
    if cfgdb_port is not None:
        cluster_json["cfgdb_port"] = int(cfgdb_port)
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
        cluster_json["cfgdb_db2_alt_port"] = int(cfgdb_db2_alt_port)
    if cfgdb_db_name is not None:
        cluster_json["cfgdb_db_name"] = cfgdb_db_name
    if cfgdb_db_secure is not None:
        cluster_json["cfgdb_db_secure"] = bool(cfgdb_db_secure)
    if cfgdb_driver_type is not None and cfgdb_db_type == "oracle":
        cluster_json["cfgdb_driver_type"] = cfgdb_driver_type
    if cfgdb_solid_tc is not None:
        if isinstance(cfgdb_solid_tc, basestring):
            import ast
            cfgdb_solid_tc = ast.literal_eval(cfgdb_solid_tc)
        cluster_json["cfgdb_solid_tc"] = cfgdb_solid_tc
    if cfgdb_fs is not None:
        if ibmsecurity.utilities.tools.version_compare(isamAppliance.facts['version'], "9.0.2.0") < 0:
            warnings.append(
                f"Appliance at version: {isamAppliance.facts['version']}, cfgdb_fs: {cfgdb_fs} is not supported. Needs 9.0.2.0 or higher. Ignoring cfgdb_fs for this call.")
        else:
            cluster_json["cfgdb_fs"] = cfgdb_fs
    if cfgdb_db_truststore is not None and cfgdb_db_truststore != "":
        cluster_json["cfgdb_db_truststore"] = cfgdb_db_truststore
    if dsc_trace_level is not None:
        cluster_json["dsc_trace_level"] = dsc_trace_level

    check_obj =  _check(isamAppliance, cluster_json, ignore_password_for_idempotency)
    if check_obj['warnings'] != []:
        warnings.append(check_obj['warnings'][0])

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

    if ignore_password_for_idempotency:
        temp = copy.deepcopy(
            cluster_json)  # deep copy necessary: otherwise password parameter would be removed from desired config dict 'cluster_json'. Comparison is done
        if 'hvdb_password' in temp:
            del temp["hvdb_password"]
        if 'cfgdb_password' in temp:
            del temp["cfgdb_password"]
        logger.debug(f"Passwordless JSON to Apply: {temp}")
    else:
        temp = cluster_json

    #only compare the keys that are in cluster_json, ignore the rest
    #  note that this may yield false comparison results if you remove parameters from your input
    temp_retobj = {}
    for key, value in ret_obj['data'].items():
        if key in temp:
            temp_retobj[key] = value
        else:
            logger.debug(f"Ignoring {key}")

    sorted_ret_obj = json.dumps(temp_retobj, skipkeys=True, sort_keys=True)
    sorted_json_data = json.dumps(temp, skipkeys=True, sort_keys=True)

    logger.debug(f"Sorted Existing Data:{sorted_ret_obj}")
    logger.debug(f"Sorted Desired  Data:{sorted_json_data}")

    if sorted_ret_obj == sorted_json_data:
        logger.debug("JSON provided already is contained in current appliance configuration.")
        check_obj['value'] = True
    else:
        check_obj['value'] = False
    return check_obj


def compare(isamAppliance1, isamAppliance2):
    """
    Compare cluster configuration between two appliances
    """

    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
