import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

uri = "/certstore_object"


def get_all(isvgAppliance, check_mode=False, force=False):
    """
    Get personal cert store entries
    """
    return isvgAppliance.invoke_get("Retrieving cert store entries",
                                    uri + "/key/certificates?type=personal")


def search(isvgAppliance, label, check_mode=False, force=False):
    """
    Search for existing certificate by label
    """
    ret_obj = get_all(isvgAppliance)
    return_obj = isvgAppliance.create_return_object()

    for obj in ret_obj['data']:
        if 'id' in obj and obj['label'] == label:
            logger.info("Found cert entry: {0}".format(obj['label']))
            return_obj['data'] = obj
            return_obj['rc'] = 0
            break

    return return_obj


def upload(isvgAppliance, db, type, password, label="lmi", check_mode=False, force=False):
    """
    Import personal certificate from db
    """
    warnings = []

    file_short = tools.path_leaf(db);
    if force is True or not _check(isvgAppliance, label):
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isvgAppliance.invoke_post_files(
                "Import personal certificate",
                uri + "/key/certificates/upload",
                [
                    {
                        'file_formfield': 'uploadedfile',
                        'filename': db,
                        'mimetype': 'application/octet-stream'
                    }
                ],
                {
                    'fileName': file_short,
                    'cert_name': label,
                    'file_password': password,
                    'file_type': type,
                    'is_getting_val': 'false',
                    'cert_type': 'personal',
                    'uploadType':'iframe'
                },
                json_response=False)

    return isvgAppliance.create_return_object()


def _check(isvgAppliance, label):
    """
    Check if personal cert needs to be uploaded
    """
    ret_obj = search(isvgAppliance, label)

    # Bogus check for now - real test will involve downloading the public personal certificate
    # and compare it with the reference one.
    if len(ret_obj['data']) > 0:
        return True
    else:
        return False
