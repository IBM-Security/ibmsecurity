import logging

logger = logging.getLogger(__name__)
requires_modules = ["wga"]
requires_version = "9.0.4.0"


def config(isamAppliance, instance_id, hostname='127.0.0.1', port=443, username='easuser', password='passw0rd',
           junction="/mga", reuse_certs=False, reuse_acls=False, api=False, browser=True, check_mode=False,
           force=False):
    """
    Oauth and Oidc configuration for a reverse proxy instance

    :param isamAppliance:
    :param instance_id:
	:param junction:
    :param hostname:
    :param port:
    :param username:
    :param password:
    :param reuse_certs:
    :param reuse_acls:
    :param api:
    :param browser:
    :param check_mode:
    :param force:
    :return:
    """
    if force is True or _check_config(isamAppliance, instance_id) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post(
                "OAuth configuration for a reverse proxy instance",
                "/wga/reverseproxy/{0}/oauth_config".format(instance_id),
                {
                    "junction": junction,
                    "hostname": hostname,
                    "port": port,
                    "username": username,
                    "password": password,
                    "api": api,
                    "browser": browser,
                    "reuse_certs": reuse_certs,
                    "reuse_acls": reuse_acls
                },
                requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()


def _check_config(isamAppliance, instance_id):
    """
    TODO: Need to code this function to check if Oauth is already configured - one option is to check for existince of /mga junction

    :param isamAppliance:
    :param instance_id:
    :return:
    """
    return False
