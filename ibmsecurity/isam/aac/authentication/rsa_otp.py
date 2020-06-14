import logging

logger = logging.getLogger(__name__)

uri = "/iam/access/v8/otp/config/rsa"
requires_modules = ["mga"]
requires_version = "8.0.0.0"


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieve a list of configuration files for RSA
    """
    return isamAppliance.invoke_get("Retrieve a list of configuration files for RSA",
                                    "{0}".format(uri),
                                    requires_modules=requires_modules, requires_version=requires_version)


def import_sdconf(isamAppliance, filepath, check_mode=False, force=False):
    """
    Import sdconf.rec

    """

    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:

        return isamAppliance.invoke_post_files(
            "Import sdconf.rec",
            "{0}/sdconf.rec".format(uri),
            [
                {
                    'file_formfield': 'file',
                    'filename': filepath,
                    'mimetype': 'application/file'
                }
            ],
            {},
            requires_modules=requires_modules, requires_version=requires_version
        )

    return isamAppliance.create_return_object()


def import_sdopts(isamAppliance, filepath, check_mode=False, force=False):
    """
    Import sdopts.rec

    """

    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:

        return isamAppliance.invoke_post_files(
            "Import sdopts.rec",
            "{0}/sdopts.rec".format(uri),
            [
                {
                    'file_formfield': 'file',
                    'filename': filepath,
                    'mimetype': 'application/file'
                }
            ],
            {},
            requires_modules=requires_modules, requires_version=requires_version
        )

    return isamAppliance.create_return_object()


def import_securid(isamAppliance, node, filepath, check_mode=False, force=False):
    """
    Import securid file for a node

    """

    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:

        return isamAppliance.invoke_post_files(
            "Import securid file for a node",
            "{0}/securid/{1}".format(uri, node),
            [
                {
                    'file_formfield': 'file',
                    'filename': filepath,
                    'mimetype': 'application/file'
                }
            ],
            {},
            requires_modules=requires_modules, requires_version=requires_version
        )

    return isamAppliance.create_return_object()


def delete_securid(isamAppliance, node, check_mode=False, force=False):
    """
    Delete the securid file from a node

    """

    ret_obj = get(isamAppliance)
    delete_required = False

    for obj in ret_obj['data']:
        if obj['fileName'] == "securid":
            if 'importTimestamp' in obj:
                delete_required = True

    if force is True or delete_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:

            return isamAppliance.invoke_delete(
                "Delete the securid file from a node",
                "{0}/securid/{1}".format(uri, node),
                requires_modules=requires_modules, requires_version=requires_version
            )

    return isamAppliance.create_return_object()


def delete_sdopts(isamAppliance, check_mode=False, force=False):
    """
    Delete sdopts.rec

    """

    ret_obj = get(isamAppliance)
    delete_required = False

    for obj in ret_obj['data']:
        if obj['fileName'] == "sdopts.rec":
            if 'importTimestamp' in obj:
                delete_required = True

    if force is True or delete_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:

            return isamAppliance.invoke_delete(
                "Delete sdopts.rec",
                "{0}/sdopts.rec".format(uri),
                requires_modules=requires_modules, requires_version=requires_version
            )

    return isamAppliance.create_return_object()


def delete_sdconf(isamAppliance, check_mode=False, force=False):
    """
    Delete sdconf.rec

    """

    ret_obj = get(isamAppliance)
    delete_required = False

    for obj in ret_obj['data']:
        if obj['fileName'] == "sdconf.rec":
            if 'importTimestamp' in obj:
                delete_required = True

    if force is True or delete_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:

            return isamAppliance.invoke_delete(
                "Delete sdconf.rec",
                "{0}/sdconf.rec".format(uri),
                requires_modules=requires_modules, requires_version=requires_version
            )

    return isamAppliance.create_return_object()
