import ibmsecurity.utilities.tools
import logging

logger = logging.getLogger(__name__)

module_uri = "/isam/felb/errorpages/"
requires_module = None
requires_version = None


def add(isamAppliance, error_page, check_mode=False, force=False):
    """
    Downloading an error page
    """
    if force is True or _check(isamAppliance, error_page) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_get("Downloading an error page",
                                            "{0}{1}?export=true".format(module_uri, error_page),
                                            requires_modules=requires_module, requires_version=requires_version)
    else:
        return isamAppliance.create_return_object()


def get(isamAppliance, error_page, check_mode=False, force=False):
    """
    Retrieving an error page
    """
    return isamAppliance.invoke_get("Retrieving an error page", "{0}{1}".format(module_uri, error_page),
                                    requires_modules=requires_module, requires_version=requires_version)


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieving List of Error Pages
    """
    return isamAppliance.invoke_get("Retrieving List of Error Pages", "{0}".format(module_uri),
                                    requires_modules=requires_module, requires_version=requires_version)


def update(isamAppliance, error_page, content, check_mode=False, force=False):
    """
    Updating an error page
    """
    string_content = str(content)
    print string_content

    if force is True or _check_update(isamAppliance, error_page, content) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put("Updating an error page", "{0}{1}".format(module_uri, error_page),
                                            {
                                                "contents": content
                                            }, requires_version=requires_version, requires_module=requires_module)
    else:
        return isamAppliance.create_return_object()


def upload(isamAppliance, error_page, file, check_mode=False, force=False):
    """
    Uploading an error page
    """

    if force is True or _check_upload(isamAppliance, error_page, file) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put("Uploading an error page", "{0}{1}".format(module_uri, error_page),
                                            {
                                                "file": file
                                            }, requires_modules=requires_module, requires_version=requires_version)

    else:
        return isamAppliance.create_return_object()


def export_file(isamAppliance, error_page, check_mode=False, force=False):
    """
    Exporting file
    """
    import os.path
    if force is False:
        ret_obj = get(isamAppliance, error_page)

    if force is True or (ret_obj['data'] != {} and os.path.exists(error_page) is False):
        if check_mode is False:  # No point downloading a file if in check_mode
            return isamAppliance.invoke_get_file(
                "Export a specific error page",
                "{0}{1}?export=true&".format(module_uri, error_page),
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


def _check(isamAppliance, error_page):
    """
    checks for idempotency
    """
    change_required = False
    try:
        pages = get(isamAppliance, error_page)
    except:
        logger.warning("The requested resource does not exist")
        return True

    return change_required

    return change_required


def _check_update(isamAppliance, error_page, content=None):
    """
    checks update for idempotency
    """
    change_required = False
    try:
        content_check = get(isamAppliance, error_page)
    except:
        return logger.debug("The requested resource does not exist")

    if content_check['data']['contents'] != content:
        change_required = True

    return change_required


def _check_upload(isamAppliance, error_page, file):
    """
    idempotency check for upload function.  First try except to see if file exist. if it does return True
    """

    try:
        check_obj = get(isamAppliance, error_page)
        if check_obj['data']['file'] != file:
            return True
        else:
            return False
    except:
        return True


def compare(isamAppliance1, isamAppliance2):
    """
    Compare cluster configuration between two appliances
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
