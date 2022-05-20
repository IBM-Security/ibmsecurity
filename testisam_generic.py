"""
Usage:  testisam_generic.py
        testisam_generic.py [--hostname=ISAM_LMI --username=ISAM_ADMIN --password=ISAM_ADMIN_PASSWORD --lmi_port=443]

Options:
  --hostname=hostname    Hostname (eg. isamlmi.local.com)
  --username=admin      The LMI administration user.  Defaults to admin@local
  --password=password    The LMI administration user's password.  Defaults to admin
  --lmi_port=443        The lmi port, defaults to 443
  -h --help     Show this screen.

"""
import logging.config
import pprint
from ibmsecurity.appliance.isamappliance import ISAMAppliance
from ibmsecurity.user.applianceuser import ApplianceUser
import pkgutil
import importlib

from docopt import docopt


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

def loadArgs(__doc__):
    args = docopt(__doc__)
    if args['--hostname']:
        hostname = args['--hostname']
    else:
        hostname = "127.0.0.1"
    if args['--username']:
        hostname = args['--username']
    else:
        username = "admin@local"
    if args['--password']:
        password = args['--password']
    else:
        password = "admin"
    if args['--lmi_port']:
        lmi_port = args['--lmi_port']
    else:
        lmi_port = "443"

    return hostname, username, password, lmi_port

if __name__ == "__main__":
    """
    This test program should not execute when imported, which would otherwise
    cause problems when generating the documentation.
    """
    hostname, username, password, lmi_port = loadArgs(__doc__)

    # Create a user credential for ISAM appliance
    u = ApplianceUser(username=username, password=password)
    # Create an ISAM appliance with above credential
    isam_server = ISAMAppliance(hostname=hostname, user=u, lmi_port=lmi_port)

    # Get the current SNMP monitoring setup details
    p(ibmsecurity.isam.web.iag.export.features.get(isamAppliance=isam_server))

    # Commit or Deploy the changes
    #p(ibmsecurity.isam.appliance.commit(isamAppliance=isam_server))
