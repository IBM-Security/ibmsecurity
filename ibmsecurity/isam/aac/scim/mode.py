import logging
from ibmsecurity.utilities.tools import json_sort
from ibmsecurity.isam.aac.scim.general import get

logger = logging.getLogger(__name__)

uri = "/mga/scim/configuration"
requires_modules = ["mga", "federation"]
requires_version = "9.0.2"

def set(isamAppliance, schema_name, scim_attribute, mode, scim_subattribute=None, check_mode=False,
                force=False):
    """
    Updating the mode of a SCIM attribute
    """

    ret_obj = get(isamAppliance)

    mode = mode.lower()

    objs = ret_obj['data']['attribute_modes']

    update_required = True

    if scim_subattribute is None:
        obj1 = {'mode': mode, 'attribute': scim_attribute}
    else:
        obj1 = {'mode': mode, 'attribute': scim_attribute, 'subattribute': scim_subattribute}

    obj1 = json_sort(obj1)

    for obj in objs:
        schema = obj['schema']
        if schema == schema_name:
            modes = obj['modes']
            for anitem in modes:
                obj2 = json_sort(anitem)
                if obj1 == obj2:
                    update_required = False

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:

            if scim_subattribute is None:
                return isamAppliance.invoke_put("Updating the mode of a SCIM attribute",
                                                "{0}/general/attribute_modes/{1}/{2}".format(uri, schema_name,
                                                                                             scim_attribute),
                                                {'mode': mode},
                                                requires_modules=requires_modules,
                                                requires_version=requires_version
                                                )
            else:
                return isamAppliance.invoke_put("Updating the mode of a SCIM attribute",
                                                "{0}/general/attribute_modes/{1}/{2}/{3}".format(uri, schema_name,
                                                                                                 scim_attribute,
                                                                                                 scim_subattribute),
                                                {'mode': mode},
                                                requires_modules=requires_modules,
                                                requires_version=requires_version
                                                )

    return isamAppliance.create_return_object(changed=False)


def reset(isamAppliance, schema_name, scim_attribute, scim_subattribute=None, check_mode=False, force=False):
    """
    Resetting a SCIM attribute mode to default
    """
    ret_obj = get(isamAppliance)

    objs = ret_obj['data']['attribute_modes']

    update_required = False

    for obj in objs:
        schema = obj['schema']
        if schema == schema_name:
            modes = obj['modes']
            for anitem in modes:
                if anitem['attribute'] == scim_attribute:
                    if scim_subattribute is not None:
                        if 'subattribute' in anitem:
                            if anitem['subattribute'] == scim_subattribute:
                                update_required = True
                    elif ('subattribute' in anitem) is False:
                        update_required = True


    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            if scim_subattribute is None:
                return isamAppliance.invoke_delete("Resetting a SCIM attribute mode to default",
                                               "{0}/general/attribute_modes/{1}/{2}".format(uri, schema_name,
                                                                                            scim_attribute),
                                               requires_modules=requires_modules,
                                               requires_version=requires_version
                                               )
            else:
                return isamAppliance.invoke_delete("Resetting a SCIM attribute mode to default",
                                               "{0}/general/attribute_modes/{1}/{2}/{3}".format(uri, schema_name,
                                                                                                scim_attribute,
                                                                                                scim_subattribute),
                                               requires_modules=requires_modules,
                                               requires_version=requires_version
                                               )

    return isamAppliance.create_return_object(changed=False)