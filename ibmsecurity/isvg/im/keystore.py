import logging
import json
import tempfile
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

uri = "/custfile_mgmt"


def get(isvgAppliance, check_mode=False, force=False):
    """
    Get keystore info
    """
    return isvgAppliance.invoke_get("Retrieving keystore entries", uri + "/data")


def search(isvgAppliance, keystore="itimKeystore.jceks", check_mode=False, force=False):
    """
    Search for existing library by file name
    """
    ret_obj = get(isvgAppliance)

    return_obj = isvgAppliance.create_return_object()

    if 'children' in ret_obj['data']:
        for child in ret_obj['data']['children']:
            if 'fileName' in child and child['fileName'] == 'keystore':
                files=json.loads(child['files'])
                for file in files:
                    if 'fileName' in file and file['fileName'] == keystore:
                        logger.info("Found keystore entry: {0}".format(file['fileName']))
                        return_obj['data'] = file
                        return_obj['rc'] = 0
                        break

    return return_obj


def upload(isvgAppliance, keystore, check_mode=False, force=False):
    """
    Import keystore
    """
    warnings = []

    if force is True or not _check(isvgAppliance, keystore):
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            ret_obj = isvgAppliance.invoke_post_files(
                "Import keystore",
                "/upload_object",
                [
                    {
                        'file_formfield': 'uploadedfile',
                        'filename': keystore,
                        'mimetype': 'application/octet-stream'
                    }
                ],
                {
                    'fileName': tools.path_leaf(keystore),
                    'upload_file_type': 'custfile'
                },
                json_response=False)

            warnings = ret_obj['warnings']

            if ret_obj["rc"] == 0:
                keystore_json = {
                   "fileName": "itimKeystore.jceks",
                   "filePath": "data/keystore",
                   "ObjType": "externalfile"
                }

                return isvgAppliance.invoke_post(
                    "Save keystore metadata", uri, keystore_json, warnings=warnings)

    return isvgAppliance.create_return_object()


def download(isvgAppliance, filename, check_mode=False, force=False):
    """
    Download keystore
    """
    import os.path

    if force is True or (os.path.exists(filename) is False):
        if check_mode is False:  # No point downloading a file if in check_mode
            return isvgAppliance.invoke_get_file("Downloading IM keystore",
                                                 "{0}/{1}?data/keystore/{2}".format(uri, "download", "itimKeystore.jceks"), filename=filename, mime_types="*/*")

    return isvgAppliance.create_return_object()


def _check(isvgAppliance, keystore):
    """
    Check if keystore needs to be uploaded
    Need to download current keystore in order to compare both
    """
    ret_obj = search(isvgAppliance, tools.path_leaf(keystore))

    if len(ret_obj['data']) > 0:
        with tempfile.TemporaryDirectory() as tmpdirname:
            tmpFile = tmpdirname + "/" + tools.path_leaf(keystore)
            ret_obj = download(isvgAppliance, tmpFile)
            if ret_obj["rc"] == 0:
                return tools.files_same(keystore, tmpFile)
    else:
        return False
