import logging.config
import pprint
from ibmsecurity.appliance.isamappliance import ISAMAppliance
from ibmsecurity.user.applianceuser import ApplianceUser
import pkgutil
import importlib
import ibmsecurity


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
        full_name = package.__name__ + "." + name
        results[full_name] = importlib.import_module(full_name)
        if recursive and is_pkg:
            results.update(import_submodules(full_name))
    return results


# Import all packages within ibmsecurity - recursively
# Note: Advisable to replace this code with specific imports for production code
try:
    import_submodules(ibmsecurity)
except Exception as e:
    print('Failed to import all submodules: ' + e)


# Setup logging to send to stdout, format and set log level
# logging.getLogger(__name__).addHandler(logging.NullHandler())
logging.basicConfig()
# Valid values are 'DEBUG', 'INFO', 'ERROR', 'CRITICAL'
logLevel = "DEBUG"
DEFAULT_LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "[%(asctime)s] [PID:%(process)d TID:%(thread)d] [%(levelname)s] [%(name)s] [%(funcName)s():%(lineno)s] %(message)s"
        },
    },
    "handlers": {
        "default": {
            "level": logLevel,
            "formatter": "standard",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "": {"level": logLevel, "handlers": ["default"], "propagate": True},
        "requests.packages.urllib3.connectionpool": {
            "level": "ERROR",
            "handlers": ["default"],
            "propagate": True,
        },
    },
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
    u = ApplianceUser(username="admin@local", password="admin")
    # Create an ISAM appliance with above credential
    isam_server = ISAMAppliance(hostname="192.168.198.100", user=u, lmi_port=443)

    # Get the current SNMP monitoring setup details
    p(ibmsecurity.isam.base.snmp_monitoring.get(isamAppliance=isam_server))
    # Set the V2 SNMP monitoring
    p(
        ibmsecurity.isam.base.snmp_monitoring.set_v1v2(
            isamAppliance=isam_server, community="IBM"
        )
    )
    # Commit or Deploy the changes
    p(ibmsecurity.isam.appliance.commit(isamAppliance=isam_server))
