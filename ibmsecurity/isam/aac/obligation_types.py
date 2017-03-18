import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)
artifact_type = "Obligation type"

# URI for this module
uri = "/iam/access/v8/obligation/types"


def search(isamAppliance, name):
    """
    Search for Obligation Type by name
    """
    ret_obj = get_all(isamAppliance)
    return_obj = isamAppliance.create_return_object()

    for obj in ret_obj["data"]:
        if obj["name"] == name:
            logger.info('Found {0} "{1}" with id: {2}'.format(artifact_type, name, obj['id']))
            return_obj['data'] = obj['id']
            return_obj['rc'] = 0

    return return_obj


def get_all(isamAppliance, start=None, count=None, filter=None, sortBy=None, check_mode=False, force=False):
    """
    Retrieve a list of Obligation types
    """
    return isamAppliance.invoke_get("Retrieve a list of {0}", "{1}/{2}".format(artifact_type, uri,
                                                                               tools.create_query_string(start=start,
                                                                                                         count=count,
                                                                                                         filter=filter,
                                                                                                         sortBy=sortBy)))


def get(isamAppliance, name, check_mode=False, force=False):
    """
    Retrieve a specific Obligation
    """

    ret_obj = search(isamAppliance, name)

    if ret_obj['data'] == {}:
        logger.info('{0} "{1}" had no match, skipping retrieval.'.format(artifact_type, name))
        return isamAppliance.create_return_object()
    else:
        return isamAppliance.invoke_get("Retrieve a specific obligation",
                                        "{0}/{1}".format(uri, ret_obj['data']))
