import logging
import json
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/iam/access/v8/fido2/registrations"
requires_modules = ["mga"]
requires_version = "9.0.7.0"

def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieve a list of all FIDO2 registrations
    """
    return isamAppliance.invoke_get("Retrieve a list of all FIDO2 registrations", uri,
                                    requires_modules=requires_modules, requires_version=requires_version)

def get(isamAppliance, credentialId, check_mode=False, force=False):
    """
    Retrieve a specific FIDO2 registration
    """
    ret_obj = isamAppliance.invoke_get("Retrieve a specific FIDO2 registration by credentialId",
                                    f"{uri}/{credentialId}", ignore_error=True,
                                    requires_modules=requires_modules, requires_version=requires_version)

    if ret_obj['rc'] == 404:
        logger.info("FIDO2 registration for {0} had no match.".format(credentialId))
        return isamAppliance.create_return_object()
    return ret_obj

def delete(isamAppliance, username=None, credentialId=None, check_mode=False, force=False):
    """
    Delete all or specific FIDO2 registrations for a user
    """
    if username is None and credentialId is None:
        from ibmsecurity.appliance.ibmappliance import IBMError
        raise IBMError("999", "Cannot delete FIDO2 registration for unknown username or credentialID. Provide one of the required parameters.")

    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:
        if username is not None:
            return isamAppliance.invoke_delete(
                "Delete all FIDO2 registrations for a user",
                "{0}/username/{1}".format(uri, username),
                requires_modules=requires_modules, requires_version=requires_version)
        elif credentialId is not None:
            return isamAppliance.invoke_delete(
                "Delete a specific FIDO2 registration for a user",
                "{0}/credentialId/{1}".format(uri, credentialId),
                requires_modules=requires_modules, requires_version=requires_version)
