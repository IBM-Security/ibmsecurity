import logging
from ibmsecurity.isam.aac.policy_information_points.all import get, search
from ibmsecurity.utilities.tools import json_sort

logger = logging.getLogger(__name__)

# URI for this module
uri = "/iam/access/v8/pips"
requires_modules = ["mga"]
requires_version = None


def add(isamAppliance, name, properties, attributes=None, description=None, type="QRadar User Behavior Analytics",
        check_mode=False, force=False):
    """
    Create a QRadar User Behavior Analytics policy information point
    """
    ret_obj = search(isamAppliance, name, check_mode=False, force=False)
    id = ret_obj['data']

    if id != {}:
        logger.info("PIP '{0}' already exists.  Skipping add.".format(name))
        warning = "PIP '{0}' already exists.  Skipping add.".format(name)
        return isamAppliance.create_return_object(warnings=warning)

    if force is True or id == {}:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:

            return isamAppliance.invoke_post(
                "Create a JavaScript policy information point",
                "{0}".format(uri),
                _create_json(name=name, description=description, type=type,
                             attributes=attributes, properties=properties),
                requires_modules=requires_modules, requires_version=requires_version
            )

    return isamAppliance.create_return_object()


def update(isamAppliance, name, properties, attributes=None, description=None, new_name=None,
           type="QRadar User Behavior Analytics", check_mode=False, force=False):
    """
    Update a specific QRadar User Behavior Analytics policy information point
    """
    ret_obj = search(isamAppliance, name=name)
    id = ret_obj['data']
    update_required = False

    if id != {}:
        json_data = get(isamAppliance, name=name)

        if properties != None:
            current_props = json_data['data']['properties']
            json_sort(current_props)
            json_sort(properties)
            if current_props != properties:
                update_required = True

        if attributes != None:
            current_attrs = json_data['data']['attributes']
            json_sort(current_attrs)
            json_sort(attributes)
            if current_attrs != attributes:
                update_required = True

        if description != None:
            current_description = json_data['data']['description']
            if current_description != description:
                update_required = True

        if new_name != None:
            if name != new_name:
                name = new_name
                update_required = True

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)

        else:

            return isamAppliance.invoke_put(
                "Update a specific JavaScript policy information point",
                "{0}/{1}".format(uri, id),
                _create_json(name=name, description=description, type=type,
                             attributes=attributes, properties=properties),
                requires_modules=requires_modules, requires_version=requires_version
            )

    if id == {}:
        logger.info("PIP '{0}' does not exists.  Skipping update.".format(name))
        warning = "PIP '{0}' does not exists.  Skipping update.".format(name)
        return isamAppliance.create_return_object(warnings=warning)

    if update_required is False:
        logger.info("Input is the same as current PIP '{0}'.  Skipping update.".format(name))
        warning = "Input is the same as current PIP '{0}'.  Skipping update.".format(name)
        return isamAppliance.create_return_object(warnings=warning)

    return isamAppliance.create_return_object()


def set(isamAppliance, name, properties, attributes=None, description=None, new_name=None, type="QRadar User Behavior Analytics",
        check_mode=False, force=False):
    """
    Creating or Modifying a QRadar User Behavior Analytics
    """
    ret_obj = search(isamAppliance, name=name)
    id = ret_obj['data']

    if id == {}:
        # If no id was found, Force the add
        return add(isamAppliance, name=name, description=description, properties=properties, attributes=attributes,
                   type=type, check_mode=check_mode, force=force)
    else:
        # Update PIP
        return update(isamAppliance, name=name, new_name=new_name, description=description, properties=properties, attributes=attributes,
                      type=type, check_mode=check_mode, force=force)


def _create_json(name, description, type, attributes, properties):
    json_data = {
        "name": name,
        "description": description,
        "type": type
    }
    if attributes is not None:
        json_data['attributes'] = attributes
    if description is not None:
        json_data['description'] = description
    if properties is not None:
        json_data['properties'] = properties

    return json_data
