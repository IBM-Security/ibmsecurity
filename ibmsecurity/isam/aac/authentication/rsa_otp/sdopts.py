import logging
from ibmsecurity.isam.aac.authentication.rsa_otp.all import get

logger = logging.getLogger(__name__)

uri = "/iam/access/v8/otp/config/rsa"
requires_modules = ["mga"]
requires_version = "8.0.0.0"


def import_file(isamAppliance, filename, check_mode=False, force=False):
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
                    'filename': filename,
                    'mimetype': 'application/file'
                }
            ],
            {},
            requires_modules=requires_modules, requires_version=requires_version
        )

    return isamAppliance.create_return_object()


def delete(isamAppliance, check_mode=False, force=False):
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
