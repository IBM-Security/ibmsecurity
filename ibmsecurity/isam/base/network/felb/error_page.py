import ibmsecurity.utilities.tools
import logging

logger = logging.getLogger(__name__)

module_uri = "/isam/felb/errorpages/"
requires_modules = None
requires_version = None


def get(isamAppliance, error_page, check_mode=False, force=False):
    """
    Retrieving an error page
    """
    return isamAppliance.invoke_get("Retrieving an error page", "{0}{1}".format(module_uri, error_page),
                                    requires_modules=requires_modules, requires_version=requires_version)


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieving List of Error Pages
    """
    return isamAppliance.invoke_get("Retrieving List of Error Pages", module_uri,
                                    requires_modules=requires_modules, requires_version=requires_version)


def set(isamAppliance, error_page, contents, check_mode=False, force=False):
    """
    Updating an error page
    """
    if force is False:
        ret_obj = get(isamAppliance, error_page)

    if force is True or ret_obj['data'] != contents:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put("Updating an error page", "{0}{1}".format(module_uri, error_page),
                                            {
                                                "contents": contents
                                            }, requires_version=requires_version, requires_module=requires_modules)
    else:
        return isamAppliance.create_return_object()


def import_file(isamAppliance, error_page, file, check_mode=False, force=False):
    """
    Uploading an error page
    """
    if force is True or _check_upload(isamAppliance, error_page, file) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post_files(description="Uploading an error page",
                                                   uri="{0}{1}".format(module_uri, error_page),
                                                   fileinfo=[{
                                                       'file_formfield': 'file',
                                                       'filename': file,
                                                       'mimetype': 'application/octet-stream'
                                                   }],
                                                   data={},
                                                   requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()


def export_file(isamAppliance, error_page, filename, check_mode=False, force=False):
    """
    Downloading an error page
    """
    import os.path
    if force is True or os.path.exists(error_page) is False:
        if check_mode is False:  # No point downloading a file if in check_mode
            return isamAppliance.invoke_get_file(
                "Downloading an error page",
                "{0}{1}?export=true".format(module_uri, error_page),
                filename=filename
            )

    return isamAppliance.create_return_object()


def set(isamAppliance, error_page, content=None, check_mode=False, force=False):
    """
    determines if add or update is used
    """
    try:
        check_obj = get(isamAppliance, error_page)
    except:
        # if error_page does not exist, function calls add function
        logger.debug("Error Page configuration does not exist")
        return add(isamAppliance, error_page, check_mode, force)

    return update(isamAppliance, error_page, content, check_mode, force)


def compare(isamAppliance1, isamAppliance2):
    """
    Compare error pages between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
