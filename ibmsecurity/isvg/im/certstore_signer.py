import logging
import hashlib
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

uri = "/sslcert_object"


def get_all(isvgAppliance, check_mode=False, force=False):
    """
    Get signer certificate entries
    """
    return isvgAppliance.invoke_get("Retrieving signer certificate entries", uri)


def search(isvgAppliance, label, check_mode=False, force=False):
    """
    Search for signer certificate by label
    """
    ret_obj = get_all(isvgAppliance)
    return_obj = isvgAppliance.create_return_object()

    for obj in ret_obj['data']:
        logger.debug("obj {0}".format(obj))
        if 'certAlias' in obj and obj['certAlias'] == label:
            logger.info("Found certificate entry: {0}".format(obj['certAlias']))
            return_obj['data'] = obj
            return_obj['rc'] = 0
            break

    return return_obj


def upload(isvgAppliance, certificate, label, check_mode=False, force=False):
    """
    Import signer certificate
    """
    warnings = []

    if force is True or not _check(isvgAppliance, certificate, label):
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            file_short = tools.path_leaf(certificate);
            ret_obj = isvgAppliance.invoke_post_files(
                "Import signer certificate",
                "/upload_object/" + file_short,
                [
                    {
                        'file_formfield': 'uploadedfile',
                        'filename': certificate,
                        'mimetype': 'application/x-x509-ca-cert'
                    }
                ],
                {
                    'certAlias': label,
                    'certLocation': file_short,
                    'upload_file_type': 'ssl_cert'
                },
                json_response=False)

            warnings = ret_obj['warnings']

            if ret_obj["rc"] == 0:
                certificate_json = {
                   "name": label,
                   "certLocation": file_short,
                   "certAlias": label,
                   "_isNew": True,
                   "action":"configure",
                   "uploadedfile":[
                      {
                         "index":0,
                         "name": file_short,
                         "type": "application/x-x509-ca-cert"
                      }
                   ]
                }

                return isvgAppliance.invoke_post(
                    "Save signer certificate metadata", uri + "/", certificate_json, warnings=warnings)

    return isvgAppliance.create_return_object()


def delete(isvgAppliance, certificate, check_mode=False, force=False):
    """
    Delete signer certificate
    """
    warnings = []

    ret_obj = search(isvgAppliance, label, check_mode=check_mode, force=force)

    if force is True or ret_obj['data'] != {}:
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            if 'uuid' in ret_obj['data']:
                uuid = ret_obj['data']['uuid']
                warnings = ret_obj['warnings']
                return isvgAppliance.invoke_delete(
                    "Delete an external certificate", "{0}/{1}".format(uri, uuid), warnings=warnings)

    return isvgAppliance.create_return_object(warnings=warnings)


def _check(isvgAppliance, certificate, label):
    """
    Check if signer certificate needs to be uploaded
    """
    ret_obj = search(isvgAppliance, label)

    if len(ret_obj['data']) > 0 and 'checkSum' in ret_obj['data']:
        applianceCheckSum = ret_obj['data']['checkSum']
        with open(certificate, "rb") as f:
            bytes = f.read()
        localCheckSum = hashlib.sha256(bytes).hexdigest()
        logger.debug("applianceCheckSum={0}".format(applianceCheckSum))
        logger.debug("localCheckSum={0}".format(localCheckSum))
        if applianceCheckSum == localCheckSum:
            return True
        else:
            return False
    else:
        return False
