import logging
import copy
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


def set(isamAppliance,
        hvdb_db_type,
        hvdb_address,
        hvdb_port,
        hvdb_user,
        hvdb_password,
        hvdb_db_name=None,
        hvdb_db_secure=None,
        hvdb_driver_type=None,
        hvdb_db2_alt_address=None,
        hvdb_db2_alt_port=None,
        cfgdb_embedded=True,
        check_mode=False,
        force=False,
        ignore_password_for_idempotency=False,
        **kwargs):
    """
    Set cluster configuration
    hvdb_db_type	String	No	The type of database that is being used. Valid values are db2, postgresql, mssql and oracle.
    hvdb_address	String	No	The IP or hostname of the external database server.
    hvdb_port	    Integer	No	The port on which the external database server is listening.
    hvdb_user	    String	No	The administrator name for the external database.
    hvdb_password	String	No	The administrator password for the external database.
    hvdb_db2_alt_address	String	Yes	The IP or hostname of the fail-over server in DB2 HADR/ACR environments. (Can be specified for DB2 only).
    hvdb_db2_alt_port	    String	Yes	The IP or hostname of the fail-over server in DB2 HADR/ACR environments. (Can be specified for DB2 only).
    hvdb_db_name	String	No	The name of the external database (Required for DB2, PostgreSQL, MSSQL and Oracle).
    hvdb_db_secure	Boolean	No	A flag true/false indicating whether or not the external database is secure. (Required for DB2, PostgreSQL, MSSQL and Oracle).
    hvdb_db_truststore	String	Yes	The SSL Key Store which contains the trusted certificate of the Oracle DB requiring secure connectivity. (Required for Oracle only when hvdb_db_secure is true)
    hvdb_driver_type	String	Yes	The type of Oracle JDBC driver to use. (Required for Oracle only).
    hvdb_failover_servers	FailoverServer[]	Yes	An ordered list of PostgreSQL failover servers for the Runtime database. (Can be specified for PostgreSQL only).
         Note: This is an array of elements.

    - new in 10.0.0.8  configdb (embedded)

    cfgdb_embedded	Boolean	No	A flag true/false indicating whether or not the Configuration database is embedded (true) or external (false). If this value is not specified, the internal database will be used and none of the other cfgdb_* values are required.
    cfgdb_db_type	String	Yes	The type of database that is being used. Valid values are db2, postgresql, mssql and oracle. This option is only valid if cfgdb_embedded is set to false.
    cfgdb_address	String	Yes	The IP or hostname of the external database server. This option is only valid if cfgdb_embedded is set to false.
    cfgdb_port	Integer	Yes	The port on which the external database server is listening. This option is only valid if cfgdb_embedded is set to false.
    cfgdb_user	String	Yes	The administrator name for the external database. This option is only valid if cfgdb_embedded is set to false.
    cfgdb_password	String	Yes	The administrator password for the external database. This option is only valid if cfgdb_embedded is set to false.
    cfgdb_db2_alt_address	String	Yes	The IP or hostname of the fail-over server in DB2 HADR/ACR environments. (Can be specified for DB2 only). This option is only valid if cfgdb_embedded is set to false.
    cfgdb_db2_alt_port	String	Yes	The IP or hostname of the fail-over server in DB2 HADR/ACR environments. (Can be specified for DB2 only). This option is only valid if cfgdb_embedded is set to false.
    cfgdb_db_name	String	Yes	The name of the external database (Required for DB2, PostgreSQL, MSSQL and Oracle). This option is only valid if cfgdb_embedded is set to false.
    cfgdb_db_secure	Boolean	Yes	A flag true/false indicating whether or not the external database is secure. (Required for DB2, PostgreSQL, MSSQL and Oracle). This option is only valid if cfgdb_embedded is set to false.
    cfgdb_db_truststore	String	Yes	The SSL Key Store which contains the trusted certificate of the Oracle DB requiring secure connectivity. (Required for Oracle only when cfgdb_db_secure is true)
    cfgdb_driver_type	String	Yes	The type of Oracle JDBC driver to use. (Required for Oracle only). This option is only valid if cfgdb_embedded is set to false.
    cfgdb_failover_servers	FailoverServer[]	Yes	An ordered list of PostgreSQL failover servers for the Configuration database. (Can be specified for PostgreSQL only).
    Note: This is an array of elements.

    - new in 11 - MSSQL

    hvdb_mssql_instance_name	String	Yes	The database instance name to connect to. When it isn't specified, a connection is made to the default instance. (Can be specified for MSSQL only)
    hvdb_mssql_trust_server_cert	Boolean	No	Set to "true" to specify that the driver doesn't validate the server TLS/SSL certificate. (Can be specified for MSSQL only)
    hvdb_mssql_failover_partner	String	Yes	The name of the failover server used in a database mirroring configuration. This property is used for an initial connection failure to the principal server. After you make the initial connection, this property is ignored. (Can be specified for MSSQL only)

    cfgdb_mssql_instance_name	String	Yes	The database instance name to connect to. When it isn't specified, a connection is made to the default instance. (Can be specified for MSSQL only)
    cfgdb_mssql_trust_server_cert	Boolean	No	Set to "true" to specify that the driver doesn't validate the server TLS/SSL certificate. (Can be specified for MSSQL only)
    cfgdb_mssql_failover_partner	String	Yes	The name of the failover server used in a database mirroring configuration. This property is used for an initial connection failure to the principal server. After you make the initial connection, this property is ignored. (Can be specified for MSSQL only)
    """
    warnings = []
    if hvdb_db_name is None:
        warnings.append(f"hvdb_db_type {hvdb_db_type} requires hvdb_db_name")
        return isamAppliance.create_return_object(warnings=warnings)
    if hvdb_db_secure is None:
        warnings.append(f"hvdb_db_type {hvdb_db_type} requires hvdb_db_secure")
        return isamAppliance.create_return_object(warnings=warnings)
    if hvdb_db_type == "oracle":
        if hvdb_driver_type is None:
            warnings.append(f"hvdb_db_type {hvdb_db_type} requires hvdb_driver_type")
            return isamAppliance.create_return_object(warnings=warnings)
        if hvdb_db_secure and kwargs.get("hvdb_db_truststore", None) is None:
            warnings.append(f"hvdb_db_type {hvdb_db_type} with hvdb_db_secure requires hvdb_db_truststore")
            return isamAppliance.create_return_object(warnings=warnings)
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

    if tools.version_compare(isamAppliance.facts['version'], "10.0.8.0") < 0:
        warnings.append(
                f"Appliance at version: {isamAppliance.facts['version']}, cfgdb_embedded is not supported. Needs 10.0.8.0 or higher. Ignoring for this call.")
    else:
        db_json["cfgdb_embedded"] = cfgdb_embedded

    for k, v in kwargs.items():
        if k.startswith("cfgdb_mssql_"):
            if tools.version_compare(isamAppliance.facts['version'], "10.0.9.0") < 0:
                warnings.append(
                    f"Appliance at version: {isamAppliance.facts['version']}, MSSQL parameters are not supported ({k}). Needs 10.0.8.0 or higher. Ignoring for this call.")
            else:
                db_json[k] = v
            continue
        if k.startswith("hvdb_mssql_"):
            if tools.version_compare(isamAppliance.facts['version'], "10.0.9.0") < 0:
                warnings.append(
                    f"Appliance at version: {isamAppliance.facts['version']}, MSSQL parameters are not supported ({k}). Needs 10.0.8.0 or higher. Ignoring for this call.")
            else:
                db_json[k] = v
            continue
        if k.startswith("cfgdb_"):
            if tools.version_compare(isamAppliance.facts['version'], "10.0.8.0") < 0:
                warnings.append(
                    f"Appliance at version: {isamAppliance.facts['version']}, cfgdb_* parameters are not supported ({k}). Needs 10.0.8.0 or higher. Ignoring for this call.")
            else:
                db_json[k] = v
            continue
        db_json[k] = v

    obj = _check(isamAppliance=isamAppliance, db_json=db_json,
                 ignore_password_for_idempotency=ignore_password_for_idempotency)

    if force or not obj['value']:
        if check_mode:
            return isamAppliance.create_return_object(changed=True, warnings=obj['warnings'])
        else:
            return isamAppliance.invoke_post("Set database configuration", uri, db_json,
                                             requires_modules=requires_modules, requires_version=requires_version,
                                             requires_model=requires_model, warnings=obj['warnings'])

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
    logger.debug(f"Sorted Existing Data:{sorted_ret_obj}")
    logger.debug(f"Sorted Desired  Data:{sorted_json_data}")

    if del_password:
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
