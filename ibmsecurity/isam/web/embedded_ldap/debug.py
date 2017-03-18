import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieve existing debug level.
    """
    return isamAppliance.invoke_get("Retrieving debug level for embedded ldap",
                                    "/isam/embedded_ldap/debug_level/v1")


def set(isamAppliance, trace=False, connection=False, search_filter=False, config_filter=False, acl_processing=False,
        statistics=False, statistics_entries=False, shell_backend=False, entry_parsing=False, sync_replication=False,
        uncategorized=False, check_mode=False, force=False):
    """
    Set debug levels in embedded ldap
    """
    if force is True or _check(isamAppliance, trace, connection, search_filter, config_filter, acl_processing,
                               statistics, statistics_entries, shell_backend, entry_parsing, sync_replication,
                               uncategorized) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post(
                "Set debug level in embedded ldap",
                "/isam/embedded_ldap/debug_level/v1",
                {
                    "trace": trace,
                    "connection": connection,
                    "search.filter": search_filter,
                    "config.file": config_filter,
                    "acl.processing": acl_processing,
                    "statistics": statistics,
                    "statistics.entries": statistics_entries,
                    "shell.backend": shell_backend,
                    "entry.parsing": entry_parsing,
                    "sync.replication": sync_replication,
                    "uncategorized": uncategorized
                })

    return isamAppliance.create_return_object()


def _check(isamAppliance, trace=False, connection=False, search_filter=False, config_filter=False, acl_processing=False,
           statistics=False, statistics_entries=False, shell_backend=False, entry_parsing=False, sync_replication=False,
           uncategorized=False):
    new_trace = {
        "trace": trace,
        "connection": connection,
        "search.filter": search_filter,
        "config.file": config_filter,
        "acl.processing": acl_processing,
        "statistics": statistics,
        "statistics.entries": statistics_entries,
        "shell.backend": shell_backend,
        "entry.parsing": entry_parsing,
        "sync.replication": sync_replication,
        "uncategorized": uncategorized
    }

    ret_obj = get(isamAppliance)

    return ibmsecurity.utilities.tools.json_sort(new_trace) == ibmsecurity.utilities.tools.json_sort(ret_obj['data'])


def compare(isamAppliance1, isamAppliance2):
    """
    Compare debug levels in two appliances
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
