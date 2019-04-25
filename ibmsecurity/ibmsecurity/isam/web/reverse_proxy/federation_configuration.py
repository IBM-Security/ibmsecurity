import logging

logger = logging.getLogger(__name__)


def config(isamAppliance, instance_id, federation_id, hostname='127.0.0.1', port=443, username='easuser',
           password='passw0rd', reuse_certs=False, reuse_acls=False, check_mode=False, force=False):
    """
    Federation configuration for a reverse proxy instance

    :param isamAppliance:
    :param instance_id:
    :param federation_id:
    :param hostname:
    :param port:
    :param username:
    :param password:
    :param reuse_certs:
    :param reuse_acls:
    :param check_mode:
    :param force:
    :return:
    """
    if force is True or _check(isamAppliance, instance_id, federation_id) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post(
                "Federation configuration for a reverse proxy instance",
                "/wga/reverseproxy/{0}/fed_config".format(instance_id),
                {
                    "runtime": {
                        "hostname": hostname,
                        "port": port,
                        "username": username,
                        "password": password
                    },
                    "federation_id": federation_id,
                    "reuse_certs": reuse_certs,
                    "reuse_acls": reuse_acls
                })

    return isamAppliance.create_return_object()


def unconfig(isamAppliance, instance_id, federation_id, check_mode=False, force=False):
    """
    Federation unconfiguration for a reverse proxy instance

    :param isamAppliance:
    :param instance_id:
    :param federation_id:
    :param check_mode:
    :param force:
    :return:
    """
    if force is True or _check(isamAppliance, instance_id, federation_id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Federation unconfiguration for a reverse proxy instance",
                "/wga/reverseproxy/{0}/fed_config/{1}".format(instance_id, federation_id))

    return isamAppliance.create_return_object()


def _check(isamappliance, instance_id, federation_id):
    # WebSEAL has a stanza that should contain the configured federations
    from ibmsecurity.isam.web.reverse_proxy.configuration import entry
    ret_obj = entry.get_all(isamappliance, reverseproxy_id=instance_id, stanza_id="isam-fed-autocfg")

    # IF there is any exception - i.e. stanza not found return False
    try:
        if federation_id in ret_obj['data']:
            return True
    except:
        pass

    return False
