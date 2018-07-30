import logging

logger = logging.getLogger(__name__)

# URI for this module
uri = "/isam/rsyslog_forwarder/source_names"
requires_modules = None
requires_version = "9.0.2.1"


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieve the remote syslog forwarding sources
    """
    return isamAppliance.invoke_get(
        "Retrieve the remote syslog forwarding sources", uri, requires_modules=requires_modules,
        requires_version=requires_version)
