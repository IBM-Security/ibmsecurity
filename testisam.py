import logging.config
import pprint
from ibmsecurity.appliance.isamappliance import ISAMAppliance
from ibmsecurity.user.applianceuser import ApplianceUser
import pkgutil
import importlib


def import_submodules(package, recursive=True):
    """
    Import all submodules of a module, recursively, including subpackages

    :param package: package (name or actual module)
    :type package: str | module
    :rtype: dict[str, types.ModuleType]
    """
    if isinstance(package, str):
        package = importlib.import_module(package)
    results = {}
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + '.' + name
        results[full_name] = importlib.import_module(full_name)
        if recursive and is_pkg:
            results.update(import_submodules(full_name))
    return results


import ibmsecurity

# Import all packages within ibmsecurity - recursively
# Note: Advisable to replace this code with specific imports for production code
import_submodules(ibmsecurity)

# Setup logging to send to stdout, format and set log level
# logging.getLogger(__name__).addHandler(logging.NullHandler())
logging.basicConfig()
# Valid values are 'DEBUG', 'INFO', 'ERROR', 'CRITICAL'
logLevel = 'DEBUG'
DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] [PID:%(process)d TID:%(thread)d] [%(levelname)s] [%(name)s] [%(funcName)s():%(lineno)s] %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': logLevel,
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'level': logLevel,
            'handlers': ['default'],
            'propagate': True
        },
        'requests.packages.urllib3.connectionpool': {
            'level': 'ERROR',
            'handlers': ['default'],
            'propagate': True
        }
    }
}
logging.config.dictConfig(DEFAULT_LOGGING)


# Function to pretty print JSON data
def p(jdata):
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(jdata)


if __name__ == "__main__":
    """
    This test program should not execute when imported, which would otherwise
    cause problems when generating the documentation.
    """
    # Create a user credential for ISAM appliance
    u = ApplianceUser(username="admin@local", password="Passw0rd")
    # Create an ISAM appliance with above credential
    isam_server = ISAMAppliance(hostname="192.168.42.111", user=u, lmi_port=443)
    #isam_server = ISAMAppliance(hostname="192.168.42.141", user=u, lmi_port=443)

    filePath = "isam_runtime/policy_server/msg__pdmgrd.log"

    #p(ibmsecurity.isam.web.authorization_server.configuration.entry.update(isamAppliance=isam_server, id='as1', stanza_id='manager', entry_name_id='', value_id=''))
    #p(ibmsecurity.isam.web.authorization_server.configuration.entry.set(isamAppliance=isam_server, id='as1', stanza_id='manager', entries=[]))
    #p(ibmsecurity.isam.web.authorization_server.configuration.entry.add(isamAppliance=isam_server, id='as1', stanza_id='manager', entries=[]))
    #p(ibmsecurity.isam.web.authorization_server.configuration.entry.delete(isamAppliance=isam_server, id='as1', stanza_id='ldap', entry_id='ssl-port', value_id='636', check_mode=True))
    #p(ibmsecurity.isam.web.authorization_server.configuration.entry.delete_all(isamAppliance=isam_server, id='as1', stanza_id='ldap', entry_id='ssl-port', check_mode=True))
    #p(ibmsecurity.isam.web.authorization_server.configuration.entry.get(isamAppliance=isam_server, id='as1', stanza_id='ldap', entry_id='ssl-port'))
    #p(ibmsecurity.isam.web.authorization_server.configuration.entry.get_all(isamAppliance=isam_server, id='as1', stanza_id='ldap'))

    #p(ibmsecurity.isam.web.authorization_server.configuration.stanza.add(isamAppliance=isam_server, id='as1', stanza_id='manager', check_mode=True))
    #p(ibmsecurity.isam.web.authorization_server.configuration.stanza.delete(isamAppliance=isam_server, id='as1', stanza_id='manager', check_mode=True))
    #p(ibmsecurity.isam.web.authorization_server.configuration.stanza.get(isamAppliance=isam_server, id='as1'))

    #p(ibmsecurity.isam.web.authorization_server.instance.execute(isamAppliance=isam_server, id='as1', admin_pwd='Passw0rd', check_mode=True))
    #p(ibmsecurity.isam.web.authorization_server.instance.delete(isamAppliance=isam_server, id='as1', admin_pwd='Passw0rd', check_mode=True))
    #p(ibmsecurity.isam.web.authorization_server.instance.add(isamAppliance=isam_server, inst_name='as1', admin_pwd='Passw0rd', addresses='192.168.42.123'))
    #p(ibmsecurity.isam.web.authorization_server.instance.get(isamAppliance=isam_server))

    #p(ibmsecurity.isam.web.authorization_server.trace.update(isamAppliance=isam_server, id='as1', trace_id='pd.acl', trace_file_id='test.log'))
    #p(ibmsecurity.isam.web.authorization_server.trace.export_file(isamAppliance=isam_server, id='as1', trace_id='pd.acl', trace_file_id='test.log', filepath='Seshu.log'))
    #p(ibmsecurity.isam.web.authorization_server.trace.delete(isamAppliance=isam_server, id='as1', trace_id='pd.acl', trace_file_id='test.log'))
    #p(ibmsecurity.isam.web.authorization_server.trace.get(isamAppliance=isam_server, id='as1', trace_id='pd.acl', trace_file_id='test.log'))
    #p(ibmsecurity.isam.web.authorization_server.trace.get_list(isamAppliance=isam_server, id='as1', trace_id='pd.acl'))
    #p(ibmsecurity.isam.web.authorization_server.trace.get_all(isamAppliance=isam_server, id='as1'))

    #p(ibmsecurity.isam.web.authorization_server.logs.delete(isamAppliance=isam_server, id='as1', file_id='as1-PDAcld_config_start.log', check_mode=True))
    #p(ibmsecurity.isam.web.authorization_server.logs.get(isamAppliance=isam_server, id='as1', file_id='as1-PDAcld_config_start.log'))
    #p(ibmsecurity.isam.web.authorization_server.logs.get_all(isamAppliance=isam_server, id='as1'))

    #p(ibmsecurity.isam.web.reverse_proxy.trace.get_all(isamAppliance=isam_server, instance_id='rp1'))
    #p(ibmsecurity.isam.base.cluster.log.get_all(isamAppliance=isam_server))

    #p(ibmsecurity.isam.web.rsa_securid_config.upload(isamAppliance=isam_server, filename=filePath))
    #p(ibmsecurity.isam.web.rsa_securid_config.delete(isamAppliance=isam_server, check_mode=True))
    #p(ibmsecurity.isam.web.rsa_securid_config.clear(isamAppliance=isam_server, check_mode=True))
    #p(ibmsecurity.isam.web.rsa_securid_config.get(isamAppliance=isam_server))

    #p(ibmsecurity.isam.web.reverse_proxy.common_logs.get_all(isamAppliance=isam_server))
    #p(ibmsecurity.isam.web.reverse_proxy.common_logs.get(isamAppliance=isam_server, file_id='msg__amweb_config.log'))
    #p(ibmsecurity.isam.web.reverse_proxy.common_logs.delete(isamAppliance=isam_server, file_id='msg__amweb_config.log', check_mode=True))
    #p(ibmsecurity.isam.web.reverse_proxy.logs.get_all(isamAppliance=isam_server, instance_id='rp1'))
    #p(ibmsecurity.isam.web.reverse_proxy.logs.get(isamAppliance=isam_server, instance_id='rp1', file_id='msg__webseald-rp1.log'))
    #p(ibmsecurity.isam.web.reverse_proxy.logs.delete(isamAppliance=isam_server, instance_id='rp1', file_id='msg__webseald-rp1.log', check_mode=True))
    #p(ibmsecurity.isam.web.reverse_proxy.logs.export_file(isamAppliance=isam_server, instance_id='rp1', file_id='msg__webseald-rp1.log', filename='seshu2.log'))
    #p(ibmsecurity.isam.application_logs.get_all(isamAppliance=isam_server, file_path='isam_runtime/policy_server', flat_details='yes'))
    #p(ibmsecurity.isam.application_logs.clear(isamAppliance=isam_server, file_id=filePath))
    #p(ibmsecurity.isam.application_logs.get(isamAppliance=isam_server, file_id=filePath))
    # Get the current SNMP monitoring setup details
    #p(ibmsecurity.isam.base.snmp_monitoring.get(isamAppliance=isam_server))
    # Set the V2 SNMP monitoring
    #p(ibmsecurity.isam.base.snmp_monitoring.set_v1v2(isamAppliance=isam_server, community="IBM"))
    # Commit or Deploy the changes
    #p(ibmsecurity.isam.appliance.commit(isamAppliance=isam_server))
