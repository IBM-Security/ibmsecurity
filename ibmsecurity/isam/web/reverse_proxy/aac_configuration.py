import logging

logger = logging.getLogger(__name__)
requires_modules = ["wga"]
requires_version = "9.0.4.0"


def config(isamAppliance, instance_id, hostname='localhost', port=443, username='easuser',
           password='passw0rd', junction="/mga", reuse_acls=None, reuse_certs=None,
           check_mode=False, force=False):
    """
    AAC CBA configuration for a reverse proxy instance
    """
    if force is True or _check_config(isamAppliance, instance_id) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            json_data = {
                "junction": junction,
                "hostname": hostname,
                "port": port,
                "username": username,
                "password": password
            }
            # Add optional values to the JSON
            if reuse_acls is not None and reuse_acls != '':
                json_data['reuse_acls'] = reuse_acls
            if reuse_certs is not None and reuse_certs != '':
                json_data['reuse_certs'] = reuse_certs
            return isamAppliance.invoke_post(
                "AAC CBA configuration for a reverse proxy instance",
                "/wga/reverseproxy/{0}/authsvc_config".format(instance_id), json_data,
                requires_modules=requires_modules, requires_version=requires_version)

        return isamAppliance.create_return_object()


def unconfig(isamAppliance, instance_id, check_mode=False, force=False):
    """
    AAC CBA unconfiguration for a reverse proxy instance
    """
    if force is True or _check_config(isamAppliance, instance_id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "AAC CBA configuration for a reverse proxy instance",
                "/wga/reverseproxy/{0}/authsvc_config".format(instance_id),
                requires_modules=requires_modules, requires_version=requires_version)

        return isamAppliance.create_return_object()


def _check_config(isamAppliance, instance_id):
    """
    TODO: Need to code this function to check if Oauth is already configured - one option is to check for existince of junction

    :param isamAppliance:
    :param instance_id:
    :return:
    """
    return False
