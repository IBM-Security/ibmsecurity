import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)


def get_all(isamAppliance, start=None, count=None, filter=None, sortBy=None, check_mode=False, force=False):
    """
    Retrieve a list of authentication mechanisms types
    """
    return isamAppliance.invoke_get("Retrieve a list of authentication mechanisms types",
                                    "/iam/access/v8/authentication/mechanism/types{0}".format(
                                        tools.create_query_string(start=start, count=count, filter=filter,
                                                                  sortBy=sortBy)))


def get(isamAppliance, name, check_mode=False, force=False):
    """
    Retrieve a specific authentication mechanism type
    """
    ret_obj = search(isamAppliance, name=name, check_mode=check_mode, force=force)
    id = ret_obj['data']

    if id == {}:
        logger.info("Authentication Mechanism Type {0} had no match, skipping retrieval.".format(name))
        return isamAppliance.create_return_object()
    else:
        return isamAppliance.invoke_get("Retrieve a specific authentication mechanism type",
                                        "/iam/access/v8/authentication/mechanism/types/{0}".format(id))


def search(isamAppliance, name, force=False, check_mode=False):
    """
    Search authentication mechanism type ID by name
    """
    ret_obj = get_all(isamAppliance)
    return_obj = isamAppliance.create_return_object()

    for obj in ret_obj['data']:
        if obj['name'] == name:
            logger.info("Found Authentication Mechanism Type {0} id: {1}".format(name, obj['id']))
            return_obj['data'] = obj['id']
            return_obj['rc'] = 0

    return return_obj


def compare(isamAppliance1, isamAppliance2):
    """
    Compare Authentication Types between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    for obj in ret_obj1['data']:
        del obj['id']
    for obj in ret_obj2['data']:
        del obj['id']

    return tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['id'])
