import logging

logger = logging.getLogger(__name__)
# URI for this module
uri = "/iam/access/v8/geolocation-db"
requires_modules = None
requires_version = None


def get(isamAppliance, check_mode=False, force=False):
    """
    Get the status of the geolocation database load
    """
    return isamAppliance.invoke_get("Get the status of the geolocation database load", "{}/status".format(uri),
                                    requires_modules=requires_modules, requires_version=requires_version)


def cancel(isamAppliance, check_mode=False, force=False):
    """
    Cancel the most recent geolocation database load
    """
    ret_obj = get(isamAppliance)
    if force is True or ret_obj['data']['status'] == 'LOADING':
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_get("Cancel the most recent geolocation database load", "{}/cancel".format(uri),
                                            requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()


def upload(isamAppliance, file=None, check_mode=False, force=False):
    """
    Load new geolocation database
    """
    warnings = ["No idempotency check for this function."]

    if check_mode is True:
        return isamAppliance.create_return_object(changed=True, warnings=warnings)
    else:
        return isamAppliance.invoke_post_files(
            "Load new geolocation database", uri,
            [
                {
                    'file_formfield': 'file',
                    'filename': file,
                    'mimetype': 'application/octet-stream'
                }
            ],
            {}, warnings=warnings, requires_modules=requires_modules, requires_version=requires_version)
