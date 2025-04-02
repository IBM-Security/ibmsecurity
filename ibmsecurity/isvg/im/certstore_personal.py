import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

uri = "/cert_object"


def get(isvgAppliance, check_mode=False, force=False):
    """
    Get personal cert store entry
    """
    return isvgAppliance.invoke_get("Retrieving cert store entry", uri)


def search(isvgAppliance, serial, check_mode=False, force=False):
    """
    Search for existing certificate by serial
    """
    ret_obj = get(isvgAppliance)
    return_obj = isvgAppliance.create_return_object()

    if 'serialnumber' in ret_obj['data'] and ret_obj['data']['serialnumber'] == int(serial):
        logger.info("Found cert entry: {0}".format(ret_obj['data']['serialnumber']))
        return_obj['data'] = ret_obj['data']
        return_obj['rc'] = 0

    return return_obj


def upload(isvgAppliance, db, type, password, serial, check_mode=False, force=False):
    """
    Import personal certificate from db
    """
    warnings = []

    file_short = tools.path_leaf(db);
    if force is True or not _check(isvgAppliance, serial):
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            ret_obj = isvgAppliance.invoke_post_files(
                "Import personal certificate",
                "/upload_object",
                [
                    {
                        'file_formfield': 'uploadedfile',
                        'filename': db,
                        'mimetype': 'application/x-pkcs12'
                    }
                ],
                {
                    'keyFilePassword': password,
                    'upload_file_type': 'app_ssl_cert'
                },
                json_response=False)

            warnings = ret_obj['warnings']

            if ret_obj["rc"] == 0:
                cert_json = {
                   "fileName": file_short,
                   "keyFilePassword": password,
                   "storeType": type
                }

                return isvgAppliance.invoke_post(
                    "Save personal certificate", "/cert_object/", cert_json, warnings=warnings)

    return isvgAppliance.create_return_object()


def _check(isvgAppliance, serial):
    """
    Check if personal cert needs to be uploaded
    """
    ret_obj = search(isvgAppliance, serial)

    if len(ret_obj['data']) > 0:
        return True
    else:
        return False
