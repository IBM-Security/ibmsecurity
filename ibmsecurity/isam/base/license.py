import logging
from io import open

logger = logging.getLogger(__name__)

# URI for this module
uri = "/core/licenses"
requires_modules = None
requires_version = None


def install(isamAppliance, license, check_mode=False, force=False):
    """
    install license in the appliance
    license should be the filename of the license file
    """
    # create the request header for the post first
    headers = {
        "Accept": "text/html"
    }

    file = {"license": open(license, 'rb')}

    if _check_license(isamAppliance, license) == True and force == False:
        return isamAppliance.create_return_object(warnings=["License already installed"])
    else:
        if _check_license(isamAppliance, license) == False or force == True:
            if check_mode:
                return isamAppliance.create_return_object(
                    changed=True)  # there is no real change in appliance, so maybe it should be false
            else:
                return isamAppliance.invoke_request("Applying license to appliance", method="post", uri=uri,
                                                    requires_modules=requires_modules,
                                                    requires_version=requires_version,
                                                    warnings=[],
                                                    headers=headers, files=file)

    return isamAppliance.create_return_object()


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieve all licenses installed in the appliance
    """
    return isamAppliance.invoke_get("Retrieve all licenses installed in the appliance",
                                    f"{uri}", requires_modules=requires_modules,
                                    requires_version=requires_version)


def _check_license(isamAppliance, license):
    """
    check if a particular license file is installed in the appliance
    """

    ret_obj = get_all(isamAppliance)

    if ret_obj['data'] == {}:
        return False  # no license installed in the appliance

    from xml.etree import ElementTree

    with open(license, 'rt') as f:
        tree = ElementTree.parse(f)

    for path in ['.//OCN']:
        node = tree.find(path)
        if node is not None:
            ocnnumber = node.text
            for item, value in ret_obj['data'].items():
                if 'ocn' in value and value['ocn'] == ocnnumber:
                    return True
        else:
            return False  # does not look like a valid input license file

    return False


def compare(isamAppliance1, isamAppliance2):
    """
    Compare license installed between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    import ibmsecurity.utilities.tools
    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['serial_number'])
