import logging


logger = logging.getLogger(__name__)

uri = "/mga/scim/configuration"
requires_modules = ["mga", "federation"]
requires_version = "9.0.2"

def get(isamAppliance, ldap_connection, check_mode=False, force=False):
    """
    Retrieving the current list of ldap object classes from the configured ldap
    """
    return isamAppliance.invoke_get("Retrieving the current list of ldap object classes from the configured ldap",
                                    "{0}/urn:ietf:params:scim:schemas:core:2.0:User/ldap_objectclasses?ldap_connection={1}".format(
                                        uri, ldap_connection),
                                    requires_modules=requires_modules,
                                    requires_version=requires_version
                                    )
