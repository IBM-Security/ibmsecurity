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
        hvdb_solid_tc=None, check_mode=False, force=False, ignore_password_for_idempotency=False):
    """
    Set cluster configuration
    """

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

    obj = _check(isamAppliance=isamAppliance, db_json=db_json,
                 ignore_password_for_idempotency=ignore_password_for_idempotency)

    if force is True or obj['value'] is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=obj['warnings'])
        else:
            return isamAppliance.invoke_post("Set database configuration", uri, db_json,
                                             requires_modules=requires_modules, requires_version=requires_version,
                                             requires_model=requires_model)

    return isamAppliance.create_return_object(warnings=obj['warnings'])


def _check(isamAppliance, db_json, ignore_password_for_idempotency=False):
    """
    Check if provided json values match the configuration on appliance

    :param isamAppliance:
    :param db_json:
    :return:
    """

    obj = {'value': True, 'warnings': ""}

    ret_obj = get(isamAppliance)

    obj['warnings'] = ret_obj['warnings']
    del_password = False

    if ignore_password_for_idempotency is True:
        if 'hvdb_password' in ret_obj['data']:
            del ret_obj['data']['hvdb_password']
        if 'hvdb_password' in db_json:
            password = db_json['hvdb_password']
            del_password = True
            del db_json['hvdb_password']

    sorted_ret_obj = tools.json_sort(ret_obj['data'])
    sorted_json_data = tools.json_sort(db_json)
    logger.debug("Sorted Existing Data:{0}".format(sorted_ret_obj))
    logger.debug("Sorted Desired  Data:{0}".format(sorted_json_data))

    if del_password is True:
        db_json['hvdb_password'] = password

    if sorted_ret_obj != sorted_json_data:
        obj['value'] = False
        return obj
    else:
        obj['value'] = True
        return obj


def compare(isamAppliance1, isamAppliance2):
    """
    Compare cluster configuration between two appliances
    """

    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
