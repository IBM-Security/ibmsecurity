"""
Usage:  testisam_generic.py
        testisam_generic.py [--hostname=ISAM_LMI --username=ISAM_ADMIN --password=ISAM_ADMIN_PASSWORD
           --lmi_port=443 --method=ibm.isam.appliance.get --method_options="name=test" --commit]

Options:
  --hostname=hostname    Hostname (eg. isamlmi.local.com)
  --username=admin      The LMI administration user.  Defaults to admin@local
  --password=password    The LMI administration user's password.  Defaults to admin
  --lmi_port=443        The lmi port, defaults to 443
  --method=ibm.isam.method  The method to call
  --method_options="name=name"  String of key-value pairs "name=test,key2=key2"
  --commit  Perform commit of the changes.  Not required if you do a GET
  -h --help     Show this screen.

"""
import logging.config
import pprint
from ibmsecurity.appliance.isamappliance import ISAMAppliance
from ibmsecurity.user.applianceuser import ApplianceUser
import pkgutil
import importlib
import json
import ibmsecurity

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


def load_args(__doc__):
    args = docopt(__doc__)
    method = None
    _options = "isamAppliance=isam_server"
    commit = False
    if args['--commit']:
        commit = True
    if args['--hostname']:
        hostname = args['--hostname']
    else:
        hostname = "127.0.0.1"
    if args['--username']:
        username = args['--username']
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
    if args["--method"]:
        method = args["--method"]
    if args["--method_options"]:
        _newoptions = args["--method_options"]
        # split in key/value pairs
        d = dict(kv.split('=', 1) for kv in _newoptions.split(','))
        for k, v in d.items():
            logging.debug(f"VALUE: {v}")
            if 'json.' in v:
                _options = _options + "," + k + "=" + eval(v)
            else:
                _options = _options + "," + k + "='" + str(v) + "'"
            logging.debug(_options)

    return commit, hostname, username, password, lmi_port, method, _options


if __name__ == "__main__":
    """
    This test program should not execute when imported, which would otherwise
    cause problems when generating the documentation.
    """
    commit, hostname, username, password, lmi_port, isam_module, options = load_args(__doc__)

    # Create a user credential for ISAM appliance
    u = ApplianceUser(username=username, password=password)
    # Create an ISAM appliance with above credential
    isam_server = ISAMAppliance(hostname=hostname, user=u, lmi_port=lmi_port)

    # Run the method with options
    module_name, method_name = isam_module.rsplit('.', 1)
    mod = importlib.import_module(module_name)
    func_ptr = getattr(mod, method_name)  # Convert action to actual function pointer
    logging.debug(func_ptr)
    func_call = 'func_ptr(' + options + ')'

    # Execute requested 'action'
    p(eval(func_call))

    # Commit or Deploy the changes
    if commit:
        p(ibmsecurity.isam.appliance.commit(isamAppliance=isam_server))
