import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get(isamAppliance, check_mode=False, force=False):
    """
    Get management ssl certificate information
    """
    return isamAppliance.invoke_get("Get management ssl certificate information",
                                    "/isam/management_ssl_certificate/")


def set(isamAppliance, certificate, password, check_mode=False, force=False):
    """
    Import certificate database
    """
    warnings = ["Idempotency not available. Unable to extract existing certificate to compare with provided one."]
    if force is True or _check(isamAppliance, certificate, password) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_post_files(
                "Import certificate database",
                "/isam/management_ssl_certificate",
                [
                    {
                        'file_formfield': 'cert',
                        'filename': certificate,
                        'mimetype': 'application/x-pkcs12'
                    }
                ],
                {
                    'password': password
                },
                json_response=False, warnings=warnings)

    return isamAppliance.create_return_object()


def _check(isamAppliance, certificate, password):
    """
    TODO replace placeholder
    requires additionally pyOpenSSL to load the p12 and extract the issuer, subject, etc
    """

    return False


def compare(isamAppliance1, isamAppliance2):
    """
    Compare management authentication settings
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
