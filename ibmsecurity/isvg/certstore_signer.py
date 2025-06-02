import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

uri = "/certstore_object"


def get_all(isvgAppliance, check_mode=False, force=False):
    """
    Get signer cert store entries
    """
    return isvgAppliance.invoke_get("Retrieving cert store entries",
                                    uri + "/key/certificates?type=signer")


def search(isvgAppliance, subject, check_mode=False, force=False):
    """
    Search for existing certificate by subject
    """
    ret_obj = get_all(isvgAppliance)
    return_obj = isvgAppliance.create_return_object()

    for obj in ret_obj['data']:
        if 'id' in obj and obj['subject'] == subject:
            logger.info("Found cert entry: {0}".format(obj['subject']))
            return_obj['data'] = obj
            return_obj['rc'] = 0
            break

    return return_obj


def upload(isvgAppliance, certificate, subject, label, check_mode=False, force=False):
    """
    Import signer certificate
    """
    warnings = []

    file_short = tools.path_leaf(certificate);
    if force is True or not _check(isvgAppliance, subject):
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isvgAppliance.invoke_post_files(
                "Import signer certificate",
                uri + "/key/certificates/upload",
                [
                    {
                        'file_formfield': 'uploadedfile',
                        'filename': certificate,
                        'mimetype': 'application/x-x509-ca-cert'
                    }
                ],
                {
                    'fileName': file_short,
                    'cert_name': label,
                    'is_getting_val': 'false',
                    'cert_type': 'signer',
                    'uploadType':'iframe'
                },
                json_response=True)

    return isvgAppliance.create_return_object()


def _check(isvgAppliance, subject):
    """
    Check if signer cert needs to be uploaded
    """
    ret_obj = search(isvgAppliance, subject)

    if len(ret_obj['data']) > 0:
        return True
    else:
        return False
