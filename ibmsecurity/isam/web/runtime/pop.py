import logging

logger = logging.getLogger(__name__)


# *** WORK IN PROGRESS - module not done yet


def get_all(isamAppliance, isamUser, admin_domain='Default'):
    """
    Retrieve a list of POPs
    """
    ret_obj = isamAppliance.invoke_post("Retrieve a list of POPs",
                                        "/isam/pdadmin/poplistext/v1", {
                                            "admin_id": isamUser.username,
                                            "admin_pwd": isamUser.password,
                                            # "pop_name": pop_name,
                                            # "pop_attribute_name": pop_attribute_name,
                                            # "pop_attribute_value": pop_attribute_value,
                                            "admin_domain": admin_domain
                                        })
    ret_obj['changed'] = False

    return ret_obj


def get(isamAppliance, isamUser, pop_name, admin_domain='Default'):
    """
    Retrieve a specific POP
    """
    ret_obj = isamAppliance.invoke_post("Retrieve a specific POP",
                                        "/isam/pdadmin/popshowext/v1", {
                                            "admin_id": isamUser.username,
                                            "admin_pwd": isamUser.password,
                                            "pop_name": pop_name,
                                            "admin_domain": admin_domain
                                        })
    ret_obj['changed'] = False

    return ret_obj


def get_pop_list(isamAppliance, isamUser, object=None, pop_name=None, pop_attribute_name=None, pop_attribute_value=None,
                 admin_domain='Default'):
    """
    Retrieve a list of protected objects
    """
    ret_obj = isamAppliance.invoke_post("Retrieve a list of protected objects",
                                        "/isam/pdadmin/popfindext/v1", {
                                            "admin_id": isamUser.username,
                                            "admin_pwd": isamUser.password,
                                            "object": object,
                                            "pop_name": pop_name,
                                            "pop_attribute_name": pop_attribute_name,
                                            "pop_attribute_value": pop_attribute_value,
                                            "admin_domain": admin_domain
                                        })
    ret_obj['changed'] = False

    return ret_obj


def compare(isamAppliance1, isamAppliance2, isamUser, admin_domain='Default'):
    """
    Compare URL Mapping between two appliances
    """
    ret_obj1 = get_all(isamAppliance1, isamUser=isamUser, admin_domain=admin_domain)
    ret_obj2 = get_all(isamAppliance2, isamUser=isamUser, admin_domain=admin_domain)

    for obj in ret_obj1['data']:
        del obj['version']
        ret_obj = get(isamAppliance1, pop_name=obj['id'], isamUser=isamUser, admin_domain=admin_domain)
        obj['script'] = ret_obj['data']['contents']
    for obj in ret_obj2['data']:
        del obj['version']
        ret_obj = get(isamAppliance2, pop_name=obj['id'], isamUser=isamUser, admin_domain=admin_domain)
        obj['script'] = ret_obj['data']['contents']

    import ibmsecurity.utilities.tools
    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['version'])
