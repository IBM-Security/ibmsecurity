import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)


def get_network(isdsAppliance, application_interface, statistics_duration, check_mode=False, force=False):
    """
    Retrieving the Application Interface Statistics
    """
    return isdsAppliance.invoke_get("Retrieving the Application Interface Statistics",
                                    "/analysis/interface_statistics{0}".format(
                                        tools.create_query_string(prefix=application_interface,
                                                                  timespan=statistics_duration)))


def get_cpu(isdsAppliance, statistics_duration, check_mode=False, force=False):
    """
    Retrieving the CPU Usage Statistics
    """
    return isdsAppliance.invoke_get(
        "Retrieving the CPU Usage Statistics",
        "/analysis/system_cpu{0}".format(
            tools.create_query_string(
                timespan=statistics_duration)))


def get_memory(isdsAppliance, statistics_duration, check_mode=False, force=False):
    """
    Retrieving the Storage Usage Statistics
    """
    return isdsAppliance.invoke_get(
        "Retrieving the Memory Usage Statistics",
        "/analysis/system_memory{0}".format(
            tools.create_query_string(
                timespan=statistics_duration)))


def get_storage(isdsAppliance, statistics_duration, check_mode=False, force=False):
    """
    Retrieving the Storage Usage Statistics
    """
    return isdsAppliance.invoke_get(
        "Retrieving the Storage Usage Statistics",
        "/analysis/system_storage{0}".format(
            tools.create_query_string(
                timespan=statistics_duration)))
