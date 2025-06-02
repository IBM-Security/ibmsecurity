import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)

requires_modules = ["wga"]
requires_version = "10.0.6.0"
# URIs for this module
acl_list_uri = "/isam/pdadmin/acllistext/v1"
show_uri = "/isam/pdadmin/aclshowext/v1"
object_list_uri = "/isam/pdadmin/aclfindext/v1"

def get_list(isamAppliance, isamUser, acl_attribute_name=None, acl_attribute_value=None, admin_domain='Default'):
    """
    Retrieve a list of ACLs using either an attribute name or value.
    """
    logger.info("ACL Name: {}".format(acl_attribute_name))
    logger.info("ACL Value: {}".format(acl_attribute_value))
    logger.info("Domain: {}".format(admin_domain))

    ret_obj = isamAppliance.invoke_post("Retrieve a list of ACLs",
                                         acl_list_uri, {
                                            "admin_id": isamUser.username,
                                            "admin_pwd": isamUser.password,
                                            "acl_attribute_name": acl_attribute_name,
                                            "acl_attribute_value": acl_attribute_value,
                                            "admin_domain": admin_domain
                                        })
    ret_obj['changed'] = False

    return ret_obj


def get(isamAppliance, isamUser, acl_name, admin_domain='Default'):
    """
    Retrieve a specific ACL
    """
    ret_obj = isamAppliance.invoke_post("Retrieve a specific ACL",
                                         show_uri, {
                                            "admin_id": isamUser.username,
                                            "admin_pwd": isamUser.password,
                                            "acl_name": acl_name,
                                            "admin_domain": admin_domain
                                        })
    ret_obj['changed'] = False

    return ret_obj


def get_object_list(isamAppliance, isamUser, object=None, acl_name=None, acl_attribute_name=None, acl_attribute_value=None,
                 admin_domain='Default'):
    """
    Retrieve a list of objects protected by a given ACL or attribute.
    """
    ret_obj = isamAppliance.invoke_post("Retrieve a list of protected objects",
                                         object_list_uri, {
                                            "admin_id": isamUser.username,
                                            "admin_pwd": isamUser.password,
                                            "object": object,
                                            "acl_name": acl_name,
                                            "acl_attribute_name": acl_attribute_name,
                                            "acl_attribute_value": acl_attribute_value,
                                            "admin_domain": admin_domain
                                        })
    ret_obj['changed'] = False

    return ret_obj


def compare(isamAppliance1, isamAppliance2, isamUser1, isamUser2, acl_attribute_name=None, acl_attribute_value=None,
            admin_domain='Default'):
    """
    Compare the list of ACLs between two appliances
    """
    ret_obj1 = get_list(isamAppliance1, isamUser1, acl_attribute_name, acl_attribute_value, admin_domain=admin_domain)
    ret_obj2 = get_list(isamAppliance2, isamUser2, acl_attribute_name, acl_attribute_value, admin_domain=admin_domain)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2)
