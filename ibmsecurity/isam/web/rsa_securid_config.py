import logging
import ibmsecurity.utilities.tools
from ibmsecurity.isam.aac.api_protection import definitions

logger = logging.getLogger(__name__)

# URI for this module
uri = "/wga/rsa_config"
requires_modules = ["wga"]
requires_version = None


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieve RSA Securid Configuration
    """
    return isamAppliance.invoke_get("Retrieve RSA Securid Configuration", uri, requires_modules=requires_modules,
                                    requires_version=requires_version)


def upload(isamAppliance, filename, check_mode=False, force=False):
    """
    Upload a RSA Securid Config file
    """
    warnings = [
        "Idempotency check is only to see if there was a config already uploaded. Force upload to replace existing configuration."]
    if force is True or _check(isamAppliance) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_post_files(
                "Upload a RSA Securid Config file",
                "{0}/server_config".format(uri),
                [
                    {
                        'file_formfield': 'server_config_file',
                        'filename': filename,
                        'mimetype': 'application/octet-stream'
                    }
                ],
                {}, requires_modules=requires_modules,
                requires_version=requires_version, warnings=warnings)

    return isamAppliance.create_return_object()


def _check(isamAppliance):
    ret_obj = get(isamAppliance)
    return ret_obj['data']['server_config'] == 'available'


def test(isamAppliance, username, passcode, check_mode=False, force=False):
    """
    Test RSA Configuration with username/passcode
    """
    if _check(isamAppliance) is False:
        return isamAppliance.create_return_object(warnings=["Valid configuration not found, test skipped."])
    else:
        ret_obj = isamAppliance.invoke_post("Test RSA Configuration with username/passcode", "{0}/test".format(uri),
                                            {
                                                'username': username,
                                                'passcode': passcode
                                            },
                                            requires_modules=requires_modules,
                                            requires_version=requires_version, ignore_error=True)
        if ret_obj['changed'] is True:
            ret_obj['changed'] = False

        return ret_obj


def delete(isamAppliance, check_mode=False, force=False):
    """
    Deleting or Clear RSA Securid Configuration
    """
    if force is True or _check(isamAppliance) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete("Deleting or Clear RSA Securid Configuration",
                                               "{0}/server_config".format(uri),
                                               requires_modules=requires_modules,
                                               requires_version=requires_version)

    return isamAppliance.create_return_object()


def clear(isamAppliance, check_mode=False, force=False):
    """
    Clear the node secret file

    :param isamAppliance:
    :param check_mode:
    :param force:
    :return:
    """
    # TODO: This function has not been tested.  Please open an issue on GitHub if you find a problem.

    if force is True or _check(isamAppliance) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete("Clear the node secret file",
                                               "{0}/node_secret".format(uri),
                                               requires_modules=requires_modules,
                                               requires_version=requires_version)

    return isamAppliance.create_return_object()
