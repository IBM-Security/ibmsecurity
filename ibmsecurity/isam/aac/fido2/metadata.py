import logging
import json
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/iam/access/v8/fido2/metadata"
requires_modules = ["mga"]
requires_version = "9.0.7.0"

def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieve a list of FIDO2 Metadata
    """
    return isamAppliance.invoke_get("Retrieving the list of FIDO2 Metadata", uri,
                                    requires_modules=requires_modules, requires_version=requires_version)

def get(isamAppliance, name, id=None, check_mode=False, force=False):
    """
    Retrieve a specific FIDO2 Metadata
    """
    if id is None:
        ret_obj = search(isamAppliance, name=name, check_mode=check_mode, force=force)
        id = ret_obj['data']

    if id == {}:
        logger.info("FIDO2 Metadata {0} had no match, skipping retrieval.".format(name))
        return isamAppliance.create_return_object()
    else:
        return _get(isamAppliance, id)

def search(isamAppliance, name, force=False, check_mode=False):
    """
    Search FIDO2 Metadata id by name
    """
    ret_obj = get_all(isamAppliance)
    return_obj = isamAppliance.create_return_object()

    for obj in ret_obj['data']:
        if obj['filename'] == name:
            logger.info("Found FIDO2 Metadata {0} id: {1}".format(name, obj['id']))
            return_obj['data'] = obj['id']
            return_obj['rc'] = 0

    return return_obj

def delete(isamAppliance, name, check_mode=False, force=False):
    """
    Delete a FIDO2 Metadata file
    """
    ret_obj = search(isamAppliance, name, check_mode=check_mode, force=force)
    id = ret_obj['data']

    if id == {}:
        logger.info("FIDO2 Metadata {0} not found, skipping delete.".format(name))
    else:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Delete a FIDO2 Metadata file",
                "{0}/{1}".format(uri, id),
                requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()

def export_file(isamAppliance, name, filename, check_mode=False, force=False):
    """
    Export a specific FIDO2 Metadata file
    """
    import os.path
    ret_obj = search(isamAppliance, name, check_mode=check_mode, force=force)
    id = ret_obj['data']

    if id == {}:
        logger.info("FIDO2 Metadata {0} not found, skipping export.".format(name))
    else:
        if force is True or (os.path.exists(filename) is False):
            if check_mode is False:  # No point downloading a file if in check_mode
                return isamAppliance.invoke_get_file(
                    "Export a specific FIDO2 Metadata file",
                    "{0}/{1}/file".format(uri,id),
                    filename,
                    requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()

def import_file(isamAppliance, filename, check_mode=False, force=False):
    """
    Import a new FIDO2 Metadata file or Import FIDO2 Metadata file contents to existing

    Only a valid FIDO MDS Document (extension .json), Yubico Metadata (extension .yubico), or PEM Certificate (extension .pem) will be accepted.
    Any other file type will fail validation.
    """
    import_new = False
    update_required = False
    if force is False:
        ret_obj = search(isamAppliance, _extract_filename(filename))
        if ret_obj['data'] != {}:
            ret_obj_content = _get(isamAppliance, ret_obj['data'])
            with open(filename, 'r') as infile:
                content = infile.read()
            if (ret_obj_content['data']['contents']).strip() != content.strip():
                update_required = True
        else:
            import_new = True

    if force is True or update_required is True or import_new is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            if import_new is True:
                filebasename = _extract_filename(filename)
                return isamAppliance.invoke_post_files(
                "Import a new FIDO2 Metadata file",
                "{0}".format(uri),
                [
                    {
                        'file_formfield': 'file',
                        'filename': filename,
                        'mimetype': 'application/file'
                    }
                ],
                {
                    "name": filebasename,
                    "filename": filebasename
                },
                requires_modules=requires_modules, requires_version=requires_version)
            else:
                return isamAppliance.invoke_post_files(
                    "Import a FIDO2 Metadata file (replace)",
                    "{0}/{1}/file".format(uri,ret_obj['data']),
                    [
                        {
                            'file_formfield': 'file',
                            'filename': filename,
                            'mimetype': 'application/file'
                        }
                    ],
                    {},
                    requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()

def _get(isamAppliance, id):
    return isamAppliance.invoke_get("Retrieve a specific FIDO2 Metadata by id",
                                    f"{uri}/{id}",
                                    requires_modules=requires_modules, requires_version=requires_version)

def _extract_filename(upload_filename):
    """
    Extract filename from fully qualified path to use if no filename provided
    """
    import os.path
    return os.path.basename(upload_filename)

def _check(isamAppliance, fido2_metadata):
    """
    Check if FIDO2 metadata configuration is identical with server
    """
    ret_obj = get_all(isamAppliance)
    logger.debug("Comparing server FIDO2 metadata configuration with desired configuration.")
    # Converting python ret_obj['data'] dict to valid JSON (RFC 8259)
    # e.g. converts python boolean 'True' -> to JSON literal lowercase value 'true'
    cur_json_string = json.dumps(ret_obj['data'])
    cur_sorted_json = tools.json_sort(cur_json_string)
    logger.debug("Server JSON : {0}".format(cur_sorted_json))
    given_json_string = json.dumps(fido2_metadata)
    given_sorted_json = tools.json_sort(given_json_string)
    logger.debug("Desired JSON: {0}".format(given_sorted_json))
    if cur_sorted_json != given_sorted_json:
        return False
        logger.debug("Changes detected!")
    else:
        logger.debug("Server configuration is identical with desired configuration. No change necessary.")
        return True
