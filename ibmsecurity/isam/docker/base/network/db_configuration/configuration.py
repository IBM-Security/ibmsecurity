import logging
import copy
import ibmsecurity.utilities.tools
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

uri = "/isam/cluster/v2"
requires_modules = None
requires_version = None
requires_model = "Docker"

try:
    basestring
except NameError:
    basestring = (str, bytes)


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieve the current database configuration
    """
    return isamAppliance.invoke_get("Retrieve the current database configuration", uri,
                                    requires_modules=requires_modules, requires_version=requires_version,
                                    requires_model=requires_model)


def set(isamAppliance, hvdb_db_type, hvdb_address, hvdb_port, hvdb_user, hvdb_password, hvdb_db_name=None,
        hvdb_db_secure=None, hvdb_driver_type=None, hvdb_db2_alt_address=None, hvdb_db2_alt_port=None,
        hvdb_solid_tc=None, check_mode=False, force=False):
    """
    Set cluster configuration
    """

    if isamAppliance.facts['model'] != "Docker":
        return isamAppliance.create_return_object(
            warnings="API invoked requires model: {0}, appliance is of deployment model: {1}.".format(
                requires_model, isamAppliance.facts['model']))

    if hvdb_db_type != "soliddb":
        if hvdb_db_name is None:
            return isamAppliance.create_return_object(
                warnings="hvdb_db_type {0} requires hvdb_db_name".format(hvdb_db_type))
        if hvdb_db_secure is None:
            return isamAppliance.create_return_object(
                warnings="hvdb_db_type {0} requires hvdb_db_secure".format(hvdb_db_type))

    if hvdb_db_type == "oracle":
        if hvdb_driver_type is None:
            return isamAppliance.create_return_object(
                warnings="hvdb_db_type {0} requires hvdb_driver_type".format(hvdb_db_type))

    if isinstance(hvdb_port, basestring):
        hvdb_port = int(hvdb_port)

    warnings = []
    # Create a simple json with just the main client attributes
    db_json = {
        "hvdb_db_type": hvdb_db_type,
        "hvdb_address": hvdb_address,
        "hvdb_port": hvdb_port,
        "hvdb_user": hvdb_user,
        "hvdb_password": hvdb_password
    }
    # Add attributes that have been supplied... otherwise skip them.

    if hvdb_db2_alt_address is not None:
        db_json["hvdb_db2_alt_address"] = hvdb_db2_alt_address
    if hvdb_db2_alt_port is not None:
        db_json["hvdb_db2_alt_port"] = hvdb_db2_alt_port
    if hvdb_db_name is not None:
        db_json["hvdb_db_name"] = hvdb_db_name
    if hvdb_db_secure is not None:
        db_json["hvdb_db_secure"] = hvdb_db_secure
    if hvdb_driver_type is not None:
        db_json["hvdb_driver_type"] = hvdb_driver_type
    if hvdb_solid_tc is not None:
        if (isinstance(hvdb_solid_tc, basestring)):
            import ast
            hvdb_solid_tc = ast.literal_eval(hvdb_solid_tc)
        db_json["hvdb_solid_tc"] = hvdb_solid_tc

    if force is True or _check(isamAppliance, db_json) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_post("Set database configuration", uri, db_json,
                                             requires_modules=requires_modules, requires_version=requires_version,
                                             requires_model=requires_model,
                                             warnings=warnings)

    return isamAppliance.create_return_object(warnings=warnings)


def _check(isamAppliance, db_json):
    """
    Check if provided json values match the configuration on appliance

    :param isamAppliance:
    :param db_json:
    :return:
    """

    if isamAppliance.facts['model'] != "Docker":
        return isamAppliance.create_return_object(
            warnings="API invoked requires model: {0}, appliance is of deployment model: {1}.".format(
                requires_model, isamAppliance.facts['model']))

    ret_obj = get(isamAppliance)
    sorted_ret_obj = tools.json_sort(ret_obj['data'])
    sorted_json_data = tools.json_sort(db_json)
    logger.debug("Sorted Existing Data:{0}".format(sorted_ret_obj))
    logger.debug("Sorted Desired  Data:{0}".format(sorted_json_data))

    temp = copy.deepcopy(
        db_json)  # deep copy neccessary: otherwise password parameter would be removed from desired config dict 'db_json'. Comparison is done with temp<>ret_obj object
    for idx, x in enumerate(db_json):
        if "password" in x:
            logger.debug("Ignoring JSON password entry: '{0}' to satisfy idempotency.".format(x))
            del temp[x]
    logger.debug("Passwordless JSON to Apply: {0}".format(temp))

    for key, value in temp.items():
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

    if isamAppliance1.facts['model'] != "Docker":
        return isamAppliance1.create_return_object(
            warnings="API invoked requires model: {0}, appliance1 is of deployment model: {1}.".format(
                requires_model, isamAppliance1.facts['model']))

    if isamAppliance2.facts['model'] != "Docker":
        return isamAppliance2.create_return_object(
            warnings="API invoked requires model: {0}, appliance2 is of deployment model: {1}.".format(
                requires_model, isamAppliance2.facts['model']))

    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
