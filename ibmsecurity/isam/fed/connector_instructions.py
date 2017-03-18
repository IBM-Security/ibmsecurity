import logging

logger = logging.getLogger(__name__)


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieve all connector instruction sets
    """
    return isamAppliance.invoke_get("Retrieve all connector instruction sets",
                                    "/mga/connector_instructions/")


def get(isamAppliance, id, variable_names=None, check_mode=False, force=False):
    """
    Retrieve a connector instruction set

    Noe: Pass variable_names as a list key value pairs like so:
        [{'hostname': 'ibm.com'}, {'key': 'value'}]

    TODO: test variable_names...
    """
    query_str = None
    if variable_names is not None:
        for var in variable_names:
            if query_str is None:
                query_str = '?'
            else:
                query_str += '&'
            for key, value in var.iteritems():
                query_str += "{0}={1}".format(key, value)

    return isamAppliance.invoke_get("Retrieve a connector instruction set",
                                    "/mga/connector_instructions/{0}{1}".format(id, query_str))
