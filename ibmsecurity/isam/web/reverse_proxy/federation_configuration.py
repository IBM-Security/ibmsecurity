import logging
import ibmsecurity.isam.fed.federations

logger = logging.getLogger(__name__)


def config(isamAppliance, instance_id, federation_id=None, federation_name=None, hostname='127.0.0.1', port='443', username=None,
           password=None, reuse_certs=False, reuse_acls=False, check_mode=False, force=False):
    """
    Federation configuration for a reverse proxy instance

    :param isamAppliance:
    :param instance_id:
    :param federation_id:
    :param federation_name:
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
    if username is None:
        logger.info("Required parameter username missing. Skipping config.")
        return isamAppliance.create_return_object(warning=["Required parameter username missing. Skipping config."])

    if password is None:
        logger.info("Required parameter password missing. Skipping config.")
        return isamAppliance.create_return_object(warning=["Required parameter password missing. Skipping config."])

    if federation_name is not None:
        ret_obj = ibmsecurity.isam.fed.federations.search(isamAppliance, name=federation_name, check_mode=check_mode,
                                                      force=force)
        federation_id = ret_obj['data']

        if federation_id == {}:
            logger.info("Federation {0}, not found. Skipping config.".format(federation_name))
            return isamAppliance.create_return_object()

    if federation_id is None:
        logger.info("Required parameter federation_id missing. Skipping config.")
        return isamAppliance.create_return_object()

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


def unconfig(isamAppliance, instance_id, federation_id=None, federation_name=None, check_mode=False, force=False):
    """
    Federation unconfiguration for a reverse proxy instance

    :param isamAppliance:
    :param instance_id:
    :param federation_id:
    :param federation_name:
    :param check_mode:
    :param force:
    :return:
    """

    if federation_name is not None:
        ret_obj = ibmsecurity.isam.fed.federations.search(isamAppliance, name=federation_name, check_mode=check_mode,
                                                      force=force)
        federation_id = ret_obj['data']

        if federation_id == {}:
            logger.info("Federation {0}, not found. Skipping config.".format(federation_name))
            return isamAppliance.create_return_object()

    if federation_id is None:
        logger.info("Required parameter federation_id missing. Skipping config.")
        return isamAppliance.create_return_object()

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
            logger.info("federation_id {0} found in reverse_proxy stanza isam-fed-autocfg.".format(federation_id))
            return True
    except:
        pass

    return False
