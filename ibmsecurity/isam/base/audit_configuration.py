import logging
from ibmsecurity.utilities import tools

try:
    basestring
except NameError:
    basestring = (str, bytes)

logger = logging.getLogger(__name__)

# URI for this module
uri = "/iam/access/v8/audit"
requires_modules = ["mga", "federation"]
requires_version = None


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieve audit configuration
    """
    return isamAppliance.invoke_get("Retrieve audit configuration", uri, requires_modules=requires_modules,
                                    requires_version=requires_version)


def set(isamAppliance, id, config, enabled=True, type='Syslog', verbose=True, check_mode=False, force=False):
    """
    Update Audit Configuration

    Sample data for Audit Configuration:
    In JSON Format:
    { u'config': [ { u'datatype': u'String',
                     u'key': u'ISAM.Audit.syslogclient.SSL_TRUST_STORE',
                     u'sensitive': False,
                     u'validValues': [],
                     u'value': u''},
                   { u'datatype': u'String',
                     u'key': u'ISAM.Audit.syslogclient.CLIENT_AUTH_KEY',
                     u'sensitive': False,
                     u'validValues': [],
                     u'value': u''},
                   { u'datatype': u'Boolean',
                     u'key': u'ISAM.Audit.syslogclient.FAILOVER_TO_DISK',
                     u'sensitive': False,
                     u'validValues': [],
                     u'value': u'false'},
                   { u'datatype': u'Integer',
                     u'key': u'ISAM.Audit.syslogclient.NUM_RETRY',
                     u'sensitive': False,
                     u'validValues': [],
                     u'value': u'2'},
                   { u'datatype': u'Integer',
                     u'key': u'ISAM.Audit.syslogclient.NUM_SENDER_THREADS',
                     u'sensitive': False,
                     u'validValues': [],
                     u'value': u'1'},
                   { u'datatype': u'Boolean',
                     u'key': u'ISAM.Audit.syslogclient.CLIENT_CERT_AUTH_REQUIRED',
                     u'sensitive': False,
                     u'validValues': [],
                     u'value': u'false'},
                   { u'datatype': u'Integer',
                     u'key': u'ISAM.Audit.syslogclient.SERVER_PORT',
                     u'sensitive': False,
                     u'validValues': [],
                     u'value': u'514'},
                   { u'datatype': u'Hostname',
                     u'key': u'ISAM.Audit.syslogclient.SERVER_HOST',
                     u'sensitive': False,
                     u'validValues': [],
                     u'value': u'127.0.0.1'},
                   { u'datatype': u'String',
                     u'key': u'ISAM.Audit.syslogclient.TRANSPORT',
                     u'sensitive': False,
                     u'validValues': [],
                     u'value': u'TRANSPORT_UDP'},
                   { u'datatype': u'Integer',
                     u'key': u'ISAM.Audit.syslogclient.QUEUE_FULL_TIMEOUT',
                     u'sensitive': False,
                     u'validValues': [],
                     u'value': u'-1'},
                   { u'datatype': u'Integer',
                     u'key': u'ISAM.Audit.syslogclient.MAX_QUEUE_SIZE',
                     u'sensitive': False,
                     u'validValues': [],
                     u'value': u'1000'}],
      u'enabled': False,
      u'id': u'1',
      u'type': u'Syslog',
      u'verbose': False}

    In YAML Format:
    config:
      - datatype: String
        key: ISAM.Audit.syslogclient.SSL_TRUST_STORE
        sensitive: false
        validValues: []
        value: ''
      - datatype: String
        key: ISAM.Audit.syslogclient.CLIENT_AUTH_KEY
        sensitive: false
        validValues: []
        value: ''
      - datatype: Boolean
        key: ISAM.Audit.syslogclient.FAILOVER_TO_DISK
        sensitive: false
        validValues: []
        value: 'false'
      - datatype: Integer
        key: ISAM.Audit.syslogclient.NUM_RETRY
        sensitive: false
        validValues: []
        value: '2'
      - datatype: Integer
        key: ISAM.Audit.syslogclient.NUM_SENDER_THREADS
        sensitive: false
        validValues: []
        value: '1'
      - datatype: Boolean
        key: ISAM.Audit.syslogclient.CLIENT_CERT_AUTH_REQUIRED
        sensitive: false
        validValues: []
        value: 'false'
      - datatype: Integer
        key: ISAM.Audit.syslogclient.SERVER_PORT
        sensitive: false
        validValues: []
        value: '514'
      - datatype: Hostname
        key: ISAM.Audit.syslogclient.SERVER_HOST
        sensitive: false
        validValues: []
        value: 127.0.0.1
      - datatype: String
        key: ISAM.Audit.syslogclient.TRANSPORT
        sensitive: false
        validValues: []
        value: TRANSPORT_UDP
      - datatype: Integer
        key: ISAM.Audit.syslogclient.QUEUE_FULL_TIMEOUT
        sensitive: false
        validValues: []
        value: '-1'
      - datatype: Integer
        key: ISAM.Audit.syslogclient.MAX_QUEUE_SIZE
        sensitive: false
        validValues: []
        value: '1000'
    enabled: false
    id: '1'
    type: Syslog
    verbose: false
    """
    pol_id, update_required, json_data = _check(isamAppliance, id, config, enabled, type, verbose)
    if pol_id is None:
        from ibmsecurity.appliance.ibmappliance import IBMError
        raise IBMError("999", "Cannot update data for unknown Audit Configuration ID: {0}".format(id))

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Update Audit Configuration",
                "{0}/{1}".format(uri, id), json_data, requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object()


def _check(isamAppliance, id, config, enabled, type, verbose):
    """
    Check and return True if update needed
    """
    update_required = False
    pol_id = None
    # convert all values into string - any other type causes issues
    for cfg in config:
        if isinstance(cfg['value'], bool):
            cfg['value'] = str(cfg['value']).lower()
        else:
            cfg['value'] = str(cfg['value'])
    # Ensure boolean variables are set correctly
    if isinstance(verbose, basestring):
        if verbose.lower() == "true":
            verbose = True
        else:
            verbose = False
    if isinstance(enabled, basestring):
        if enabled.lower() == "true":
            enabled = True
        else:
            enabled = False
    json_data = {
        "id": id,
        "config": config,
        "enabled": enabled,
        "type": type,
        "verbose": verbose
    }
    ret_obj = get(isamAppliance)
    for aud_cfg in ret_obj['data']:
        if id == aud_cfg['id']:
            pol_id = id
            break
    if pol_id is None:
        logger.warning("Audit Configuration not found, returning no update required.")
        return pol_id, update_required, json_data
    else:
        import ibmsecurity.utilities.tools
        sorted_json_data = ibmsecurity.utilities.tools.json_sort(json_data)
        logger.debug("Sorted input: {0}".format(sorted_json_data))
        sorted_ret_obj = ibmsecurity.utilities.tools.json_sort(aud_cfg)
        logger.debug("Sorted existing data: {0}".format(sorted_ret_obj))
        if sorted_ret_obj != sorted_json_data:
            logger.info("Changes detected, update needed.")
            update_required = True

    return pol_id, update_required, json_data


def compare(isamAppliance1, isamAppliance2):
    """
    Compare Audit Configuration between two appliances
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    for obj in ret_obj1['data']:
        del obj['id']
    for obj in ret_obj2['data']:
        del obj['id']

    return tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['id'])
