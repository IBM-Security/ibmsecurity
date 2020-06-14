import logging
import os.path
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get(isdsAppliance, check_mode=False, force=False):
    """
    Retrieve existing fixpacks.
    """
    return isdsAppliance.invoke_get("Retrieving fixpacks",
                                    "/fixpacks")


def install(isdsAppliance, file, check_mode=False, force=False):
    """
    Install fixpack
    """
    if force is True or _check(isdsAppliance, file) is False:
        if check_mode is True:
            return isdsAppliance.create_return_object(changed=True)
        else:
            return isdsAppliance.invoke_post_files(
                "Install fixpack",
                "/fixpacks",
                [{
                    'file_formfield': 'file',
                    'filename': file,
                    'mimetype': 'application/octet-stream'
                }],
                {})

    return isdsAppliance.create_return_object()


def _check(isdsAppliance, fixpack):
    """
    Check if fixpack is already installed
    """
    ret_obj = get(isdsAppliance)

    fixpack_name = _extract_fixpack_name(fixpack)

    # Reverse sort the json by 'id'
    json_data_sorted = sorted(ret_obj['data'], key=lambda k: int(k['id']), reverse=True)
    # Eliminate all rollbacks
    del_fixpack = ''  # Delete succeeding fixpack to a rollback, only last fixpack can be rolled back
    for fixpack in json_data_sorted:
        if fixpack['action'] == 'Uninstalled':
            del_fixpack = fixpack['name']
        elif del_fixpack == fixpack['name'] and fixpack['rollback'] == 'Yes':
            del_fixpack = ''
        elif fixpack['name'].lower() == fixpack_name.lower():
            return True

    return False


def _extract_fixpack_name(fixpack):
    """
    Extract fixpack name from the given fixpack
    """
    import re

    # Look for the follwing string inside the fixpack file
    # FIXPACK_NAME="9021_IPv6_Routes_fix"
    for s in ibmsecurity.utilities.tools.strings(fixpack):
        match_obj = re.search(r"FIXPACK_NAME=\"(?P<fp_name>\w+)\"", s)
        if match_obj:
            logger.info("Fixpack name extracted from file using strings method: {0}".format(match_obj.group('fp_name')))
            return match_obj.group('fp_name')

    # Unable to extract fixpack name from binary
    # Return fixpack name derived from the filename
    logger.debug(fixpack)
    file_name = os.path.basename(fixpack)
    fixpack_name, ext_name = file_name.split('.fixpack')
    logger.debug("Extracted fixpack_name: " + fixpack_name)
    return fixpack_name


def compare(isdsAppliance1, isdsAppliance2):
    """
    Compare fixpacks between two appliances
    Sort in reverse order and remove fixpacks that were rolled back before compare
    """
    ret_obj1 = get(isdsAppliance1)
    ret_obj2 = get(isdsAppliance2)

    json_data1_sorted = sorted(ret_obj1['data'], key=lambda k: int(k['id']), reverse=True)
    del_fixpack = ''  # Delete succeeding fixpack to a rollback, only last fixpack can be rolled back
    for fixpack in json_data1_sorted:
        if fixpack['action'] == 'Uninstalled':
            del_fixpack = fixpack['name']
            del fixpack
        elif del_fixpack == fixpack['name'] and fixpack['rollback'] == 'Yes':
            del_fixpack = ''
            del fixpack
        else:
            del fixpack['date']

    json_data2_sorted = sorted(ret_obj2['data'], key=lambda k: int(k['id']), reverse=True)
    del_fixpack = ''  # Delete succeeding fixpack to a rollback, only last fixpack can be rolled back
    for fixpack in json_data2_sorted:
        if fixpack['action'] == 'Uninstalled':
            del_fixpack = fixpack['name']
            del fixpack
        elif del_fixpack == fixpack['name'] and fixpack['rollback'] == 'Yes':
            del_fixpack = ''
            del fixpack
        else:
            del fixpack['date']

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
