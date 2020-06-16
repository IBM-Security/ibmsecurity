import logging

logger = logging.getLogger(__name__)

uri = "/isam/azn_server"
requires_modules = None
requires_version = None
version = "v1"


def get(isamAppliance, isamUser, domain="Default", check_mode=False, force=False):
    """
    Retrieving the list of authorization servers
    """
    return isamAppliance.invoke_post("Retrieving all authorization servers",
                                     "{0}".format(uri),
                                     {
                                         "user": isamUser.username,
                                         "password": isamUser.password,
                                         "domain": domain
                                     },
                                     requires_modules=requires_modules, requires_version=requires_version)


def delete(isamAppliance, id, isamUser, domain="Default", check_mode=False, force=False):
    """
    Removing an authorization server
    """
    if force is True or _check(isamAppliance, id, isamUser, domain) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete("Remove a authorization server",
                                               "{0}/{1}".format(uri, id),
                                               {

                                                   "user": isamUser.username,
                                                   "password": isamUser.password,
                                                   "domain": domain
                                               },
                                               requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()


def _check(isamAppliance, id, isamUser, domain):
    """
    Check if authorization server is already created or not

    :param isamAppliance:
    :return:
    """
    ret_obj = get(isamAppliance, isamUser, domain)

    logger.debug("Looking for existing authorization servers in: {0}".format(ret_obj['data']))
    if ret_obj['data']:
        for obj in ret_obj['data']:
            if obj['id'] == id:
                logger.debug("Found authorization server: {0}".format(id))
                return True

    return False
