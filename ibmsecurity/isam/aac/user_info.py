import logging

from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/iam/access/v8/user-info"
requires_modules = None
requires_version = "9.0.3"


# TODO - WARNING: This has not been fully tested.  Please open a bug issue on GITHub if you find a problem.

def get_all(isamAppliance, count=None, start=None, check_mode=False, force=False):
    """
    Retrieve a list of attributes for all users
    """
    return isamAppliance.invoke_get("Retrieve a list of access policies",
                                    "{0}/{1}".format(uri, tools.create_query_string(count=count, start=start)),
                                    requires_modules=requires_modules, requires_version=requires_version)


def get(isamAppliance, userid, check_mode=False, force=False):
    """
    Retrieve the attributes of a user
    """

    return isamAppliance.invoke_get("Retrieve the attributes of a user",
                                    "{0}/{1}".format(uri, userid),
                                    requires_modules=requires_modules,
                                    requires_version=requires_version)


def delete(isamAppliance, userid, check_mode=False, force=False):
    """
    Delete user attributes
    """

    ret_obj = get(isamAppliance, userid)

    if force is True or ret_obj['data'] != []:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete("Delete user attributes",
                                               "{0}/{1}".format(uri, userid),
                                               requires_modules=requires_modules,
                                               requires_version=requires_version)

    return isamAppliance.create_return_object()
