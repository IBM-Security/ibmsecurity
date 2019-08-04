import logging

logger = logging.getLogger(__name__)

# URI for this module
uri = "/mga/connector_instructions"
requires_modules = ["federation"]
requires_version = "9.0.0.0"


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieve all connector instruction sets
    """
    return isamAppliance.invoke_get("Retrieve all connector instruction sets", uri,
                                    requires_modules=requires_modules,
                                    requires_version=requires_version)


def get(isamAppliance, id, variable_names=None, check_mode=False, force=False):
    """
    Retrieve a connector instruction set

    Noe: Pass variable_names as a list key value pairs like so:
        [{'hostname': 'ibm.com'}, {'key': 'value'}]

    TODO: test variable_names...
    """
    query_str = ""
    if variable_names is not None:
        for var in variable_names:
            if query_str == "":
                query_str = '?'
            else:
                query_str += '&'

            for key, value in var.items():
                query_str += "{0}={1}".format(key, value)

    return isamAppliance.invoke_get("Retrieve a connector instruction set",
                                    "{0}/{1}{2}".format(uri, id, query_str),
                                    requires_modules=requires_modules,
                                    requires_version=requires_version)
