import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)

uri = "/isam/pdadmin"
requires_version = "10.0.0"
requires_modules = None
requires_model = "Appliance"
version = "v1"

def retrieve(isamAppliance, admin_id, admin_pwd, object='/', admin_domain='Default', check_mode=False, force=False):
    """
    Retrieve a list of objects
    Fix: do not consider 404 an error
    """
    _action = "objectlistandshowext"
    ret_obj = isamAppliance.invoke_post(description="Retrieve a list of objects",
                                        uri=f"{uri}/{_action}/{version}",
                                        ignore_error=True,
                                        data={
                                            "admin_id": admin_id,
                                            "admin_pwd": admin_pwd,
                                            "admin_domain": admin_domain,
                                            "object": object
                                        })
    ret_obj['changed'] = False
    if ret_obj['rc'] == 404:
        logger.info(f"Object {object} could not be found in {admin_domain} for list and show")
        return isamAppliance.create_return_object()
    return ret_obj

def get(isamAppliance, admin_id, admin_pwd, object='/', admin_domain='Default', check_mode=False, force=False):
    """
    Retrieve a specific object
    Fix: do not consider 404 an error
    """
    _action = "objectshowext"
    ret_obj = isamAppliance.invoke_post(description="Retrieve a specific object",
                                        uri=f"{uri}/{_action}/{version}",
                                        ignore_error=True,
                                        data={
                                            "admin_id": admin_id,
                                            "admin_pwd": admin_pwd,
                                            "admin_domain": admin_domain,
                                            "object": object
                                        })
    ret_obj['changed'] = False
    if ret_obj['rc'] == 404:
        logger.info(f"Object {object} could not be found in {admin_domain}")
        return isamAppliance.create_return_object()

    return ret_obj


def compare(isamAppliance1, isamAppliance2, admin_id, admin_pwd, admin_domain='Default', check_mode=False, force=False):
    """
    Compare objects between two appliances
    Note that this only compares the first level
    """
    ret_obj1 = retrieve(isamAppliance1, admin_id, admin_pwd, '/', admin_domain)
    ret_obj2 = retrieve(isamAppliance2, admin_id, admin_pwd, '/', admin_domain)

    for obj in ret_obj1['data']:
        ret_obj = get(isamAppliance1, admin_id, admin_pwd, object=obj['id'], admin_domain=admin_domain)
        obj['script'] = ret_obj['data']['contents']
    for obj in ret_obj2['data']:
        ret_obj = get(isamAppliance2, admin_id, admin_pwd, object=obj['id'], admin_domain=admin_domain)
        obj['script'] = ret_obj['data']['contents']

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
