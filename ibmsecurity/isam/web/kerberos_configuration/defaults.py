import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/wga/kerberos/config/libdefaults"
requires_modules = ['wga']
requires_version = None


def get(isamAppliance, recursive='yes', includeValues='yes', check_mode=False, force=False):
    """
    Retrieve Kerberos Configuration: Defaults
    """
    return isamAppliance.invoke_get("Retrieve Kerberos Configuration: Defaults",
                                    "{0}{1}".format(uri, tools.create_query_string(recursive=recursive,
                                                                                   includeValues=includeValues)),
                                    requires_modules=requires_modules, requires_version=requires_version)


def compare(isamAppliance1, isamAppliance2):
    """
    Compare kerberos configuration defaults between two appliances
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    for obj in ret_obj1['data']:
        del obj['id']
    for obj in ret_obj2['data']:
        del obj['id']

    return tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['id'])
