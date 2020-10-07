import logging
import ibmsecurity.utilities.tools
from ibmsecurity.isam.aac.api_protection import definitions

logger = logging.getLogger(__name__)

# URI for this module
uri = "/wga/rsa_config"
requires_modules = ["wga"]
requires_version = None
requires_model = "Appliance"


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieve RSA Securid Configuration
    """
    return isamAppliance.invoke_get("Retrieve RSA Securid Configuration", uri, requires_modules=requires_modules,
                                    requires_version=requires_version, requires_model=requires_model)


def upload(isamAppliance, filename, check_mode=False, force=False):
    """
    Upload a RSA Securid Config file
    """

    srv_cfg_available, warnings = _check(isamAppliance)
    if warnings and warnings[0] != '':
        return isamAppliance.create_return_object(warnings=warnings)

    if force is True or srv_cfg_available is False:
        warnings = [
                "Idempotency check is only to see if there was a config already uploaded. Force upload to replace existing configuration."]

        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_post_files(
                    "Upload a RSA Securid Config file",
                    "{0}/server_config".format(uri),
                    [
                        dict(file_formfield='server_config_file', filename=filename,
                             mimetype='application/octet-stream')
                    ],
                    {}, requires_modules=requires_modules,
                    requires_version=requires_version, warnings=warnings, requires_model=requires_model)

    return isamAppliance.create_return_object(warnings=warnings)


def _check(isamAppliance):
    ret_obj = get(isamAppliance)
    srv_cfg_available, warnings = False, ret_obj['warnings']

    if warnings == [] and ret_obj['data']['server_config'] == 'available':
        srv_cfg_available = True
    return srv_cfg_available, warnings


def test(isamAppliance, username, passcode, check_mode=False, force=False):
    """
    Test RSA Configuration with username/passcode
    """
    srv_cfg_available, warnings = _check(isamAppliance)

    if warnings and warnings[0] != '':
        return isamAppliance.create_return_object(warnings=warnings)

    if srv_cfg_available is False:
        return isamAppliance.create_return_object(warnings=["Valid configuration not found, test skipped."])
    else:
        ret_obj = isamAppliance.invoke_post("Test RSA Configuration with username/passcode", "{0}/test".format(uri),
                                            {
                                                'username': username,
                                                'passcode': passcode
                                            },
                                            requires_modules=requires_modules,
                                            requires_version=requires_version,
                                            ignore_error=True,
                                            requires_model=requires_model)
        if ret_obj['changed'] is True:
            ret_obj['changed'] = False

        return ret_obj


def delete(isamAppliance, check_mode=False, force=False):
    """
    Deleting or Clear RSA Securid Configuration
    """
    srv_cfg_available, warnings = _check(isamAppliance)

    if force is True or srv_cfg_available is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_delete("Deleting or Clear RSA Securid Configuration",
                                               "{0}/server_config".format(uri),
                                               requires_modules=requires_modules,
                                               requires_version=requires_version,
                                               requires_model=requires_model)

    return isamAppliance.create_return_object(warnings=warnings)


def clear(isamAppliance, check_mode=False, force=False):
    """
    Clear the node secret file

    :param isamAppliance:
    :param check_mode:
    :param force:
    :return:
    """
    # TODO: This function has not been tested.  Please open an issue on GitHub if you find a problem.
    srv_cfg_available, warnings = _check(isamAppliance)

    if force is True or srv_cfg_available is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_delete("Clear the node secret file",
                                               "{0}/node_secret".format(uri),
                                               requires_modules=requires_modules,
                                               requires_version=requires_version,
                                               requires_model=requires_model)

    return isamAppliance.create_return_object(warnings=warnings)
