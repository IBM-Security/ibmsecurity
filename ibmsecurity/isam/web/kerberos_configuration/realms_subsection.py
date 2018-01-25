import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/wga/kerberos/config/realms"
requires_modules = ['wga']
requires_version = None
import ibmsecurity.isam.web.kerberos_configuration.realms as realms


def search(isamAppliance, realm, subsection, check_mode=False, force=False):
    """
    Search kerberos realm subsection by name
    """
    logger.info("subsection to search under: {0} is: {1} ".format(realm, subsection))
    ret_obj = realms._get(isamAppliance, realm)
    return_obj = isamAppliance.create_return_object()
    return_obj["warnings"] = ret_obj["warnings"]

    for obj in ret_obj['data']:
        if obj['type'] == "section":
            if obj['name'] == subsection:
                logger.info("Found Kerberos realm subsection {0} id: {1}".format(subsection, obj['id']))
                return_obj['data'] = obj
                return_obj['rc'] = 0
                break

    return return_obj


def _check(isamAppliance, realm, subsection):
    """
    Check if kerberos realm's subsection is already created or not

    :param isamAppliance:
    :return:
    """
    ret_obj = _search(isamAppliance, realm, subsection)

    realm = "{0}/{1}".format("realms", realm)

    logger.debug("Looking for existing kerberos subsection: {1} in realm: {0} in: {2}".format(realm, subsection,
                                                                                              ret_obj['data']))
    if ret_obj['data'] != {}:
        if ret_obj['data']['name'] == subsection and ret_obj['data']['parent'] == realm:
            logger.debug("Found kerberos realm's subsection: {0}".format(subsection))
            return True
    return False


def add(isamAppliance, realm, subsection, check_mode=False, force=False):
    """
        Add kerberos realm's subsection
        :param isamAppliance:
        :return:
     """
    check_realm = realms.search(isamAppliance, realm)

    if check_realm == {}:
        return isamAppliance.create_return_object(warnings=["Kerberos realm: {0} not found".format(realm)])

    check_subsection = _check(isamAppliance, realm, subsection)

    if check_subsection is True and force is False:
        return isamAppliance.create_return_object(
            warnings=["Kerberos subsection {1} in realm: {0} already exists".format(realm, subsection)])

    if force is True or check_subsection is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post("Add kerberos realm's subsection", "{0}/{1}".format(uri, realm),
                                             {
                                                 "subsection": subsection
                                             },
                                             requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()


def delete(isamAppliance, realm, subsection, check_mode=False, force=False):
    """
    Remove kerberos realms subsection
    :param isamAppliance:
    :return:
    """
    logger.debug(" Remove param uri = {0}/{1}/{2}".format(uri, realm, subsection))

    if realms.search(isamAppliance, realm) == {} and force is False:
        return isamAppliance.create_return_object(warnings=["Realm: {0} does not exists: ".format(realm)])

    if _check(isamAppliance, realm, subsection) is False and force is False:
        return isamAppliance.create_return_object(warnings=["subsection: {0} not found".format(subsection)])
    else:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(description="Delete kerberos realm subsection ",
                                               uri="{0}/{1}/{2}".format(uri, realm, subsection),
                                               requires_modules=requires_modules, requires_version=requires_version)
