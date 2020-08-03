import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)
requires_model = "Appliance"

def get_network(isamAppliance, application_interface, statistics_duration, check_mode=False, force=False):
    """
    Retrieving the Application Interface Statistics
    """
    return isamAppliance.invoke_get("Retrieving the Application Interface Statistics",
                                    "/analysis/interface_statistics.json{0}".format(
                                        tools.create_query_string(prefix=application_interface,
                                                                  timespan=statistics_duration)),requires_model=requires_model)


def get_rp_junction(isamAppliance, instance, date, duration, check_mode=False, force=False):
    """
    Retrieving junction average response times for a Reverse Proxy instance
    """
    return isamAppliance.invoke_get("Retrieving junction average response times for a Reverse Proxy instance",
                                    "/analysis/reverse_proxy_traffic/reqtime{0}".format(
                                        tools.create_query_string(date=date,
                                                                  duration=duration,
                                                                  instance=instance)),requires_model=requires_model)


def get_rp_health_summary(isamAppliance, check_mode=False, force=False):
    """
    Retrieving a summary of Reverse Proxy health
    """
    return isamAppliance.invoke_get("Retrieving a summary of Reverse Proxy health",
                                    "/wga/widgets/health.json",requires_model=requires_model)


def get_rp_throughput_summary(isamAppliance, date, duration, aspect, summary=None, check_mode=False, force=False):
    """
    Retrieving a summary of throughput for all Reverse Proxy instances
    """
    headers = {'Accept': 'application/json', 'range': 'items=0-24'}
    return isamAppliance.invoke_get_with_headers("Retrieving a summary of throughput for all Reverse Proxy instances",
                                                 "/analysis/reverse_proxy_traffic/throughput/{0}".format(
                                                     tools.create_query_string(summary=summary,
                                                                               date=date,
                                                                               duration=duration,
                                                                               aspect=aspect)), 
                                                                               requires_model=requires_model,
                                                                               headers=headers)


def get_rp_throughput(isamAppliance, instance, date, duration, check_mode=False, force=False):
    """
    Retrieving throughput records for a specific Reverse Proxy instance
    """
    return isamAppliance.invoke_get("Retrieving throughput records for a specific Reverse Proxy instance",
                                    "/analysis/reverse_proxy_traffic/throughput/{0}{1}".format(instance,
                                                                                               tools.create_query_string(
                                                                                                   date=date,
                                                                                                   duration=duration)),requires_model=requires_model)


def get_rp_traffic_summary(isamAppliance, instance, date, duration, aspect, summary=True, check_mode=False,
                           force=False):
    """
    Retrieving a summary of traffic by Junction or User-Agent on a Reverse Proxy instance
    """
    return isamAppliance.invoke_get(
        "Retrieving a summary of traffic by Junction or User-Agent on a Reverse Proxy instance",
        "/analysis/reverse_proxy_traffic/traffic/instance/{0}/{1}".format(instance,
                                                                          tools.create_query_string(summary=summary,
                                                                                                    date=date,
                                                                                                    duration=duration,
                                                                                                    aspect=aspect)),requires_model=requires_model)


def get_rp_traffic(isamAppliance, instance, date, duration, aspect, aspect_identifier, check_mode=False, force=False):
    """
    Retrieving a summary of traffic records for a specific Junction or User-Agent on a Reverse Proxy instance
    """
    return isamAppliance.invoke_get(
        "Retrieving a summary of traffic records for a specific Junction or User-Agent on a Reverse Proxy instance",
        "/analysis/reverse_proxy_traffic/traffic/instance/{0}/{1}/{2}{3}".format(instance, aspect, aspect_identifier,
                                                                                 tools.create_query_string(date=date,
                                                                                                           duration=duration)),requires_model=requires_model)


def get_rp_traffic_detail(isamAppliance, instance, date, duration, aspect, aspect_identifier, check_mode=False,
                          force=False):
    """
    Retrieving detailed traffic records for a specific Junction or User-Agent on a Reverse Proxy instance
    """
    return isamAppliance.invoke_get(
        "Retrieving detailed traffic records for a specific Junction or User-Agent on a Reverse Proxy instance",
        "/analysis/reverse_proxy_traffic/traffic/instance/{0}/{1}/{2}/{3}".format(instance, aspect, aspect_identifier,
                                                                                  tools.create_query_string(date=date,
                                                                                                            duration=duration,
                                                                                                            aspect=aspect)),requires_model=requires_model)


def get_rp_traffic_detail_aspect(isamAppliance, instance, date, duration, aspect, aspect_identifier, check_mode=False,
                                 force=False):
    """
    Retrieving detailed traffic records for a specific User-Agent on a specific junction in a Reverse Proxy instance
    """
    return isamAppliance.invoke_get(
        "Retrieving detailed traffic records for a specific User-Agent on a specific junction in a Reverse Proxy instance",
        "/analysis/reverse_proxy_traffic/traffic/instance/{0}/{1}/{2}/{1}/{2}{3}".format(instance, aspect,
                                                                                         aspect_identifier,
                                                                                         tools.create_query_string(
                                                                                             date=date,
                                                                                             duration=duration)),requires_model=requires_model)


def get_rp_waf_events(isamAppliance, instance, date, duration, type, check_mode=False,
                      force=False):
    """
    Retrieving security action events for a Reverse Proxy instance
    """
    return isamAppliance.invoke_get(
        "Retrieving security action events for a Reverse Proxy instance",
        "/analysis/reverse_proxy_traffic/pam_events{0}".format(
            tools.create_query_string(
                date=date,
                duration=duration,
                instance=instance,
                type=type)),requires_model=requires_model)


def get_cpu(isamAppliance, statistics_duration, check_mode=False, force=False):
    """
    Retrieving the CPU Usage Statistics
    """
    return isamAppliance.invoke_get(
        "Retrieving the CPU Usage Statistics",
        "/statistics/systems/cpu.json{0}".format(
            tools.create_query_string(
                timespan=statistics_duration)),requires_model=requires_model)


def get_memory(isamAppliance, statistics_duration, check_mode=False, force=False):
    """
    Retrieving the Storage Usage Statistics
    """
    return isamAppliance.invoke_get(
        "Retrieving the Memory Usage Statistics",
        "/statistics/systems/memory.json{0}".format(
            tools.create_query_string(
                timespan=statistics_duration)),requires_model=requires_model)


def get_storage(isamAppliance, statistics_duration, check_mode=False, force=False):
    """
    Retrieving the Storage Usage Statistics
    """
    return isamAppliance.invoke_get(
        "Retrieving the Storage Usage Statistics",
        "/statistics/systems/storage.json{0}".format(
            tools.create_query_string(
                timespan=statistics_duration)),requires_model=requires_model)
