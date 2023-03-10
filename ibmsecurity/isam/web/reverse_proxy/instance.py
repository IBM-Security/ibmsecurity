import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)

uri = "/wga/reverseproxy"
requires_modules = ["wga"]
requires_version = None


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieve all reverse proxies
    """
    return isamAppliance.invoke_get(description="Retrieving all reverse proxies", uri=uri,
                                    requires_modules=requires_modules, requires_version=requires_version)


def _check(isamAppliance, id):
    """
    Check if reverse proxy is already created or not

    :param isamAppliance:
    :return:
    """
    ret_obj = get(isamAppliance)

    logger.debug("Looking for existing reverse proxies in: {0}".format(ret_obj['data']))
    if ret_obj['data']:
        for rp in ret_obj['data']:
            if rp['id'] == id:
                logger.debug("Found reverse proxy: {0}".format(id))
                return True

    return False


def add(isamAppliance, inst_name, admin_pwd, host='localhost', listening_port='7234', domain='Default',
        admin_id='sec_master', ssl_yn='no', key_file=None, cert_label=None, ssl_port=None, http_yn='no', http_port='80',
        https_yn='yes', https_port='443', nw_interface_yn='no', ip_address='0.0.0.0', check_mode=False, force=False):
    """
    Add a reverse proxy

    :param isamAppliance:
    :return:
    """
    if force is True or _check(isamAppliance, inst_name) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post(description="Add a reverse proxy", uri=uri,
                                             data={
                                                 "inst_name": inst_name,
                                                 "host": host,
                                                 "listening_port": listening_port,
                                                 "domain": domain,
                                                 "admin_id": admin_id,
                                                 "admin_pwd": admin_pwd,
                                                 "ssl_yn": ssl_yn,
                                                 "key_file": key_file,
                                                 "cert_label": cert_label,
                                                 "ssl_port": ssl_port,
                                                 "http_yn": http_yn,
                                                 "http_port": http_port,
                                                 "https_yn": https_yn,
                                                 "https_port": https_port,
                                                 "nw_interface_yn": nw_interface_yn,
                                                 "ip_address": ip_address
                                             },
                                             requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()


def delete(isamAppliance, id, admin_pwd, admin_id='sec_master', domain='Default', check_mode=False, force=False):
    """
    Unconfigure existing runtime component
    """
    if force is True or _check(isamAppliance, id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(description="Remove a reverse proxy",
                                            uri="{0}/{1}".format(uri, id),
                                            data={
                                                "operation": "unconfigure",
                                                "admin_id": admin_id,
                                                "admin_pwd": admin_pwd,
                                                "domain": domain
                                            },
                                            requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()


def import_config(isamAppliance, id, file, overwrite=True, check_mode=False, force=False):
    """
    Import or migrate reverse proxy
    """
    if force is True or _check(isamAppliance, id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post_files(description="Import or Migrate reverse proxy",
                                                   uri="{0}/{1}/migrate".format(uri, id),
                                                   fileinfo=[{
                                                       'file_formfield': 'file',
                                                       'filename': file,
                                                       'mimetype': 'application/octet-stream'
                                                   }],
                                                   data={'overwrite': overwrite},
                                                   requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()


def export_config(isamAppliance, id, filename, check_mode=False, force=False):
    """
    Export a Reverse Proxy Configuration
        -id is the name of the reverse proxy instance
        -filename is file system location to export the file (e.g. /tmp/webseal_config.zip)
    """
    import os.path
    if force is True or os.path.exists(os.path.dirname(filename)) is True:
        if check_mode is True:  # No point downloading a file if in check_mode
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_get_file(
                description="Export a Reverse Proxy Configuration",
                uri="{0}/{1}?action=export".format(uri, id),
                filename=filename)

    return isamAppliance.create_return_object()


def execute(isamAppliance, id, operation="restart", check_mode=False, force=False):
    """
    Execute an operation on runtime component

    :param isamAppliance:
    :param operation:
    :return:
    """
    ret_obj = get(isamAppliance)

    for rp in ret_obj['data']:
        if rp['id'] == id:
            if (force is True or
                    (rp['restart'] == "true" and operation == "restart") or
                    (rp['started'] == 'yes' and operation == "stop") or
                    (rp['started'] == 'no' and operation == "start")):
                if check_mode is True:
                    return isamAppliance.create_return_object(changed=True)
                else:
                    return isamAppliance.invoke_put(description="Execute an operation on reverse proxy",
                                                    uri="{0}/{1}".format(uri, id),
                                                    data={
                                                        "operation": operation
                                                    },
                                                    requires_modules=requires_modules,
                                                    requires_version=requires_version)
            break

    return isamAppliance.create_return_object()


def execute_multiples(isamAppliance, instances, operation, check_mode=False, force=False):
    """
    Stopping, starting, or restarting multiple instances

    :param isamAppliance:
    :param operation:
    :return:
    """
    ret_obj = get(isamAppliance)
    new_instances = []

    for instance in instances:
        for rp in ret_obj['data']:
            if rp['id'] == instance['instance_name']:
                if ((rp['restart'] == "true" and operation == "restart") or
                        (rp['started'] == 'yes' and operation == "stop") or
                        (rp['started'] == 'no' and operation == "start")):
                    new_instances.append(instance)

    if force is True or len(new_instances) >= 1:

        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        elif len(new_instances) > 1:
            return isamAppliance.invoke_put("Stopping, starting, or restarting multiple instances",
                                            "{0}".format(uri),
                                            {
                                                "operation": operation,
                                                "instances": new_instances
                                            },
                                            requires_modules=requires_modules,
                                            requires_version=requires_version)
        elif len(new_instances) == 1:
            execute(isamAppliance, new_instances[0]['instance_name'], operation=operation, check_mode=check_mode,
                    force=force)

    return isamAppliance.create_return_object()


def obfuscating(isamAppliance, id, pwd, check_mode=False, force=False):
    """
    Obfuscating a GSO password
    Must set gso-obfuscation-key in the config file for the password to be obfuscated.
    https://www.ibm.com/support/knowledgecenter/SSPREK_9.0.6/com.ibm.isam.doc/wrp_stza_ref/reference/ref_gso_obfuscation_key.html
    """
    return isamAppliance.invoke_post("Obfuscating a GSO password",
                                     "{0}/{1}?action=obfuscate_gso_pwd".format(uri, id),
                                     {
                                         "pwd": pwd
                                     },
                                     requires_modules=requires_modules, requires_version=requires_version)


def renew_cert(isamAppliance, id, isamUser, check_mode=False, force=False):
    """
    Renew a reverse proxy instance management certificate
    """
    return isamAppliance.invoke_put("Renew a reverse proxy instance management certificate",
                                    "{0}/{1}".format(uri, id),
                                    {
                                        "admin_id": isamUser.username,
                                        "admin_pwd": isamUser.password,
                                        "operation": "renew"
                                    },
                                    requires_modules=requires_modules, requires_version=requires_version)


def compare(isamAppliance1, isamAppliance2):
    """
    Compare list of reverse proxies between 2 appliances
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    for rp in ret_obj1['data']:
        del rp['started']
        del rp['restart']
        del rp['version']
    for rp in ret_obj2['data']:
        del rp['started']
        del rp['restart']
        del rp['version']

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['restart', 'started', 'version'])
