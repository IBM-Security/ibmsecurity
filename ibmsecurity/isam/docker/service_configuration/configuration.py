import logging
import ibmsecurity.utilities.tools

try:
    basestring
except NameError:
    basestring = (str, bytes)

logger = logging.getLogger(__name__)

uri = "/isam/cluster/v2"
requires_modules = None
requires_version = "9.0.4.0"


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieve the current service configuration
    """
    return isamAppliance.invoke_get("Retrieve the current service configuration", uri,
                                    requires_modules=requires_modules, requires_version=requires_version)


def set(isamAppliance, hvdb_db_type=None, hvdb_address=None, hvdb_port=None, hvdb_user=None,
        hvdb_password=None, hvdb_db2_alt_address=None, hvdb_db2_alt_port=None, hvdb_db_name=None, hvdb_db_secure=None,
        hvdb_driver_type=None, hvdb_solid_tc=None, check_mode=False, force=False):
    """
    Set service configuration
    """
    warnings = []
    # Create a simple json with just the main client attributes
    service_json = {}
    # Add attributes that have been supplied... otherwise skip them.
    if hvdb_db_type is not None:
        service_json["hvdb_db_type"] = hvdb_db_type
    if hvdb_address is not None:
        service_json["hvdb_address"] = hvdb_address
    if hvdb_port is not None:
        service_json["hvdb_port"] = hvdb_port
    if hvdb_user is not None:
        service_json["hvdb_user"] = hvdb_user
    if hvdb_password is not None:
        warnings.append("Since existing hvdb_password cannot be read - this call will not be idempotent.")
        service_json["hvdb_password"] = hvdb_password
    if hvdb_db2_alt_address is not None:
        service_json["hvdb_db2_alt_address"] = hvdb_db2_alt_address
    if hvdb_db2_alt_port is not None:
        service_json["hvdb_db2_alt_port"] = hvdb_db2_alt_port
    if hvdb_db_name is not None:
        service_json["hvdb_db_name"] = hvdb_db_name
    if hvdb_db_secure is not None:
        service_json["hvdb_db_secure"] = hvdb_db_secure
    if hvdb_driver_type is not None:
        service_json["hvdb_driver_type"] = hvdb_driver_type
    if hvdb_solid_tc is not None:
        if (isinstance(hvdb_solid_tc, basestring)):
            import ast
            hvdb_solid_tc = ast.literal_eval(hvdb_solid_tc)
            service_json["hvdb_solid_tc"] = hvdb_solid_tc

    if force is True or _check(isamAppliance, service_json) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post("Set service configuration", uri, service_json,
                                             requires_modules=requires_modules, requires_version=requires_version,
                                             warnings=warnings)

    return isamAppliance.create_return_object()


def _check(isamAppliance, service_json):
    """
    Check if provided json values match the configuration on appliance

    :param isamAppliance:
    :param service_json:
    :return:
    """
    ret_obj = get(isamAppliance)
    logger.debug("Appliance current configuration: {0}".format(ret_obj['data']))
    logger.debug("JSON to Apply: {0}".format(service_json))

    for key, value in service_json.items():
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
    Compare service configuration between two containers
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
