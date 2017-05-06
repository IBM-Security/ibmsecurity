import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/wga/kerberos/config/domain_realm"
requires_modules = ['wga']
requires_version = None


def get(isamAppliance, recursive='yes', includeValues='yes', check_mode=False, force=False):
    """
    Retrieve Kerberos Configuration: Domains
    """
    return isamAppliance.invoke_get("Retrieve Kerberos Configuration: Domains",
                                    "{0}{1}".format(uri, tools.create_query_string(recursive=recursive,
                                                                                   includeValues=includeValues)),
                                    requires_modules=requires_modules, requires_version=requires_version)


def compare(isamAppliance1, isamAppliance2):
    """
    Compare kerberos configuration domains between two appliances
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    return tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
