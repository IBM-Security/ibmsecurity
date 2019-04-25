import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/iam/access/v8/sts/modules"
requires_modules = ['federation']
requires_version = "9.0.1.0"


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieve a list of STS module instances
    """
    return isamAppliance.invoke_get("Retrieve a list of STS module instances", uri,
                                    requires_modules=requires_modules,
                                    requires_version=requires_version)


def search(isamAppliance, name, force=False, check_mode=False):
    """
    Search STS modules by name
    """
    ret_obj = get_all(isamAppliance)
    return_obj = isamAppliance.create_return_object()

    for obj in ret_obj['data']:
        if obj['name'] == name:
            logger.info("Found STS Module {0} id: {1}".format(name, obj['id']))
            return_obj['data'] = obj['id']
            return_obj['rc'] = 0

    return return_obj


def get(isamAppliance, name, check_mode=False, force=False):
    """
    Retrieve a specific STS module instance
    """
    ret_obj = search(isamAppliance, name=name, check_mode=check_mode, force=force)
    id = ret_obj['data']

    if id == {}:
        warnings = ["STS Module {0} had no match, skipping retrieval.".format(name)]
        return isamAppliance.create_return_object(warnings=warnings)
    else:
        return _get(isamAppliance, id)


def _get(isamAppliance, id):
    """
    Internal function to get data using "id" - used to avoid extra calls
    """
    return isamAppliance.invoke_get("Retrieve a specific STS module instance", "{0}/{1}".format(uri, id),
                                    requires_modules=requires_modules,
                                    requires_version=requires_version)


def get_types(isamAppliance, check_mode=False, force=False):
    """
    Retrieve a list of STS module types
    """
    return isamAppliance.invoke_get("Retrieve a list of STS module types", "/iam/access/v8/sts/module-types",
                                    requires_modules=requires_modules,
                                    requires_version=requires_version)
