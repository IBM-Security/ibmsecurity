import ibmsecurity.utilities.tools
import logging

logger = logging.getLogger(__name__)

module_uri = "/isam/felb/errorpages/"
requires_modules = None
requires_version = None
requires_model = "Appliance"


def get(isamAppliance, error_page, check_mode=False, force=False):
    """
    Retrieving an error page
    """
    return isamAppliance.invoke_get("Retrieving an error page", f"{module_uri}{error_page}",
                                    requires_modules=requires_modules, requires_version=requires_version,
                                    requires_model=requires_model)


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieving List of Error Pages
    """
    return isamAppliance.invoke_get("Retrieving List of Error Pages", module_uri,
                                    requires_modules=requires_modules, requires_version=requires_version,
                                    requires_model=requires_model)


def set(isamAppliance, error_page, contents, check_mode=False, force=False):
    """
    Updating an error page
    """

    ret_obj = get(isamAppliance, error_page)
    warnings = ret_obj['warnings']

    if 'contents' in ret_obj['data']:
        ret_contents = ret_obj['data']['contents']
    else:
        ret_contents = False

    if force is True or ret_contents != contents:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_put("Updating an error page", f"{module_uri}{error_page}",
                                            {
                                                "contents": contents
                                            }, requires_version=requires_version, requires_modules=requires_modules,
                                            requires_model=requires_model)
    else:
        return isamAppliance.create_return_object(warnings=warnings)


def import_file(isamAppliance, error_page, filename, check_mode=False, force=False):
    """
    Uploading an error page
    """

    check_value, warnings = _check(isamAppliance, error_page, filename)

    if force is True or check_value is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_post_files(description="Uploading an error page",
                                                   uri=f"{module_uri}{error_page}",
                                                   fileinfo=[{
                                                       'file_formfield': 'file',
                                                       'filename': filename,
                                                       'mimetype': 'application/octet-stream'
                                                   }],
                                                   data={},
                                                   requires_modules=requires_modules, requires_version=requires_version,
                                                   requires_model=requires_model)

    return isamAppliance.create_return_object(warnings=warnings)


def export_file(isamAppliance, error_page, filename, check_mode=False, force=False):
    """
    Downloading an error page
    """

    import os.path
    if force is True or os.path.exists(error_page) is False:
        if check_mode is False:  # No point downloading a file if in check_mode
            return isamAppliance.invoke_get_file(
                "Downloading an error page",
                f"{module_uri}{error_page}?export=true",
                filename=filename, requires_model=requires_model
            )

    return isamAppliance.create_return_object()


def _check(isamAppliance, error_page, filename):
    ret_obj = get(isamAppliance, error_page)
    value = True
    warnings = ret_obj['warnings']
    ret_contents = ""

    if ret_obj['data'] != {}:
        ret_contents = ret_obj['data']['contents']

    with open(filename, 'r') as infile:
        contents = infile.read()

    if len(ret_contents) > 0 and len(contents) > 0:
        if ret_contents.strip() == contents.strip():
            value = False
            return value, warnings
        else:
            value = True
            return value, warnings
    else:
        value = True
        return value, warnings


def compare(isamAppliance1, isamAppliance2):
    """
    Compare error pages between two appliances
    """

    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
