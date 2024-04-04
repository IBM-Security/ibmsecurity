import logging
import ibmsecurity.utilities.tools
from ibmsecurity.isam.web.reverse_proxy import junctions

logger = logging.getLogger(__name__)
requires_modules = ["wga"]
requires_version = "9.0.4.0"


def config(isamAppliance, instance_id, hostname='127.0.0.1', port=443, username=None, password=None,
           junction="/mga", reuse_certs=False, reuse_acls=False, api=False, browser=False, auth_register=None, fapi_compliant=None,
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
    :return:
    """
    if username is None:
        logger.info("Required parameter username missing. Skipping config.")
        return isamAppliance.create_return_object(warning=["Required parameter username missing. Skipping config."])

    if password is None:
        logger.info("Required parameter password missing. Skipping config.")
        return isamAppliance.create_return_object(warning=["Required parameter password missing. Skipping config."])

    warnings = [
        "Idempotency logic will check for existence of {} junction. Use force=True to override.".format(junction)]
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
                    "Appliance at version: {0}, auth_register: {1} is not supported. Needs 9.0.5.0 or higher. Ignoring auth_register for this call.".format(
                        isamAppliance.facts["version"], auth_register))
            else:
                json_data["auth_register"] = auth_register
        if fapi_compliant is not None:
            if ibmsecurity.utilities.tools.version_compare(isamAppliance.facts["version"], "10.0.0.0") < 0:
                warnings.append(
                    "Appliance at version: {0}, fapi_compliant: {1} is not supported. Needs 10.0.0.0 or higher. Ignoring fapi_compliant for this call.".format(
                        isamAppliance.facts["version"], fapi_compliant))
            else:
                json_data["fapi_compliant"] = fapi_compliant 
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_post(
                "OAuth configuration for a reverse proxy instance",
                "/wga/reverseproxy/{0}/oauth_config".format(instance_id), json_data, warnings=warnings,
                requires_modules=requires_modules, requires_version=requires_version)
    return isamAppliance.create_return_object(warnings=warnings)

def _check_config(isamAppliance, instance_id, junction):
    """
    Check if the junction for oauth already created

    :param isamAppliance:
    :param instance_id:
    :param junction:
    :return:
    """
    ret_obj = junctions.get_all(isamAppliance, instance_id)

    for j in ret_obj['data']:
        if j['id'] == junction:
            logger.info("Junction {} was found - hence oauth config must have already executed.".format(junction))
            return True

    return False
