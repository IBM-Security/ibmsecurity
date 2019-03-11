import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/iam/access/v8/piptypes"
requires_modules = ["mga"]
requires_version = None


def get_all(isamAppliance, count=None, start=None, filter=None, sortBy=None, check_mode=False, force=False):
    """
    Retrieve a list of policy information point types
    """
    return isamAppliance.invoke_get("Retrieve a list of policy information point types",
                                    "{0}/{1}".format(uri,
                                                     tools.create_query_string(count=count, start=start, filter=filter,
                                                                               sortBy=sortBy)),
                                    requires_modules=requires_modules, requires_version=requires_version)


def get(isamAppliance, name, check_mode=False, force=False):
    """
    Retrieve a specific policy information point type
    """
    ret_obj = search(isamAppliance, name, check_mode=False, force=False)
    id = ret_obj['data']

    if id == {}:
        logger.info("PIP Type {0} had no match, skipping retrieval.".format(name))
        warnings = ["PIP Type {0} had no match, skipping retrieval.".format(name)]
        return isamAppliance.create_return_object(warnings=warnings)
    else:
        return _get(isamAppliance, id)


def search(isamAppliance, name, force=False, check_mode=False):
    """
    Retrieve ID for named PIP
    """
    ret_obj = get_all(isamAppliance)

    ret_obj_new = isamAppliance.create_return_object()

    for obj in ret_obj['data']:
        if obj['name'] == name:
            logger.info("Found Policy Type {0} id: {1}".format(name, obj['id']))
            ret_obj_new['data'] = obj['id']

    return ret_obj_new


def _get(isamAppliance, id):
    return isamAppliance.invoke_get("Retrieve a specific PIP Type",
                                    "{0}/{1}".format(uri, id))
