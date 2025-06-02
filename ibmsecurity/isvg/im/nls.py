import logging
import json
import tempfile
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

uri = "/custfile_mgmt"


def get_all(isvgAppliance, check_mode=False, force=False):
    """
    Get nls property file info
    """
    return isvgAppliance.invoke_get("Retrieving nls file entries", uri + "/directories")


def search(isvgAppliance, filename, check_mode=False, force=False):
    """
    Search for existing nls property by file name
    """
    ret_obj = get_all(isvgAppliance)

    return_obj = isvgAppliance.create_return_object()

    if 'children' in ret_obj['data']:
        for child in ret_obj['data']['children']:
            if 'fileName' in child and child['fileName'] == 'nls':
                files=json.loads(child['files'])
                for file in files:
                    if 'fileName' in file and file['fileName'] == filename:
                        logger.info("Found filename entry: {0}".format(file['fileName']))
                        return_obj['data'] = file
                        return_obj['rc'] = 0
                        break

    logger.debug("Found nls entry: {0}".format(return_obj))

    return return_obj


def upload(isvgAppliance, filename, check_mode=False, force=False):
    """
    Import nls property file
    """
    warnings = []

    if force is True or not _check(isvgAppliance, filename):
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            file_short = tools.path_leaf(filename)
            ret_obj = isvgAppliance.invoke_post_files(
                "Import nls property",
                "/upload_object",
                [
                    {
                        'file_formfield': 'uploadedfile',
                        'filename': filename,
                        'mimetype': 'text/plain'
                    }
                ],
                {
                    'fileName': file_short,
                    'upload_file_type': 'custfile'
                },
                json_response=False)

            warnings = ret_obj['warnings']

            if ret_obj["rc"] == 0:
                nls_json = {
                   "fileName": file_short,
                   "filePath": "nls/",
                   "ObjType": "externalfile"
                }

                return isvgAppliance.invoke_post(
                    "Save nls property metadata", uri, nls_json, warnings=warnings)

    return isvgAppliance.create_return_object()


def download(isvgAppliance, filename, check_mode=False, force=False):
    """
    Download nls property file
    """
    import os.path

    if force is True or (os.path.exists(filename) is False):
        if check_mode is False:  # No point downloading a file if in check_mode
            return isvgAppliance.invoke_get_file("Downloading nls file",
                                                 "{0}/{1}?nls/{2}".format(uri, "download", tools.path_leaf(filename)), filename=filename, mime_types="text/html")

    return isvgAppliance.create_return_object()


def _check(isvgAppliance, filename):
    """
    Check if nls filename needs to be uploaded
    Need to download current filename in order to compare both
    """
    ret_obj = search(isvgAppliance, tools.path_leaf(filename))

    if len(ret_obj['data']) > 0:
        with tempfile.TemporaryDirectory() as tmpdirname:
            tmpFile = tmpdirname + "/" + tools.path_leaf(filename)
            ret_obj = download(isvgAppliance, tmpFile)
            if ret_obj["rc"] == 0:
                return tools.files_same(filename, tmpFile)
    else:
        return True
