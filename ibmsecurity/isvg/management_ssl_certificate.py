import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


#
# Following code to be adapted for using /custfile_mgmt end-point since there are no
# /management_ssl_certificate end-point in ISVG.
#
def get(isvgAppliance, check_mode=False, force=False):
    """
    Get management ssl certificate information
    """
    return isvgAppliance.invoke_get("Get management ssl certificate information",
                                    "/custfile_mgmt/download?certs/lmi.jks")


#
# Following code to be adapted for using /custfile_mgmt end-point since there are no
# /management_ssl_certificate end-point in ISVG. Needs to be adapter also to rely on
# JKS format instead of PKCS12
#
# Another adaptation is ISVG export simple post body as opposed to multipart upload
# like in ISAM
#
def set(isvgAppliance, certificate, password, check_mode=False, force=False):
    """
    Import certificate database
    """
    warnings = ["Idempotency not available. Unable to extract existing certificate to compare with provided one."]
    if force is True or _check(isvgAppliance, certificate, None) is False:
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True, warnings=warnings)
        else:
#
#	Create a new method isvgAppliance.invoke_post_file() in isvgAppliance to
#	support the type of upload method required by /custfile_mgmt end-point that differs from
#	other techniques used by other end-point /snapshort, available_updates, ...
#
#	Ajust list of post data parameter as required
#
            return isvgAppliance.invoke_post_files(
                "Import certificate database",
                "/upload_object",
                [{
                    'file_formfield': 'uploadedfile',
                    'filename': certificate,
                    'mimetype': 'application/octet-stream'
                }],
                {}, json_response=False)

    return isvgAppliance.create_return_object()


def _check(isvgAppliance, certificate, password):
    """
    TODO replace placeholder
    requires additionally pyOpenSSL to load the p12 and extract the issuer, subject, etc
    """

    return False


def compare(isvgAppliance1, isvgAppliance2):
    """
    Compare management authentication settings
    """
    ret_obj1 = get(isvgAppliance1)
    ret_obj2 = get(isvgAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
