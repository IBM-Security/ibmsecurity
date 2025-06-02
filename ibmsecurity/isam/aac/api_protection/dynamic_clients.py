import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/iam/access/v8/dynamic_clients"
requires_modules = ["mga"]
requires_version = "9.0.5.0"


def get_all(isamAppliance, sortBy=None, count=None, start=None, filter=None, check_mode=False, force=False):
    """
    Retrieve a list of API protection clients
    """
    return isamAppliance.invoke_get("Retrieve several dynamically registered clients",
                                    f"{uri}/{tools.create_query_string(filter=filter, sortBy=sortBy, count=count, start=start)}",
                                    requires_modules=requires_modules, requires_version=requires_version)


def get(isamAppliance, client_id, check_mode=False, force=False):
    """
    Retrieve a dynamically registered client
    """
    return isamAppliance.invoke_get("Retrieve a dynamically registered client", f"{uri}/{client_id}",
                                    requires_modules=requires_modules, requires_version=requires_version)


def search(isamAppliance, client_id, check_mode=False, force=False):
    """
    Search API Protection Dynamic Client by name
    """
    ret_obj = get_all(isamAppliance)

    for obj in ret_obj['data']:
        if obj['clientId'] == client_id:
            logger.info(f"Found API Protection Dynamic Client id: {client_id}")
            return True

    return False


def delete(isamAppliance, client_id, check_mode=False, force=False):
    """
    Delete a dynamically registered client
    """

    if force or search(isamAppliance, client_id, check_mode=check_mode, force=force):
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Delete a dynamically registered client", f"{uri}/{client_id}",
                requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()
