import logging
import os.path
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)
requires_model = "Appliance"


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieve existing fixpacks.
    """
    return isamAppliance.invoke_get("Retrieving fixpacks",
                                    "/fixpacks")


def install(isamAppliance, file, check_mode=False, force=False):
    """
    Installing a fix pack
    """
    if force is True or _check(isamAppliance, file) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post_files(
                "Installing a fix pack",
                "/fixpacks",
                [{
                    'file_formfield': 'file',
                    'filename': file,
                    'mimetype': 'application/octet-stream'
                }],
                {}, requires_model=requires_model)

    return isamAppliance.create_return_object()


def rollback(isamAppliance, file, check_mode=False, force=False):
    """
    Rollback the most recently installed fixpack
    """
    if force is True or _check_rollback(isamAppliance, file) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Rollback the most recently installed fixpack",
                "/fixpacks",
                requires_modules=None,
                requires_version="9.0.3.0",
                requires_model=requires_model
            )

    return isamAppliance.create_return_object()


def _check_rollback(isamAppliance, fixpack):
    """
    Check if fixpack is already installed
    """
    ret_obj = get(isamAppliance)

    fixpack_name = _extract_fixpack_name(fixpack)

    # Reverse sort the json by 'id'
    json_data_sorted = sorted(ret_obj['data'], key=lambda k: int(k['id']), reverse=True)

    # Eliminate all rollbacks before hitting the first non-rollback fixpack
    del_fixpack = ''  # Delete succeeding fixpack to a rollback, only last fixpack can be rolled back
    for fp in json_data_sorted:
        if fp['action'] == 'Uninstalled':
            del_fixpack = fp['name']
        elif del_fixpack == fp['name'] and fp['rollback'] == 'Yes':
            del_fixpack = ''
        elif fp['name'].lower() == fixpack_name.lower():
            return True
        # The first non-rollback fixpack needs to match the name otherwise skip rollback
        else:
            return False

    return False


def _check(isamAppliance, fixpack):
    """
    Check if fixpack is already installed
    """
    ret_obj = get(isamAppliance)

    fixpack_name = _extract_fixpack_name(fixpack)

    # Reverse sort the json by 'id'
    json_data_sorted = sorted(ret_obj['data'], key=lambda k: int(k['id']), reverse=True)

    samename_fps = []
    for fp in json_data_sorted:
        if fp['name'] == fixpack_name:
            samename_fps.append(fp)

    if len(samename_fps) > 0:
        fp_sorted = sorted(samename_fps, key=lambda k: int(k['id']), reverse=True)
        if fp_sorted[0]['action'] == 'Installed':
            return True
        else:
            return False
    else:
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
            logger.info(f"Fixpack name extracted from file using strings method: {match_obj.group('fp_name')}")
            return match_obj.group('fp_name')

    # Unable to extract fixpack name from binary
    # Return fixpack name derived from the filename
    file_name = os.path.basename(fixpack)
    if file_name.find(".fixpack"):
        fixpack_name = file_name.partition(".fixpack")[0]
    else:
        fixpack_name, ext_name = file_name.split('.')
    logger.info(
        f"Fixpack name could not be extracted from binary, use name derived from the filename: {fixpack_name}")
    return fixpack_name


def compare(isamAppliance1, isamAppliance2):
    """
    Compare fixpacks between two appliances
    Sort in reverse order and remove fixpacks that were rolled back before compare
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

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
