import logging

logger = logging.getLogger(__name__)


# *** WORK IN PROGRESS - module not done yet

def get_all(isamAppliance, isamUser, object='/', admin_domain='Default'):
    """
    Retrieve a list of objects
    """
    ret_obj = isamAppliance.invoke_post("Retrieve a list of objects",
                                        "/isam/pdadmin/objectlistandshowext/v1", {
                                            "admin_id": isamUser.username,
                                            "admin_pwd": isamUser.password,
                                            "admin_domain": admin_domain,
                                            "object": object
                                        })
    ret_obj['changed'] = False

    return ret_obj


def get(isamAppliance, isamUser, object, admin_domain='Default'):
    """
    Retrieve a specific object
    """
    ret_obj = isamAppliance.invoke_post("Retrieve a specific object",
                                        "/isam/pdadmin/objectshowext/v1", {
                                            "admin_id": isamUser.username,
                                            "admin_pwd": isamUser.password,
                                            "admin_domain": admin_domain,
                                            "object": object
                                        })
    ret_obj['changed'] = False

    return ret_obj


def compare(isamAppliance1, isamAppliance2, isamUser, admin_domain='Default'):
    """
    Compare objects between two appliances
    """
    ret_obj1 = get_all(isamAppliance1, isamUser, '/', admin_domain)
    ret_obj2 = get_all(isamAppliance2, isamUser, '/', admin_domain)

    for obj in ret_obj1['data']:
        ret_obj = get(isamAppliance1, isamUser=isamUser, object=obj['id'], admin_domain=admin_domain)
        obj['script'] = ret_obj['data']['contents']
    for obj in ret_obj2['data']:
        ret_obj = get(isamAppliance2, isamUser=isamUser, object=obj['id'], admin_domain=admin_domain)
        obj['script'] = ret_obj['data']['contents']

    import ibmsecurity.utilities.tools
    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
