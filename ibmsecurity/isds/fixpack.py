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

def getfips(isdsAppliance, check_mode=False, force=False):
    """
    Retrieve existing fixpack FIPS mode setting
    """
    return isdsAppliance.invoke_get("Retrieving fixpacks FIPS mode",
                                    "/fixpacks/fipsmode")


def install(isdsAppliance, file, check_mode=False, force=False):
    """
    Install fixpack
    """
    if force is True or _check(isdsAppliance, file) is False:
        if check_mode is True:
            return isdsAppliance.create_return_object(changed=True)
        else:
            logger.info("SHOULD NOT BE HERE")
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
    # Extract fixpack name from file
    file_name = os.path.basename(fixpack)

    # Reverse sort the json by 'id'
    for fixpack in ret_obj['data']:
        if fixpack['name'].lower() == file_name.lower():
            return True

    return False


def compare(isdsAppliance1, isamAppliance2):
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
