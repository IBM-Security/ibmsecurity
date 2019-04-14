import logging
from ibmsecurity.isam.web.reverse_proxy import junctions

logger = logging.getLogger(__name__)
requires_modules = ["wga"]
requires_version = "9.0.6.0"


def config(isamAppliance, instance_id, hostname='127.0.0.1', port=443, username='easuser', password='passw0rd',
           junction="/mga", reuse_certs=False, reuse_acls=False, check_mode=False, force=False):
    """
    Authentication and Context based access configuration for a reverse proxy instance

    :param isamAppliance:
    :param instance_id:
    :param junction:
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
    warnings = [
        "Idempotency logic will check for existence of {} junction. Use force=True to override.".format(junction)]
    if force is True or _check_config(isamAppliance, instance_id, junction) is False:
        json_data = {
            "junction": junction,
            "hostname": hostname,
            "port": port,
            "username": username,
            "password": password,
            "reuse_certs": reuse_certs,
            "reuse_acls": reuse_acls
        }
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_post(
                " Authentication and Context based access configuration for a reverse proxy instance",
                "/wga/reverseproxy/{}/authsvc_config".format(instance_id), json_data, warnings=warnings,
                requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object(warnings=warnings)


def _check_config(isamAppliance, instance_id, junction):
    """
    Check if the junction for aac already created

    :param isamAppliance:
    :param instance_id:
    :param junction:
    :return:
    """
    ret_obj = junctions.get_all(isamAppliance, instance_id)

    for j in ret_obj['data']:
        if j['id'] == junction:
            logger.info("Junction {} was found - hence aac config must have already executed.".format(junction))
            return True

    return False
