import logging

logger = logging.getLogger(__name__)

# URI for this module
uri = "/events/system"
requires_modules = None
requires_version = None


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Exporting the System Event Log

    """
    return isamAppliance.invoke_get("Exporting the System Event Log",
                                    "{0}".format(uri),
                                    requires_modules=requires_modules, requires_version=requires_version)


def get(isamAppliance, field, filter, check_mode=False, force=False):
    """
    Exporting the filtered System Event Log

    """
    return isamAppliance.invoke_get("Exporting the filtered System Event Log",
                                    "{0}/{1}/{2}".format(uri, field, filter),
                                    requires_modules=requires_modules, requires_version=requires_version)


def get_by_date_range_filter(isamAppliance, time_filter, check_mode=False, force=False):
    """
    Exporting the filtered System Event Log Using a Date Range

    """
    return isamAppliance.invoke_get("Exporting the filtered System Event Log Using a Date Range",
                                    "{0}/time/{1}".format(uri, time_filter,
                                                          requires_modules=requires_modules,
                                                          requires_version="10.0.1"))
