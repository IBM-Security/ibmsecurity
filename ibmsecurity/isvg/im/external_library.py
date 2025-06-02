import logging
import hashlib
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

uri = "/external_library"


def get_all(isvgAppliance, check_mode=False, force=False):
    """
    Get external library entries
    """
    return isvgAppliance.invoke_get("Retrieving external library entries", uri)


def search(isvgAppliance, library, check_mode=False, force=False):
    """
    Search for existing library by file name
    """
    ret_obj = get_all(isvgAppliance)
    return_obj = isvgAppliance.create_return_object()

    for obj in ret_obj['data']:
        if 'fileName' in obj and obj['fileName'] == tools.path_leaf(library):
            logger.info("Found library entry: {0}".format(obj['fileName']))
            return_obj['data'] = obj
            return_obj['rc'] = 0
            break

    return return_obj


def upload(isvgAppliance, library, check_mode=False, force=False):
    """
    Import external library
    """
    warnings = []

    if force is True or not _check(isvgAppliance, library):
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            file_short = tools.path_leaf(library);
            ret_obj = isvgAppliance.invoke_post_files(
                "Import external library",
                "/upload_object/" + file_short,
                [
                    {
                        'file_formfield': 'uploadedfile',
                        'filename': library,
                        'mimetype': 'application/octet-stream'
                    }
                ],
                {
                    'fileName': file_short,
                    'upload_file_type': 'library'
                },
                json_response=False)

            warnings = ret_obj['warnings']

            if ret_obj["rc"] == 0:
                library_json = {
                   "fileName": file_short,
                   "isWorkflowExtension": "false",
                   "extensionFile": "",
                   "isLibrary": True,
                   "action":"configure",
                   "_isNew": True,
                   "uploadedfile":[
                      {
                         "index":0,
                         "name": file_short,
                         "type": ""
                      }
                   ]
                }

                return isvgAppliance.invoke_post(
                    "Save external library metadata", uri, library_json, warnings=warnings)

    return isvgAppliance.create_return_object()


def delete(isvgAppliance, library, check_mode=False, force=False):
    """
    Delete an existing external library
    """
    warnings = []

    ret_obj = search(isvgAppliance, library, check_mode=check_mode, force=force)

    if force is True or ret_obj['data'] != {}:
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            if 'uuid' in ret_obj['data']:
                uuid = ret_obj['data']['uuid']
                warnings = ret_obj['warnings']
                return isvgAppliance.invoke_delete(
                    "Delete an existing external library", "{0}/{1}".format(uri, uuid), warnings=warnings)

    return isvgAppliance.create_return_object(warnings=warnings)


def _check(isvgAppliance, library):
    """
    Check if external library needs to be uploaded
    """
    ret_obj = search(isvgAppliance, library)

    if len(ret_obj['data']) > 0 and 'checkSum' in ret_obj['data']:
        applianceCheckSum = ret_obj['data']['checkSum']
        with open(library, "rb") as f:
            bytes = f.read()
        localCheckSum = hashlib.sha256(bytes).hexdigest()
        if applianceCheckSum == localCheckSum:
            return True
        else:
            return False
    else:
        return False
