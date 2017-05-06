import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/wga/kerberos/config/capaths"
requires_modules = ['wga']
requires_version = None


def get_all(isamAppliance, recursive='yes', includeValues='yes', addParent='yes', check_mode=False, force=False):
    """
    Retrieve Kerberos Configuration: CA Paths
    """
    return isamAppliance.invoke_get("Retrieve Kerberos Configuration: CA Paths",
                                    "{0}{1}".format(uri, tools.create_query_string(recursive=recursive,
                                                                                   includeValues=includeValues,
                                                                                   addParent=addParent)),
                                    requires_modules=requires_modules, requires_version=requires_version)


def get(isamAppliance, name, check_mode=False, force=False):
    pass


def search(isamAppliance, name, check_mode=False, force=False):
    """
    Search definition id by name
    """
    ret_obj = get_all(isamAppliance)
    return_obj = isamAppliance.create_return_object()
    return_obj["warnings"] = ret_obj["warnings"]

    for obj in ret_obj['data']:
        if obj['name'] == name:
            logger.info("Found name {0} id: {1}".format(name, obj['id']))
            return_obj['data'] = obj['id']
            return_obj['rc'] = 0

    return return_obj

def set(isamAppliance, check_mode=False, force=False):
    pass


def add(isamAppliance, check_mode=False, force=False):
    pass


def delete(isamAppliance, check_mode=False, force=False):
    pass


def update(isamAppliance, check_mode=False, force=False):
    pass


def compare(isamAppliance1, isamAppliance2):
    """
    Compare kerberos configuration ca paths between two appliances
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    for obj in ret_obj1['data']:
        del obj['id']
    for obj in ret_obj2['data']:
        del obj['id']

    return tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
