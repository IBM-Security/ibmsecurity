import ibmsecurity.utilities.tools

module_uri="/isam/felb/errorpages/"
requires_module=None
requires_version=None


def download(isamAppliance, error_page, check_mode=False, force=False):
    """
    Downloads error page
    """
    if force is True or _check(isamAppliance, error_page) is True:
        return isamAppliance.invoke_get("Downloading Error Page", "{0}{1}?export=true".format(module_uri, error_page))
    else:
        return isamAppliance.create_return_object(changed=False)

def get(isamAppliance, error_page, check_mode=False, force=False):
    """
    Retrieving the contents of an error page
    """
    return isamAppliance.invoke_get("Retrieving Error Page Contents", "{0}{1}".format(module_uri, error_page))

def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieves a list of the error pages
    """
    return isamAppliance.invoke_get("Retrieving List of Error Pages", "{0}".format(module_uri))

def update(isamAppliance, error_page, content=None, check_mode=False, force=False):
    """
    Updates existing error page
    """
    if force is True or check_mode is True:
        if _check_update(isamAppliance, error_page, content) is True:
            return isamAppliance.invoke_put("Updating Error Page", "{0}{1}".format(module_uri, error_page),
                                    {
                                        "contents": content
                                    })
        else:
            return isamAppliance.create_return_object(changed=False)

def upload(isamAppliance, error_page, file, check_mode=False, force=False):
    """
    Updating a error page by importing a new file
    """
    return isamAppliance.invoke_put("Uploading Error Page file","{0}{1}".format(module_uri, error_page),
                                    {
                                        "file": file
                                    })
def _check(isamAppliance, error_page):
    """
    checks for idempotency
    """
    pages = get_all(isamAppliance, error_page)
    change_required=True
    for page in pages['data']:
        if page['id'] == error_page:
            change_required=False

    return change_required

def _check_update(isamAppliance, error_page, content=None):
    """
    checks update for idempotency
    """
    change_required=False
    content_check= get(isamAppliance, error_page)

    if content_check['data']['contents'] != content:
        change_required=True

    return change_required

def _check_upload(isamAppliance, error_page, file=None):
    """
    checks upload for idempotency
    """

    return isamAppliance.invoke_get("Checking", "/isam/felb/errorpages")