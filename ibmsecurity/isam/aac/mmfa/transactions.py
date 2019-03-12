import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)
module_uri = "/iam/access/v8/mmfa-transactions/"
requires_modules = ["mga"]
requires_version = None


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Get information on all existing Transactions
    """
    return isamAppliance.invoke_get("Retrieving a list of transactions", "{0}".format(module_uri),
                                    requires_modules=requires_modules, requires_version=requires_version)


def get(isamAppliance, id, check_mode=False, force=False):
    """
    Get information on single transaction
    """
    return isamAppliance.invoke_get("Retrieving a transaction", "{0}{1}".format(module_uri, id),
                                    requires_version=requires_version,
                                    requires_modules=requires_modules)


def delete(isamAppliance, id, check_mode=False, force=False):
    """
    Deletes single transaction
    """
    if force is True or _check(isamAppliance, id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete("Deleting transaction",
                                               "{0}{1}".format(module_uri, id), requires_modules=requires_modules,
                                               requires_version=requires_version)

    return isamAppliance.create_return_object()


def _check(isamAppliance, id=None):
    """
    checks with id exists within isam appliance
    :param isamAppliance:
    :param id:
    :return:
    """
    new_obj = get_all(isamAppliance)

    if id != None:
        for users in new_obj['data']:
            if users['id'] == id:
                return True

    return False
