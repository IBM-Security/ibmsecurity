import logging

logger = logging.getLogger(__name__)

# URI for this module
uri = "/isam/rsyslog_forwarder/source_names/{}/instances"
requires_modules = None
requires_version = "9.0.2.1"


def get(isamAppliance, source_name='webseal', check_mode=False, force=False):
    """
    Retrieve the instances for a particular remote syslog forwarding source
    """
    return isamAppliance.invoke_get(
        "Retrieve the instances for a particular remote syslog forwarding source", uri.format(source_name),
        requires_modules=requires_modules, requires_version=requires_version)
