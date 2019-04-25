import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/iam/access/v8/alias_service"
requires_modules = ["federation"]
requires_version = "9.0.1.0"


def get(isamAppliance, sortBy=None, count=None, start=None, filter=None, check_mode=False, force=False):
    """
    Retrieve alias associations
    """
    return isamAppliance.invoke_get("Retrieve alias associations", "{0}{1}".format(uri, tools.create_query_string(
        sortBy=sortBy, count=count, start=start, filter=filter)), requires_modules=requires_modules,
                                    requires_version=requires_version)


def add(isamAppliance, username, federation_id, aliases, type=None, partner_id=None, check_mode=False, force=False):
    """
    Create an alias association

    TODO: Need to understand uniqueness of federation/partner_id and username to complete this
    """
    warnings = ["Idempotency has not been coded for this function."]
    if force is True or _check(isamAppliance, username) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            fed_id = federation_id
            if partner_id is not None:
                fed_id = fed_id + "|" + partner_id
            json_data = {
                "username": username,
                "federation_id": fed_id,
                "aliases": aliases
            }
            if type is not None:
                json_data['type'] = type
            return isamAppliance.invoke_post(
                "Create an alias association", uri, json_data, warnings=warnings,
                requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object()


def _check(isamAppliance, username):
    """
    TODO: Code the idempotency check logic
    """
    return False
