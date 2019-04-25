import logging
import os.path
from ibmsecurity.utilities import tools
from ibmsecurity.utilities.tools import files_same, get_random_temp_dir, json_compare
import shutil

logger = logging.getLogger(__name__)

# URI for this module
uri = "/iam/access/v8/bundles"


def get_all(isamAppliance, filter=None, start=None, count=None, check_mode=False, force=False):
    """
    Retrieve a list of bundles
    """
    return isamAppliance.invoke_get("Retrieve a list of bundles",
                                    "{0}{1}".format(uri,
                                                    tools.create_query_string(filter=filter, start=start, count=count)))


def get(isamAppliance, filename, check_mode=False, force=False):
    """
    Retrieve a specific bundle
    """
    ret_obj = search(isamAppliance, filename=filename, check_mode=check_mode, force=force)
    bundle_id = ret_obj['data']

    if bundle_id == {}:
        logger.info("Bundle {0} had no match, skipping retrieval.".format(filename))
        return isamAppliance.create_return_object()
    else:
        return isamAppliance.invoke_get("Retrieve a specific bundle",
                                        "{0}/{1}".format(uri, bundle_id))


def search(isamAppliance, filename, force=False, check_mode=False):
    """
    Search bundle id by name
    """
    ret_obj = get_all(isamAppliance)
    return_obj = isamAppliance.create_return_object()

    for obj in ret_obj['data']:
        if obj['filename'] == filename:
            logger.info("Found Bundle {0} id: {1}".format(filename, obj['id']))
            return_obj['data'] = obj['id']
            return_obj['rc'] = 0

    return return_obj


def create(isamAppliance, filename, check_mode=False, force=False):
    """
    Create a bundle
    """
    (d, f) = os.path.split(filename)
    if force is True or (search(isamAppliance, filename=f))['data'] == {}:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post(
                "Create a bundle", uri,
                {
                    "filename": f
                })

    return isamAppliance.create_return_object()


def verify(isamAppliance, filename, check_mode=False, force=False):
    """
    Verify the contents of a bundle file

    Note: No changes are being made, so changed flag is being forced to False.
    """
    (d, f) = os.path.split(filename)
    ret_obj = isamAppliance.invoke_post_files(
        "Verify the contents of a bundle file",
        "{0}/verify".format(uri),
        [
            {
                'file_formfield': 'file',
                'filename': filename,
                'mimetype': 'application/jar'
            }
        ],
        {
            "import_file": f
        })

    ret_obj['changed'] = False

    return ret_obj


def export_bundle(isamAppliance, filename, extract_filename, check_mode=False, force=False):
    """
    Export a specific bundle
        -filename is the name of the jar on the Appliance (e.g. mybundle.jar)
        -extract_filename is file system location to export the file (e.g. /tmp/mybundle.jar)
    """
    ret_obj = search(isamAppliance, filename)
    if force is True or ret_obj['data'] != {}:  # ret_obj['data'] is the numeric id assigned by the system
        if check_mode is False:  # No point downloading a file if in check_mode
            return isamAppliance.invoke_get_file(
                "Export a specific bundle",
                "{0}/{1}/file".format(uri, ret_obj['data']),
                extract_filename)

    return isamAppliance.create_return_object()


def import_bundle(isamAppliance, filename, check_mode=False, force=False):
    """
    Import the bundle file for a bundle

    ret_obj used in the code below looks like this:
        { 'changed': False,
          'data': [ { u'extensions': [ { u'id': u'NewAuthMech',
                                         u'name': u'NewAuthMech',
                                         u'type': u'Authentication Mechanism'}],
                      u'filename': u'newauth.jar',
                      u'id': u'2'}],
          'rc': 0,
          'warnings': []}

    """
    f = os.path.basename(filename)
    warnings, bundle_id = _check_import(isamAppliance, filename)
    if force is True or bundle_id:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_post_files(
                "Import the bundle file for a bundle",
                "{0}/{1}/file".format(uri, bundle_id),
                [
                    {
                        'file_formfield': 'file',
                        'filename': filename,
                        'mimetype': 'application/jar'
                    }
                ],
                {
                    "import_file": f
                }, warnings=warnings)

    return isamAppliance.create_return_object(warnings=warnings)


def _check_import(isamAppliance, filename):
    """
    Checks if file on the Appliance exists and if so, whether it is different from filename
    """
    warnings = []
    (d, f) = os.path.split(filename)  # this means the name of the bundle has to match name of file to import
    ret_obj = get(isamAppliance, f)
    tmpdir = get_random_temp_dir()
    if ret_obj['data'] != {} and ret_obj['data']['extensions'] != []:
        tmp_original_file = os.path.join(tmpdir, ret_obj['data']['filename'])
        export_bundle(isamAppliance, ret_obj['data']['filename'], tmp_original_file, check_mode=False, force=True)
        logger.debug("file already exists on appliance")
        if files_same(tmp_original_file, filename):
            logger.debug("files are the same, so we don't want to do anything")
            shutil.rmtree(tmpdir)
            return warnings, False
        else:
            logger.debug("files are different, so we replace existing file")
            bundle_id = ret_obj['data']['id']
            shutil.rmtree(tmpdir)
            return warnings, bundle_id
    elif ret_obj['data'] != {} and ret_obj['data']['extensions'] == []:
        bundle_id = ret_obj['data']['id']
        return warnings, bundle_id
    else:
        warnings.append("Bundle does not exist on appliance, create a bundle first and then import.")
        return warnings, False


def _check(isamAppliance, id):
    """
    Check if id already exists
    """
    ret_obj = get_all(isamAppliance)

    for obj in ret_obj['data']:
        if obj['id'] == id:
            return True

    return False


def delete(isamAppliance, filename, check_mode=False, force=False):
    """
    Delete a bundle
    """
    (d, f) = os.path.split(filename)
    ret_obj = search(isamAppliance, f)
    if force is True or ret_obj['data'] != {}:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Delete a bundle",
                "{0}/{1}".format(uri, ret_obj['data']))

    return isamAppliance.create_return_object()


def compare(isamAppliance1, isamAppliance2):
    """
    Compare list of extension bundles between 2 appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    for obj in ret_obj1['data']:
        del obj['id']
    for obj in ret_obj2['data']:
        del obj['id']

    return tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['id'])
