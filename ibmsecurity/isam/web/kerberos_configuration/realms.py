import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/wga/kerberos/config/realms"
requires_modules = ['wga']
requires_version = None


def get(isamAppliance, recursive='yes', includeValuesInLine='yes', check_mode=False, force=False):
    """
    Retrieve Kerberos Configuration: Realms
    """
    return isamAppliance.invoke_get("Retrieve Kerberos Configuration: Realms",
                                    "{0}{1}".format(uri, tools.create_query_string(recursive=recursive,
                                                                                   includeValuesInLine=includeValuesInLine)),
                                    requires_modules=requires_modules, requires_version=requires_version)


def compare(isamAppliance1, isamAppliance2):
    """
    Compare kerberos configuration realms between two appliances
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    return tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
def add (isamAppliance, realm_type, realm_name, realm_type_key, realm_type_value, force=False):
    """
    add realm entry
    """
    logger.debug('realm name: '+realm_name)
    if realm_type == 'realm':
        return isamAppliance.invoke_post("Add Kerberos Realm", "/wga/kerberos/config/realms",
                                        {
                                             "subsection": realm_name 
                                        })
    if realm_type == 'property':
        return isamAppliance.invoke_post("Add kerberos Realm property", "/wga/kerberos/config/realms/" + realm_name,
                                        {
                                             "name": realm_type_key,
                                             "value": realm_type_value
                                        })

