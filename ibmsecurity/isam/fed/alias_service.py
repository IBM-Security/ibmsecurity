import logging
from  ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)


def get(isamAppliance, sortBy=None, count=None, start=None, filter=None, check_mode=False, force=False):
    """
    Retrieve alias associations
    """
    return isamAppliance.invoke_get("Retrieve alias associations",
                                    "/iam/access/v8/alias_service{0}".format(
                                        tools.create_query_string(sortBy=sortBy, count=count, start=start,
                                                                  filter=filter)))


def add(isamAppliance, username, federation_id, aliases, type=None, partner_id=None, check_mode=False, force=False):
    """
    Create an alias association

    TODO: Need to understand uniqueness of federation/partner_id and username to complete this
    """
    if force is True or _check(isamAppliance, username) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            fed_id = federation_id
            if partner_id is not None:
                fed_id = fed_id + "|" + partner_id
            json_data =                 {
                    "username": username,
                    "federation_id": fed_id,
                    "aliases": aliases
                }
            if type is not None:
                json_data['type'] = type
            return isamAppliance.invoke_post(
                "Create an alias association",
                "/iam/access/v8/alias_service", json_data)

    return isamAppliance.create_return_object()
