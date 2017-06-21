import logging

logger = logging.getLogger(__name__)

# URI for this module
uri = "/mga/partner_templates"
requires_modules = ["federation"]
requires_version = "9.0.0.0"


def get(isamAppliance, check_mode=False, force=False):
    """
    Get the status of the federation partner templates
    """
    return isamAppliance.invoke_get("Get the status of the federation partner templates",
                                    uri,
                                    requires_modules=requires_modules,
                                    requires_version=requires_version)


def upload(isamAppliance, filename, check_mode=False, force=False):
    """
    Update the federation partner templates

    Technote: http://www-01.ibm.com/support/docview.wss?uid=swg21970379
    Description: Connectors available for SAML 2.0

    :param isamAppliance:
    :param filename:
    :param check_mode:
    :param force:
    :return:
    """
    if force is True or _check(isamAppliance, filename) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post_files(
                "Update the federation partner templates", uri,
                [
                    {
                        'file_formfield': 'file',
                        'filename': filename,
                        'mimetype': 'application/octet-stream'
                    }
                ],
                {},
                requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object()


def _check(isamAppliance, filename):
    ret_obj = get(isamAppliance)

    cur_ver = ret_obj['data']['version']
    logger.info("Current Installed Version: {0}".format(cur_ver))

    import os
    fname = os.path.splitext(filename)[0]

    new_ver = fname.split('_')[-1]

    logger.info("Provided Package Version: {0}".format(new_ver))

    if new_ver > cur_ver:
        logger.info("Install of new package can proceed")
        return True
    else:
        logger.info("current package is upto date, no need for upgrade at this time.")
        return False
