import logging

logger = logging.getLogger(__name__)

# URI for this module
uri = "/isam/rsyslog_forwarder/source_names/{}/instances/{}/logs"
requires_modules = None
requires_version = "9.0.2.1"


def get(isamAppliance, instance_name, source_name='webseal', check_mode=False, force=False):
    """
    Retrieve the log files for a particular remote syslog forwarding source and instance
    """
    return isamAppliance.invoke_get(
        "Retrieve the log files for a particular remote syslog forwarding source and instance",
        uri.format(source_name, instance_name), requires_modules=requires_modules, requires_version=requires_version)
