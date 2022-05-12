import logging
import json
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/iam/access/v8/fido2/u2f-migration"
requires_modules = ["mga"]
requires_version = "9.0.7.0"

def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieve a count of U2F Registrations yet to be migrated
    """
    return isamAppliance.invoke_get("Retrieve a count of U2F Registrations yet to be migrated", uri,
                                    requires_modules=requires_modules, requires_version=requires_version)

def migrate(isamAppliance, batchSize, batchCount, check_mode=False, force=False):
    """
    Migrate U2F Registrations
    """

    json_data = {
        "batchSize": batchSize,
        "batchCount": batchCount
    }

    ret_obj = isamAppliance.invoke_post("Migrate U2F Registrations", uri, json_data,
                                    requires_modules=requires_modules, requires_version=requires_version)

    return ret_obj
