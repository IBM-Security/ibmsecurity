import logging
import ibmsecurity.utilities.tools
from ibmsecurity.isam.web.reverse_proxy import junctions

logger = logging.getLogger(__name__)
requires_modules = ["wga"]
requires_version = "10.0.4.0"


def config(isamAppliance, instance_id, hostname='127.0.0.1', port=443,
           junction="/isvaop", enable_mtls=None, mutual_key_label=None, reuse_certs=False,
           reuse_acls=False, load_certificate=True,
           check_mode=False, force=False):
    """
    OAuth2 IBM Security Verify OIDC Provider configuration

    :param isamAppliance:
    :param instance_id:
    :param junction:
    :param hostname:
    :param port:
    :param enable_mtls # new in 10.0.8
    :param mutual_key_label # new in 10.0.8
    :param reuse_certs:
    :param reuse_acls:
    :param check_mode:
    :param force:
    :param load_certificate # new in ?  Default is true
    :return:
    """

    warnings = [
        f"Idempotency logic will check for existence of {junction} junction. Use force=True to override."]
    if force or _check_config(isamAppliance, instance_id, junction) is False:
        json_data = {
            "junction": junction,
            "hostname": hostname,
            "port": port,
            "reuse_certs": reuse_certs,
            "reuse_acls": reuse_acls,
            "load_certificate": load_certificate
        }
        if enable_mtls is not None:
            if ibmsecurity.utilities.tools.version_compare(isamAppliance.facts["version"], "10.0.8.0") < 0:
                warnings.append(
                    f"Appliance at version: {isamAppliance.facts['version']}, enable_mtls: {enable_mtls} is not supported. Needs 10.0.8.0 or higher. Ignoring enable_mtls for this call.")
            else:
                json_data["enable_mtls"] = enable_mtls
        if mutual_key_label is not None:
            if ibmsecurity.utilities.tools.version_compare(isamAppliance.facts["version"], "10.0.8.0") < 0:
                warnings.append(
                    f"Appliance at version: {isamAppliance.facts['version']}, mutual_key_label: {mutual_key_label} is not supported. Needs 10.0.8.0 or higher. Ignoring mutual_key_label for this call.")
            else:
                json_data["mutual_key_label"] = mutual_key_label
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_post(
                "OAuth2 IBM Security Verify OIDC Provider configuration for a reverse proxy instance",
                f"/wga/reverseproxy/{instance_id}/oauth2_config",
                json_data,
                warnings=warnings,
                requires_modules=requires_modules, requires_version=requires_version)
    return isamAppliance.create_return_object(warnings=warnings)

def _check_config(isamAppliance, instance_id, junction):
    """
    Check if the junction for oauth already created.  This is overly simplistic.

    :param isamAppliance:
    :param instance_id:
    :param junction:
    :return:
    """
    ret_obj = junctions.get_all(isamAppliance, instance_id)

    for j in ret_obj['data']:
        if j['id'] == junction:
            logger.info(f"Junction {junction} was found - hence oauth2 config must have already executed.")
            return True

    return False
