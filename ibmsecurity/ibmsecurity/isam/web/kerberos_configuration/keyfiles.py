import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/wga/kerberos/keytab"
requires_modules = ['wga']
requires_version = None


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieve Kerberos: Keytab
    """
    return isamAppliance.invoke_get("Retrieve Kerberos: Keytab", uri,
                                    requires_modules=requires_modules, requires_version=requires_version)


def _check(isamAppliance, id):
    """
    Check if keytab file is present

    :param isamAppliance:
    :return:
    """
    ret_obj = get(isamAppliance)

    logger.debug("Looking for {0} existing keytab files in: {1}".format(id, ret_obj['data']))
    if ret_obj['data']:
        for keytab in ret_obj['data']:
            if keytab['id'] == id:
                logger.debug("Found keytab: {0}".format(id))
                return True

    return False


def import_keytab(isamAppliance, id, file, check_mode=False, force=False):
    """
    Import a keytab file, id is the name of the keytab file (they should be the same)
    """
    if force is True or _check(isamAppliance, id) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post_files(description="Import a keytab file",
                                                   uri="{0}".format(uri),
                                                   fileinfo=[{
                                                       'file_formfield': 'keytab_file',
                                                       'filename': file,
                                                       'mimetype': 'application/octet-stream'
                                                   }],
                                                   data={},
                                                   requires_modules=requires_modules, requires_version=requires_version,
                                                   json_response=False)

    return isamAppliance.create_return_object()


def delete(isamAppliance, id, check_mode=False, force=False):
    """
    Delete a keytab file, id is the name of the keytab file
    """
    if force is True or _check(isamAppliance, id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(description="Delete a keytab file", uri="{0}/{1}".format(uri, id),
                                               requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()


def combine(isamAppliance, newname, keytab_files, check_mode=False, force=False):
    """
    Combine two or more keytab files into one

    keytab_files should be an array of keytabs, like so:
        ['a.keytab', 'b.keytab']
    """
    warnings = []
    for keytab in keytab_files:
        if _check(isamAppliance, keytab) is False:
            warnings.append("keytab file to be combined: {0}, not found".format(keytab))

    if force is True or _check(isamAppliance, newname) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(description="Combine keytab files", uri=uri,
                                            data={
                                                "new_name": newname,
                                                "keytab_files": keytab_files
                                            }, warnings=warnings,
                                            requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()


def compare(isamAppliance1, isamAppliance2):
    """
    Compare kerberos keytab files between two appliances
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    return tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
