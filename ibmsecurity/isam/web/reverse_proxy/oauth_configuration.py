import logging
import ibmsecurity.utilities.tools
from ibmsecurity.isam.web.reverse_proxy import junctions

logger = logging.getLogger(__name__)
requires_modules = ["wga"]
requires_version = "9.0.4.0"


def config(isamAppliance, instance_id, hostname='127.0.0.1', port=443, username=None, password=None,
           junction="/mga", reuse_certs=False, reuse_acls=False, api=False, browser=False, auth_register=None, fapi_compliant=None,
           load_certificate=None, enable_mtls=None, mutual_key_label=None,
           check_mode=False, force=False):
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
    :param auth_register:
    :param check_mode:
    :param force:
    :param fapi_compliant:
    :param load_certificate # new in ?
    :param enable_mtls # new in 10.0.8
    :param mutual_key_label # new in 10.0.8
    :return:
    """
    if username is None:
        logger.info("Required parameter username missing. Skipping config.")
        return isamAppliance.create_return_object(warning=["Required parameter username missing. Skipping config."])

    if password is None:
        logger.info("Required parameter password missing. Skipping config.")
        return isamAppliance.create_return_object(warning=["Required parameter password missing. Skipping config."])

    warnings = [
        f"Idempotency logic will check for existence of {junction} junction. Use force=True to override."]
    if force is True or _check_config(isamAppliance, instance_id, junction) is False:
        json_data = {
            "junction": junction,
            "hostname": hostname,
            "port": port,
            "username": username,
            "password": password,
            "api": api,
            "browser": browser,
            "reuse_certs": reuse_certs,
            "reuse_acls": reuse_acls
        }
        if auth_register is not None:
            if ibmsecurity.utilities.tools.version_compare(isamAppliance.facts["version"], "9.0.5.0") < 0:
                warnings.append(
                    f"Appliance at version: {isamAppliance.facts['version']}, auth_register: {auth_register} is not supported. Needs 9.0.5.0 or higher. Ignoring auth_register for this call.")
            else:
                json_data["auth_register"] = auth_register
        if fapi_compliant is not None:
            if ibmsecurity.utilities.tools.version_compare(isamAppliance.facts["version"], "10.0.0.0") < 0:
                warnings.append(
                    f"Appliance at version: {isamAppliance.facts['version']}, fapi_compliant: {fapi_compliant} is not supported. Needs 10.0.0.0 or higher. Ignoring fapi_compliant for this call.")
            else:
                json_data["fapi_compliant"] = fapi_compliant
        if load_certificate is not None:
            if ibmsecurity.utilities.tools.version_compare(isamAppliance.facts["version"], "10.0.0.0") < 0:
                warnings.append(
                    f"Appliance at version: {isamAppliance.facts['version']}, load_certificate: {load_certificate} is not supported. Needs 10.0.0.0 or higher. Ignoring load_certificate for this call.")
            else:
                json_data["load_certificate"] = load_certificate
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
                "OAuth configuration for a reverse proxy instance",
                f"/wga/reverseproxy/{instance_id}/oauth_config",
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
            logger.info(f"Junction {junction} was found - hence oauth config must have already executed.")
            return True

    return False
