import logging.config
import pprint
from ibmsecurity.appliance.isdsappliance import ISDSAppliance
from ibmsecurity.user.isdsapplianceuser import ISDSApplianceUser
import pkgutil
import importlib
import yaml
import json


def import_submodules(package, recursive=True):
    """ Import all submodules of a module, recursively, including subpackages

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

# Import all packages within ibmsecurity!!!
import_submodules(ibmsecurity)

# logging.getLogger(__name__).addHandler(logging.NullHandler())
logging.basicConfig()
# Setup logging to send to stdout, format and set log level
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


def p(jdata):
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(jdata)
    print(yaml.safe_dump(jdata, encoding='utf-8', allow_unicode=True))


u = ISDSApplianceUser(username="admin", password="admin")
# isds_server = ISDSAppliance(hostname="isds8otech", user=u, lmi_port=443)
isds_server = ISDSAppliance(hostname="isds81dz", user=u, lmi_port=443)
isds_server2 = ISDSAppliance(hostname="isds8otech", user=u, lmi_port=443)

################ ACTIVE TEST ################
p(ibmsecurity.isds.snapshots.apply(isdsAppliance=isds_server, id="24b4b8f1f71bd6b5a07e0e2cc43e93db"))
################ ACTIVE TEST ################

#
# Successfully tested
#
# Any changes needed to the isam code that this is based on is documented,
# or new functions added that will flow to the isam code;
# see lines starting with "Note:".
#
# Lines starting with "TBD:" are work not done yet.
#
####
#
# APPLIANCE.PY
#
# p(ibmsecurity.isds.appliance.shutdown(isdsAppliance=isds_server))
# p(ibmsecurity.isds.appliance.reboot(isdsAppliance=isds_server))
# p(ibmsecurity.isds.firmware.swap(isdsAppliance=isds_server))
# Note: changed method from PUT to GET 
# Note: changed URI
# Note: disabled check for pending changes (not supported)
# p(ibmsecurity.isds.appliance.commit(isdsAppliance=isds_server))
# Note: changed method from DELETE to GET 
# Note: changed URI
# p(ibmsecurity.isds.appliance.rollback(isdsAppliance=isds_server))
# Note: dsabled check for pending changes (not supported)
# p(ibmsecurity.isds.appliance.commit_and_restart(isdsAppliance=isds_server))
#
# FIRMWARE.PY
#
# p(ibmsecurity.isds.firmware.get(isdsAppliance=isds_server))
# p(ibmsecurity.isds.firmware.set(isdsAppliance=isds_server, id="1", comment="NEW COMMENT"))
# p(ibmsecurity.isds.firmware.backup(isdsAppliance=isds_server))
# p(ibmsecurity.isds.firmware.swap(isdsAppliance=isds_server))
#
# SNAPSHOTS.PY
#
# p(ibmsecurity.isds.snapshots.get(isdsAppliance=isds_server))
# p(ibmsecurity.isds.snapshots.create(isdsAppliance=isds_server, comment="COMMENT"))
# p(ibmsecurity.isds.snapshots.delete(isdsAppliance=isds_server, id="82a69dda50c51854db1d83d80100267e"))
# p(ibmsecurity.isds.snapshots.download(isdsAppliance=isds_server, filename="jeff.zip", id="f908e2f7ec4a3e1cb60ca7fc8bfa24fd"))
# p(ibmsecurity.isds.snapshots.download_latest(isdsAppliance=isds_server))
# p(ibmsecurity.isds.snapshots.modify(isdsAppliance=isds_server, id="f908e2f7ec4a3e1cb60ca7fc8bfa24fd", comment="NEW COMMENT"))
# p(ibmsecurity.isds.snapshots.upload(isdsAppliance=isds_server, filename="jeff.zip"))
# TBD: p(ibmsecurity.isds.snapshots.apply - needs authentication token
#
# SUPPORT.PY
#
# p(ibmsecurity.isds.support.get(isdsAppliance=isds_server))
# p(ibmsecurity.isds.support.create(isdsAppliance=isds_server, comment="SECOND SUPPORT FILE COMMENT"))
# p(ibmsecurity.isds.support.delete(isdsAppliance=isds_server, id="9a885478de0b3d53d8d9cd437683bd5d"))
# p(ibmsecurity.isds.support.download(isdsAppliance=isds_server, filename="jeff.zip", id="9a885478de0b3d53d8d9cd437683bd5d"))
# p(ibmsecurity.isds.support.download_latest(isdsAppliance=isds_server))
# Note: REST API documentation says modify should require 4 arguments 
# p(ibmsecurity.isds.support.modify(isdsAppliance=isds_server, id="9a885478de0b3d53d8d9cd437683bd5d", filename="", comment="NEW COMMENT"))
#
# HOST_RECORDS.PY
#
# p(ibmsecurity.isds.host_records.get(isdsAppliance=isds_server))
# p(ibmsecurity.isds.host_records.set(isdsAppliance=isds_server, hostname="jeff", ip_addr="192.168.203.159"))
# p(ibmsecurity.isds.host_records.delete(isdsAppliance=isds_server, hostname="jeff", ip_addr="192.168.203.159"))
#
# DATE_TIME.PY
#
# p(ibmsecurity.isds.date_time.get(isdsAppliance=isds_server))
# p(ibmsecurity.isds.date_time.set(isdsAppliance=isds_server, ntpServers="host1,host2", timeZone="America/Phoenix"))
# p(ibmsecurity.isds.date_time.disable(isdsAppliance=isds_server))
# p(ibmsecurity.isds.date_time.compare(isdsAppliance1=isds_server, isdsAppliance2=isds_server2))
#
# SNMP_MONITORING.PY
#
# Note: changed URI
# p(ibmsecurity.isds.snmp_monitoring.get(isdsAppliance=isds_server))
# Note: changed URI
# p(ibmsecurity.isds.snmp_monitoring.disable(isdsAppliance=isds_server))
# Note: changed URI
# p(ibmsecurity.isds.snmp_monitoring.set_v1v2(isdsAppliance=isds_server, community="JLD"))
# Note: New function
# Note: Code changes to detect if snmpv1v2c or snmpv3 set or not (duplicated in ISAM version)
# p(ibmsecurity.isds.snmp_monitoring.set_v3(isdsAppliance=isds_server, securityLevel="authPriv", securityUser="JDEMENT", authPassword="passw0rd", authProtocol="SHA", privacyPassword="passw0rd", privacyProtocol="CBC-DES"))
#
# STATISTICS.PY`
#
# Note: changed URI
# Note: inconsistency between working code and documentation - had to remove ".json" from URI
# p(ibmsecurity.isds.statistics.get_cpu(isdsAppliance=isds_server, statistics_duration="1d"))
# Note: changed URI
# Note: inconsistency between working code and documentation - had to remove ".json" from URI
# p(ibmsecurity.isds.statistics.get_memory(isdsAppliance=isds_server, statistics_duration="1d"))
# Note: changed URI
# Note: inconsistency between working code and documentation - had to remove ".json" from URI
# p(ibmsecurity.isds.statistics.get_storage(isdsAppliance=isds_server, statistics_duration="1d"))
# Note: changed URI
# Note: inconsistency between working code and documentation - had to remove ".json" from URI
# p(ibmsecurity.isds.statistics.get_network(isdsAppliance=isds_server, application_interface="M.1", statistics_duration="1d"))
#
# FIXPACK.PY
#
# p(ibmsecurity.isds.fixpack.get(isdsAppliance=isds_server))
# Note: New function
# p(ibmsecurity.isds.fixpack.getfips(isdsAppliance=isds_server))
# Note: _check logic sort of working) - needs more work
# Note: worked without "authentication token"
# p(ibmsecurity.isds.fixpack.install(isdsAppliance=isds_server, file="8.0.1.0-ISS-ISDS-IF0003.fixpack"))
# p(ibmsecurity.isds.fixpack.compare(isdsAppliance1=isds_server, isdsAppliance2=isds_server2"))
#
# INTERFACES.PY
#
# Note: changed URI
# p(ibmsecurity.isds.fixpack.get_all(isdsAppliance=isds_server))
# Note: New function
# p(ibmsecurity.isds.interfaces.get_all_app(isdsAppliance=isds_server))
# Note: changed URI
# p(ibmsecurity.isds.interfaces.get(isdsAppliance=isds_server, uuid=P.1))
# p(ibmsecurity.isds.interfaces.compare(isdsAppliance1=isds_server, isdsAppliance2=isds_server2))
#
# CONFIG.PY (NEW)
#
# p(ibmsecurity.isds.config.get(isdsAppliance=isds_server))
# p(ibmsecurity.isds.config.set(isdsAppliance=isds_server, serverType="RDBM"))
# p(ibmsecurity.isds.config.set(isdsAppliance=isds_server, serverType="PROXY"))
# p(ibmsecurity.isds.config.set(isdsAppliance=isds_server, serverType="VD"))
# p(ibmsecurity.isds.date_time.compare(isdsAppliance1=isds_server, isdsAppliance2=isds_server2))
#
# SERVER.PY (NEW)
#
# p(ibmsecurity.isds.server.start(...)
# p(ibmsecurity.isds.server.startconfig(...)
# p(ibmsecurity.isds.server.stop(...)
# p(ibmsecurity.isds.server.restart(...)
# p(ibmsecurity.isds.server.stop(isdsAppliance=isds_server, serverID="directoryserver"))
# p(ibmsecurity.isds.server.stop(isdsAppliance=isds_server, serverID="directoryadminserver"))
# p(ibmsecurity.isds.server.stop(isdsAppliance=isds_server, serverID="directorywat"))
# p(ibmsecurity.isds.server.stop(isdsAppliance=isds_server, serverID="directoryintegrator"))
# p(ibmsecurity.isds.server.stop(isdsAppliance=isds_server, serverID="directoryintegratorscimtarget"))
# p(ibmsecurity.isds.server.stop(isdsAppliance=isds_server, serverID="scimservice"))
#
# LOGS.PY (NEW)
#
# p(ibmsecurity.isds.logs.get_event_log((isdsAppliance=isds_server))
#
# TOKEN.PY (NEW)
#
# p(ibmsecurity.isds.token.get(isdsAppliance=isds_server))
