import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/wga/kerberos/config/realms"
requires_modules = ['wga']
requires_version = None
import ibmsecurity.isam.web.kerberos_configuration.realms as realms
import ibmsecurity.isam.web.kerberos_configuration.realms_subsection as subsections


def search(isamAppliance, realm, propname, subsection=None, includeValuesInLine='yes', check_mode=False, force=False):
    """
    Search kerberos realm property by name
    """
    if subsection is None:
        uriprop = "{0}".format(realm)
        subsection = "NA"
    else:
        uriprop = "{0}/{1}".format(realm, subsection)

    logger.info("property to search under: {0} where property is: {1}".format(uriprop, propname))
    ret_obj = isamAppliance.invoke_get("Retrieve realm configuration", "{0}/{1}{2}".format(uri, realm,
                                                                                           tools.create_query_string(
                                                                                               includeValuesInLine=includeValuesInLine)),
                                       requires_modules=requires_modules, requires_version=requires_version)

    return_obj = isamAppliance.create_return_object()
    return_obj["warnings"] = ret_obj["warnings"]
    return_obj['data'] = {}

    for obj in ret_obj['data']:
        if obj['type'] == "property":
            if "{0} = ".format(propname) in obj['name']:
                logger.info("Found Kerberos realm property {0} id: {1}".format(propname, obj['id']))
                return_obj['data']['name'] = obj['name']
                return_obj['data']['id'] = obj['id']
                return_obj['rc'] = 0
                break

    return return_obj


def _check(isamAppliance, realm, propname, propvalue, subsection=None):
    """
    Check if kerberos realm's property with given value is already created or not

    :param isamAppliance:
    :return:
    """

    propstring = "{0} = {1}".format(propname, propvalue)

    ret_obj = search(isamAppliance, realm, propname, subsection)
    logger.debug("Looking for existing kerberos property {0} in {1}".format(propname, ret_obj['data']))
    if ret_obj['data'] != {}:
        if ret_obj['data']['name'] == propstring:
            logger.debug("Found kerberos property: {0} in : {1}".format(propname, ret_obj['data']))
            return True
    return False


def add(isamAppliance, realm, propname, propvalue, subsection=None, check_mode=False, force=False):
    """
            Add kerberos realm's property
            realm and subsection if passed needs to exist
            :param isamAppliance:
            :return:
         """
    if subsection is None:
        uriprop = realm
    else:
        uriprop = "{0}/{1}".format(realm, subsection)

    if realms.search(isamAppliance, realm) == {}:
        return isamAppliance.create_return_object(warnings=["Realm: {0} does not exists: ".format(realm)])

    if subsection is not None and subsections._check(isamAppliance, realm, subsection) is False:
        return isamAppliance.create_return_object(
            warnings=["Subsection: {0}/{1} does not exists.".format(realm, subsection)])

    if force is False and _check(isamAppliance, realm, propname, propvalue, subsection) is True:
        return isamAppliance.create_return_object(
            warnings=["Property: {0} with value: {1} already exists: ".format(uriprop, propvalue)])

    if force is True or _check(isamAppliance, realm, propname, propvalue, subsection) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post("Add kerberos real property", "{0}/{1}".format(uri, uriprop),
                                             {
                                                 "name": propname,
                                                 "value": propvalue
                                             },
                                             requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()


def delete(isamAppliance, realm, propname, subsection=None, check_mode=False, force=False):
    """
    Remove kerberos realms property
    :param isamAppliance:
    :return:
    """
    if realms.search(isamAppliance, realm) == {}:
        return isamAppliance.create_return_object(warnings=["Realm: {0} does not exists: ".format(realm)])

    if subsection is None:
        uriprop = realm
    else:
        uriprop = "{0}/{1}".format(realm, subsection)

    logger.debug(" Remove param uri = {0}/{1}/{2}".format(uri, uriprop, propname))
    ret_obj = search(isamAppliance, realm, propname, subsection)

    if ret_obj['data'] == {} and force is False:
        return isamAppliance.create_return_object(
            warnings=["property: {0} not found or force is: {1}".format(propname, force)])
    else:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(description="Delete kerberos realm prop ",
                                               uri="{0}/{1}/{2}".format(uri, uriprop, propname),
                                               requires_modules=requires_modules, requires_version=requires_version)


def update(isamAppliance, realm, propname, propvalue, subsection=None, check_mode=False, force=False):
    """
    Set kerberos realm property

    :param isamAppliance:
    :return:
    """
    if subsection is None:
        uriprop = realm
    else:
        uriprop = "{0}/{1}".format(realm, subsection)

    if realms.search(isamAppliance, realm) == {}:
        return isamAppliance.create_return_object(warnings=["Realm: {0} does not exists: ".format(realm)])

    if subsection is not None and subsections._check(isamAppliance, realm, subsection) is False:
        return isamAppliance.create_return_object(
            warnings=["Subsection: {0}/{1} does not exists.".format(realm, subsection)])

    ret_obj = search(isamAppliance, realm, propname, subsection)
    warnings = ret_obj["warnings"]

    if ret_obj["data"] == {}:
        warnings.append("Property {0} not found, skipping update.".format(propname))
        return isamAppliance.create_return_object(warnings=warnings)

    needs_update = False

    propstring = "{0} = {1}".format(propname, propvalue)

    if force is not True:
        if ret_obj['data']['name'] != propstring:
            needs_update = True

    if force is True or needs_update is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            idval = "/{0}/{1}".format(uriprop, propname)
            return isamAppliance.invoke_put(description="Add kerberos param value",
                                            uri="{0}/{1}/{2}".format(uri, uriprop, propname),
                                            data={
                                                "id": idval,
                                                "value": propvalue
                                            },
                                            requires_modules=requires_modules, requires_version=requires_version,
                                            warnings=warnings)
    return isamAppliance.create_return_object(warnings=warnings)


def set(isamAppliance, realm, propname, propvalue, subsection=None, check_mode=False, force=False):
    """
    Set kerberos realm property

    :param isamAppliance:
    :return:
    """
    if realms.search(isamAppliance, realm) == {}:
        return isamAppliance.create_return_object(warnings=["Realm: {0} does not exists: ".format(realm)])

    if subsection is not None and subsections._check(isamAppliance, realm, subsection) is False:
        return isamAppliance.create_return_object(
            warnings=["Subsection: {0}/{1} does not exists.".format(realm, subsection)])

    ret_obj = search(isamAppliance, realm, propname, subsection)

    if ret_obj["data"] == {}:
        return add(isamAppliance, realm, propname, propvalue, subsection, check_mode, force=True)

    return update(isamAppliance, realm, propname, propvalue, subsection, check_mode, force)
