import logging
from ibmsecurity.isam.aac.policy_information_points.all import get, search, _create_json
from ibmsecurity.utilities.tools import json_sort

logger = logging.getLogger(__name__)

# URI for this module
uri = "/iam/access/v8/pips"
requires_modules = ["mga"]
requires_version = None


def add(isamAppliance, name, properties, attributes=None, description=None, type="FiberLink MaaS360",
        check_mode=False, force=False):
    """
    Create a FiberLink MaaS360 policy information point
    """

    ret_obj = search(isamAppliance, name, check_mode=False, force=False)
    id = ret_obj['data']

    if id != {}:
        logger.info("PIP '{0}' already exists.  Skipping add.".format(name))

    if force is True or id == {}:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:

            return isamAppliance.invoke_post(
                "Create a FiberLink MaaS360 policy information point",
                "{0}".format(uri),
                _create_json(name=name, description=description, type=type,
                             attributes=attributes, properties=properties),
                requires_modules=requires_modules, requires_version=requires_version
            )

    return isamAppliance.create_return_object()


def update(isamAppliance, name, properties, attributes=None, description=None, type="FiberLink MaaS360", new_name=None,
           check_mode=False, force=False):
    """
    Update a specific FiberLink MaaS360 policy information point
    """
    ret_obj = search(isamAppliance, name=name)
    id = ret_obj['data']

    update_required = False

    if id != {}:
        ret_obj = get(isamAppliance, name=name)

        if new_name != None:
            json_data = _create_json(name=new_name, properties=properties, attributes=attributes,
                                     description=description, type=type)
        else:
            json_data = _create_json(name=name, properties=properties, attributes=attributes, description=description,
                                     type=type)

        sorted_json_data = json_sort(json_data)

        logger.debug("Sorted input: {0}".format(sorted_json_data))

        del ret_obj['data']['id']
        del ret_obj['data']['predefined']
        sorted_ret_obj = json_sort(ret_obj['data'])

        logger.debug("Sorted existing data: {0}".format(sorted_ret_obj))

        if sorted_json_data != sorted_ret_obj:
            update_required = True
    else:
        logger.info("PIP '{0}' does not exists.  Skipping update.".format(name))
        warnings = ["PIP '{0}' does not exists.  Skipping update.".format(name)]
        return isamAppliance.create_return_object(warnings=warnings)

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)

        else:

            return isamAppliance.invoke_put(
                "Update a specific FiberLink MaaS360 policy information point",
                "{0}/{1}".format(uri, id),
                json_data,
                requires_modules=requires_modules, requires_version=requires_version
            )

    if update_required is False:
        logger.info("Input is the same as current PIP '{0}'.  Skipping update.".format(name))

    return isamAppliance.create_return_object()


def set(isamAppliance, name, properties, attributes=None, description=None, type="FiberLink MaaS360", new_name=None,
        check_mode=False, force=False):
    """
    Creating or Modifying a FiberLink MaaS360 PIP
    """
    ret_obj = search(isamAppliance, name=name)
    id = ret_obj['data']

    if id == {}:
        # If no id was found, Force the add
        return add(isamAppliance, name=name, properties=properties, attributes=attributes, description=description,
                   type=type, check_mode=check_mode, force=force)
    else:
        # Update PIP
        return update(isamAppliance, name=name, properties=properties, attributes=attributes, description=description,
                      type=type, new_name=new_name, check_mode=check_mode, force=force)
