import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)

uri = "/wga/kerberos/config"
requires_modules = ["wga"]
requires_version = None


def get_kerberos_realm(isamAppliance, realm, check_mode=False, force=False):
    """
    Retrieve kerberos realm configuration
    """
    return isamAppliance.invoke_get(description="Retrieving kerberos configuration", uri="{0}/{1}".format(uri, "realms"),
                                    requires_modules=requires_modules, requires_version=requires_version)

def _check(isamAppliance, realm):
    """
    Check if kerberos realm is already created or not

    :param isamAppliance:
    :return:
    """
    ret_obj = get_kerberos_realm(isamAppliance, realm)

    logger.debug("Looking for existing kerberos realm in: {0}".format(ret_obj['data']))
    if ret_obj['data']:
        for krb in ret_obj['data']:
            if krb['name'] == realm:
                logger.debug("Found kerberos realm: {0}".format(realm))
                return True
    return False


def add_kerberos_realm(isamAppliance, realm, kdc, default_domain, admin_server, domain_realm, default_realm, check_mode=False, force=False):
    """
    Add kerberos realm
    :param isamAppliance:
    :return:
    """
    if _check(isamAppliance, realm) is True and force is False:
        return isamAppliance.create_return_object(warnings=["Found kerberos realm: {0}".format(realm)])
    if _check(isamAppliance, realm) is True and force is True:
        ret_obj = remove_kerberos_realm(isamAppliance, realm)
        if ret_obj['warnings']:
                logger.debug("Can't remove kerberos realm: {0}".format(realm))
                return isamAppliance.create_return_object(warnings=["Can't remove kerberos realm: {0}.{1}".format(realm,ret_obj['warnings'])])

    if force is True or _check(isamAppliance, realm) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post(description="Add kerberos realm", uri="{0}/{1}".format(uri, "realms"),
                                             data={
                                                 "subsection": realm
                                             },
                                             requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()

def config_kerberos_realm(isamAppliance, realm, kdc, default_domain, admin_server, domain_realm, default_realm, check_mode=False, force=False):
    """
    Add kerberos realm
    :param isamAppliance:
    :return:
    """
    # Add kdc configuration parameter
    ret_obj = set_realm_param(isamAppliance, realm, "realms/{0}".format(realm), 
                                "kdc", kdc, check_mode, force)
    if ret_obj['warnings']:
                logger.debug("Can't add kerberos parameter {0} - {1}".format("kdc", kdc))
                return isamAppliance.create_return_object("Can't add kerberos parameter {0} - {1}".format("kdc", kdc))

    # Add default domain configuration parameter
    ret_obj = set_realm_param(isamAppliance, realm, "realms/{0}".format(realm), 
                                "default_domain", default_domain, check_mode, force)
    if ret_obj['warnings']:
                logger.debug("Can't add kerberos parameter {0} - {1}".format("default_domain", default_domain))
                return isamAppliance.create_return_object("Can't add kerberos parameter {0} - {1}".format("default_domain", default_domain))

    ret_obj = set_realm_param(isamAppliance, realm, "realms/{0}".format(realm), 
                                "admin_server", admin_server, check_mode, force)
    if ret_obj['warnings']:
                logger.debug("Can't add kerberos parameter {0} - {1}".format("admin_server", admin_server))
                return isamAppliance.create_return_object("Can't add kerberos parameter {0} - {1}".format("admin_server", admin_server))

    ret_obj = set_domain_realm(isamAppliance, realm, "domain_realm", 
                                "domain_realm", domain_realm, check_mode, force)
    if ret_obj['warnings']:
                logger.debug("Can't configure domain realm {0} - {1}".format("domain_realm", domain_realm))
                return isamAppliance.create_return_object("Can't configure domain realm {0} - {1}".format("domain_realm", domain_realm))
    return isamAppliance.create_return_object()

    ret_obj = set_default_realm(isamAppliance, default_realm, check_mode, force)
    if ret_obj['warnings']:
                logger.debug("Can't update default realm {0} - {1}".format("libdefaults/default_realm", default_realm))
                return isamAppliance.create_return_object("Can't update default realm {0} - {1}".format("libdefaults/default_realm", default_realm))
    return isamAppliance.create_return_object()

def remove_kerberos_realm(isamAppliance, realm, check_mode=False, force=False):
    """
    Remove kerberos realm
    :param isamAppliance:
    :return:
    """
    if _check(isamAppliance, realm) is False:
        return isamAppliance.create_return_object(warnings=["Can't found kerberos realm: {0}".format(realm)])
    else:
        return isamAppliance.invoke_delete(description="Delete kerberos realm ", uri="{0}/{1}/{2}".format(uri, "realms",realm),
                                             requires_modules=requires_modules, requires_version=requires_version)
    return isamAppliance.create_return_object()

def get_kerberos_param(isamAppliance, paramuri, paramname, paramvalue, check_mode=False, force=False):
    """
    Retrieve kerberos param
    """
    return isamAppliance.invoke_get(description="Retrieving kerberos parameter {0} in : {1}".format(paramname,paramuri), uri="{0}/{1}".format(uri, paramuri),
                                    requires_modules=requires_modules, requires_version=requires_version)

def set_default_realm(isamAppliance, default_realm, check_mode=False, force=False):
    """
    Set kerberos default realm
    """
    return isamAppliance.invoke_put(description="Add default realm", uri="{0}/{1}".format(uri, "libdefaults/default_realm"),
                                             data={
                                                "id": "default_realm",
                                                 "value": default_realm
                                             },
                                             requires_modules=requires_modules, requires_version=requires_version)   

def _check_param(isamAppliance, paramuri, paramname, paramvalue):
    """
    Check if kerberos param is already created or not

    :param isamAppliance:
    :return:
    """
    ret_obj = get_kerberos_param(isamAppliance, paramuri, paramname, paramvalue)

    logger.debug("Looking for existing kerberos parameter {0} in: {1}".format(paramname,ret_obj['data']))
    if ret_obj['data']:
        for krb in ret_obj['data']:
            if krb['name'] == paramname:
                logger.debug("Found kerberos parameter: {0} - {1}".format(paramname, paramvalue))
                return True
    return False

def get_param_id(isamAppliance, paramuri, paramname, paramvalue):
    """
    Return kerberos parm id

    :param isamAppliance:
    :return:
    """
    ret_obj = get_kerberos_param(isamAppliance, paramuri, paramname, paramvalue)

    logger.debug("Looking for existing kerberos parameter {0} in: {1}".format(paramname,ret_obj['data']))
    if ret_obj['data']:
        for krb in ret_obj['data']:
            if krb['name'] == paramname:
                logger.debug("Found kerberos parameter: {0} - {1}".format(paramname, krb['id']))
                return krb['id']
    return False


def remove_kerberos_param(isamAppliance, realm, paramuri, paramname, paramvalue, check_mode=False, force=False):
    """
    Remove kerberos parameter
    :param isamAppliance:
    :return:
    """
    logger.debug(" Remove param uri = {0}".format(paramuri))

    if _check_param(isamAppliance, paramuri, paramname, paramvalue) is False or force is False:
        logger.debug(" Ignore remove = {0}".format(force))
        return isamAppliance.create_return_object(warnings=["Can't found kerberos param : {0}".format(paramname)])
    else:
        return isamAppliance.invoke_delete(description="Delete kerberos param ", uri="{0}/{1}".format(uri,paramuri),
                                             requires_modules=requires_modules, requires_version=requires_version)
    return isamAppliance.create_return_object()

def remove_domain_realm(isamAppliance, realm, domainname, check_mode=False, force=False):
    """
    Remove kerberos parameter
    :param isamAppliance:
    :return:
    """
    logger.debug(" Remove domain realm uri = domain_realm/{0}".format(domainname))

    paramuri = "domain_realm"
    if _check_param(isamAppliance, paramuri, domainname, domainname) is False or force is False:
        logger.debug(" Ignore remove = {0}".format(force))
        return isamAppliance.create_return_object(warnings=["Can't remove domain realm : {0}".format(domainname)])
    else:
        return isamAppliance.invoke_delete(description="Delete domain realm ", uri="{0}/domain_realm/{1}".format(uri,domainname),
                                             requires_modules=requires_modules, requires_version=requires_version)
    return isamAppliance.create_return_object()

def set_realm_param(isamAppliance, realm, paramuri, paramname, paramvalue, check_mode=False, force=False):
    """
    Set kerberos realm param

    :param isamAppliance:
    :return:
    """

    param_exists_flag = _check_param(isamAppliance, paramuri, paramname, paramvalue)

    if param_exists_flag is True and force is False:
        return isamAppliance.create_return_object(warnings=["Found kerberos parameter: {0} - {1}. Ignoring update.".format(paramname,paramvalue)])

    if param_exists_flag is False or force is True:
        if param_exists_flag is True:
            ret_obj = remove_kerberos_param(isamAppliance, realm, paramuri, paramname, paramvalue, check_mode, force)

        if isinstance(paramvalue, basestring): 
            return isamAppliance.invoke_post(description="Add kerberos param", uri="{0}/{1}".format(uri, paramuri),
                                             data={
                                                 "name": paramname,
                                                 "value": paramvalue
                                             },
                                             requires_modules=requires_modules, requires_version=requires_version)
        else:
            paramcycle = 0
            for paramStr in paramvalue:
                if paramcycle == 0:
                    paramcycle = paramcycle + 1
                    isamAppliance.invoke_post(description="Add kerberos param", uri="{0}/{1}".format(uri, paramuri),
                                             data={
                                                 "name": paramname,
                                                 "value": paramStr
                                             },
                                             requires_modules=requires_modules, requires_version=requires_version)
                else:
                    #paramID = get_param_id(isamAppliance, paramuri, paramname, paramvalue)
                    ret_obj = isamAppliance.invoke_put(description="Add kerberos param value", uri="{0}/{1}".format(uri, paramuri),
                                             data={
                                                 "name": paramname,
                                                 "value": paramStr
                                             },
                                             requires_modules=requires_modules, requires_version=requires_version)   

    return isamAppliance.create_return_object()

def set_domain_realm(isamAppliance, realm, paramuri, paramname, paramvalue, check_mode=False, force=False):
    """
    Configure domain realms

    :param isamAppliance:
    :return:
    """
    param_exists_flag = _check_param(isamAppliance, paramuri, paramname, paramvalue)

    if param_exists_flag is True and force is False:
        return isamAppliance.create_return_object(warnings=["Found domain realm: {0} - {1}. Ignoring update.".format(paramname,paramvalue)])

    else:

        if isinstance(paramvalue, basestring): 
            param_exists_flag = _check_param(isamAppliance, paramuri, paramvalue, paramvalue)
            if param_exists_flag is True and force is False:
                return isamAppliance.create_return_object(warnings=["Found domain realm: {0} - {1}. Ignoring update.".format(paramvalue,realm)])
            if param_exists_flag is True and force is True:
                paramuri = paramuri + "/" + paramvalue
                ret_obj = remove_domain_realm(isamAppliance, realm, paramvalue, check_mode, force)
            return isamAppliance.invoke_post(description="Add domain realm", uri="{0}/{1}".format(uri, paramuri),
                                             data={
                                                 "name": paramvalue,
                                                 "value": realm
                                             },
                                             requires_modules=requires_modules, requires_version=requires_version)
        else:
            for paramStr in paramvalue:
                param_exists_flag = _check_param(isamAppliance, paramuri, paramStr, paramvalue)
                if param_exists_flag is True and force is False:
                    return isamAppliance.create_return_object(warnings=["Found domain realm: {0} - {1}. Ignoring update.".format(paramStr,realm)])
                if param_exists_flag is True and force is True:
                    ret_obj = remove_domain_realm(isamAppliance, realm, paramStr, check_mode, force)                                              
                isamAppliance.invoke_post(description="Add domain realm", uri="{0}/{1}".format(uri, paramuri),
                                             data={
                                                 "name": paramStr,
                                                 "value": realm
                                             },
                                             requires_modules=requires_modules, requires_version=requires_version)
    return isamAppliance.create_return_object()
