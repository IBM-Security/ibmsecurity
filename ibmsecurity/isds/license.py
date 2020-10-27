import logging
from io import open
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/license_activate"
requires_modules = None
requires_version = None


def get(isdsAppliance, check_mode=False, force=False):
    """
    Retrieve license installed in the appliance
    """
    return isdsAppliance.invoke_get("Retrieve license installed in the appliance",
                                    "{0}".format(uri), requires_modules=requires_modules,
                                    requires_version=requires_version)


def install(isdsAppliance, license, check_mode=False, force=False):
    """
    install license in the appliance
    license should be the filename of the license file
    license file content expected format:

    IBM Security Directory Suite V8.0.x
    xxx Edition Key:     xyxyxyxyxyxyxyxyxyxyxy
    """
    f = open(license, 'rt')
    logger.debug(f.readline())
    licence_key_line = f.readline()

    licence_key_tokens = licence_key_line.split(':')
    license_name = licence_key_tokens[0].strip()
    license_key = licence_key_tokens[1].strip()
    logger.debug("License name: " + license_name)
    logger.debug("License key: " + license_key)

    if _check_license(isdsAppliance) == True and force == False:
        return isdsAppliance.create_return_object(warnings=["License already installed"])
    else:
        if _check_license(isdsAppliance) == False or force == True:
            if check_mode:
                return isdsAppliance.create_return_object(
                    changed=True)  # there is no real change in appliance, so maybe it should be false
            else:
                return isdsAppliance.invoke_post("Applying license key to appliance", uri,
                                                 {
                                                     "Licensetext": license_key
                                                 })


def _check_license(isdsAppliance):
    """
    check if a particular license is installed in the appliance
    cannot retrieve installed license key value so sole presence
    of license is sufficient
    """

    ret_obj = get(isdsAppliance)
    """
    Returned json is any of the following:
        {"LicenseActivated":"LIMITED"}
        {"LicenseActivated":"STANDARD"}
        {"LicenseActivated":"ENTERPRISE"}
    """

    if ret_obj['data'] == {"LicenseActivated": "STANDARD"}:
        return True
    elif ret_obj['data'] == {"LicenseActivated": "ENTERPRISE"}:
        return True
    else:
        return False  # no license installed in the appliance


def compare(isdsAppliance1, isdsAppliance2):
    """
    Compare license installed between two appliances
    """
    ret_obj1 = get(isdsAppliance1)
    ret_obj2 = get(isdsAppliance2)

    import ibmsecurity.utilities.tools
    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['serial_number'])
