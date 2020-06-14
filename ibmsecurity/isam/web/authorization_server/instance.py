import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)

uri = "/isam/authzserver"
requires_modules = None
requires_version = None
version = "v1"
requires_model = "Appliance"


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieve all authorization servers
    """
    return isamAppliance.invoke_get(description="Retrieving all authorization servers",
                                    uri="{0}/{1}".format(uri, version),
                                    requires_modules=requires_modules,
                                    requires_version=requires_version,
                                    requires_model=requires_model)


def _check(isamAppliance, id):
    """
    Check if authorization server is already created or not

    :param isamAppliance:
    :return:
    """
    ret_obj = get(isamAppliance)
    azsrv_exists, warnings = False, ret_obj['warnings']

    if not warnings:
        logger.debug("Looking for existing authorization servers in: {0}".format(ret_obj['data']))
        if ret_obj['data']:
            for acld in ret_obj['data']:
                if acld['id'] == id:
                    logger.debug("Found authorization server: {0}".format(id))
                    azsrv_exists = True

    return azsrv_exists, warnings


def add(isamAppliance, inst_name, admin_pwd, addresses, hostname='localhost', authport='7136', adminport='7137',
        domain='Default',
        admin_id='sec_master', ssl='no', ssl_port=None, keyfile=None, keyfile_label=None, check_mode=False,
        force=False):
    """
    Add an authorization server

    :param isamAppliance, inst_name, admin_pwd, addresses:
    :return:
    """
    azsrv_exists, warnings = _check(isamAppliance, inst_name)

    if warnings:
        return isamAppliance.create_return_object(warnings=warnings)

    if force is True or azsrv_exists is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_post(description="Add an authorization server",
                                             uri="{0}/{1}".format(uri, version),
                                             data={
                                                 "inst_name": inst_name,
                                                 "hostname": hostname,
                                                 "authport": authport,
                                                 "adminport": adminport,
                                                 "domain": domain,
                                                 "admin_id": admin_id,
                                                 "admin_pwd": admin_pwd,
                                                 "addresses": addresses,
                                                 "ssl": ssl,
                                                 "ssl_port": ssl_port,
                                                 "keyfile": keyfile,
                                                 "keyfile_label": keyfile_label
                                             },
                                             requires_modules=requires_modules,
                                             requires_version=requires_version,
                                             requires_model=requires_model)

    return isamAppliance.create_return_object(warnings="Authorization server {0} already exists".format(inst_name))


def delete(isamAppliance, id, admin_pwd, admin_id='sec_master', check_mode=False, force=False):
    """
    Unconfigure existing runtime component
    """

    azsrv_exists, warnings = _check(isamAppliance, id)

    if warnings:
        return isamAppliance.create_return_object(warnings=warnings)

    if force is True or force == "yes" or azsrv_exists is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            force_yn = "no"
            if force is True or force == "yes":
                force_yn = "yes"
            return isamAppliance.invoke_put(description="Remove a authorization server",
                                            uri="{0}/{1}/{2}".format(uri, id, version),
                                            data={
                                                "operation": "unconfigure",
                                                "force": force_yn,
                                                "admin_id": admin_id,
                                                "admin_pwd": admin_pwd
                                            },
                                            requires_modules=requires_modules,
                                            requires_version=requires_version,
                                            requires_model=requires_model)

    return isamAppliance.create_return_object(
        warnings="The authorization server instance specified in the request does not exist. Check that the authorization server instance is correct: {0}".format(
            id))


def execute(isamAppliance, id, operation="restart", admin_id="sec_master", admin_pwd=None, check_mode=False,
            force=False, warnings=[]):
    """
    Execute an operation on runtime component

    :param isamAppliance:
    :param operation:
    :return:
    """
    ret_obj = get(isamAppliance)
    warnings = ret_obj['warnings']
    if warnings and 'Docker' in warnings[0]:
        return isamAppliance.create_return_object(warnings=ret_obj['warnings'])

    for acld in ret_obj['data']:
        if acld['id'] == id:
            if (force is True or
                    (acld['restart'] == "true" and operation == "restart") or
                    (acld['started'] == 'yes' and operation == "stop") or
                    (acld['started'] == 'no' and operation == "start") or
                    (operation == "renew")):
                if check_mode is True:
                    return isamAppliance.create_return_object(changed=True)
                else:
                    body_json = {
                        "operation": operation
                    }
                    if operation == "renew":
                        if admin_pwd is not None:
                            body_json["admin_id"] = admin_id
                            body_json["admin_pwd"] = admin_pwd
                        else:
                            warnings.append("admin_pwd must be specified when operation is renew")
                            return isamAppliance.create_return_object(warnings=warnings)
                    return isamAppliance.invoke_put(description="Execute an operation on authorization server",
                                                    uri="{0}/{1}/{2}".format(uri, id, version),
                                                    data=body_json,
                                                    requires_modules=requires_modules,
                                                    requires_version=requires_version, warnings=warnings)
            break
    if _check(isamAppliance, id) is False:
        return isamAppliance.create_return_object(
            warnings="The authorization server instance specified in the request does not exist. Check that the authorization server instance is correct: {0}".format(
                id))
    else:
        return isamAppliance.create_return_object()


def compare(isamAppliance1, isamAppliance2):
    """
    Compare list of authorization servers between 2 appliances
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    for acld in ret_obj1['data']:
        del acld['started']
        del acld['restart']
        del acld['version']
    for acld in ret_obj2['data']:
        del acld['started']
        del acld['restart']
        del acld['version']

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['restart', 'started', 'version'])
