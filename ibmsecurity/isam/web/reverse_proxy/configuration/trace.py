import logging
import os.path
import shutil

from ibmsecurity.utilities.tools import get_random_temp_dir, files_same

logger = logging.getLogger(__name__)
uri = "/wga/reverseproxy"
requires_modules = ["wga"]
requires_version = None


def get(isamAppliance, instance_id, check_mode=False, force=False):
    """
    Retrieving a tracing configuration file

    """
    return isamAppliance.invoke_get("Retrieving a tracing configuration file",
                                    "{0}/{1}/tracing_configuration".format(uri, instance_id),
                                    requires_modules=requires_modules, requires_version=requires_version)


def export_file(isamAppliance, instance_id, filepath, check_mode=False, force=False):
    """
    Exporting a tracing configuration file
    """

    if os.path.exists(filepath) is True:
        logger.info("File '{0}' already exists.  Skipping export.".format(filepath))
        warnings = ["File '{0}' already exists.  Skipping export.".format(filepath)]
        return isamAppliance.create_return_object(warnings=warnings)

    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:
        return isamAppliance.invoke_get_file(
            "Exporting a tracing configuration file",
            "{0}/{1}/tracing_configuration?export".format(uri, instance_id), filepath
        )

    return isamAppliance.create_return_object()


def update(isamAppliance, instance_id, contents, check_mode=False, force=False):
    """
    Updating tracing configuration file data - using contents string

    """
    update_required = False

    ret_obj = get(isamAppliance, instance_id)
    ret_contents = ret_obj['data']['contents']

    if ret_contents.strip() != contents.strip():
        update_required = True

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:

            return isamAppliance.invoke_put(
                "Updating tracing configuration file data - using contents string",
                "{0}/{1}/tracing_configuration".format(uri, instance_id),
                {
                    'file_contents': contents
                },
                requires_modules=requires_modules, requires_version=requires_version
            )

    return isamAppliance.create_return_object()


def import_file(isamAppliance, instance_id, filepath, check_mode=False, force=False):
    """
    Updating tracing configuration file data - using a file

    """

    if force is True or _check_import(isamAppliance=isamAppliance, id=instance_id, filepath=filepath) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:

            return isamAppliance.invoke_put_files(
                "Updating tracing configuration file data - using a file",
                "{0}/{1}/tracing_configuration".format(uri, instance_id),
                [
                    {
                        'file_formfield': 'file',
                        'filename': filepath,
                        'mimetype': 'application/octet-stream'
                    }
                ],
                {},
                requires_modules=requires_modules, requires_version=requires_version
            )

    return isamAppliance.create_return_object()


def _check_import(isamAppliance, id, filepath):
    """
    Checks if the file to be imported is the same as the file that's already on the instance
    """
    tmpdir = get_random_temp_dir()
    tmp_original_file = os.path.join(tmpdir, os.path.basename("tempfile.txt"))

    export_file(isamAppliance, instance_id=id, filepath=tmp_original_file, check_mode=False, force=True)

    if files_same(tmp_original_file, filepath):
        logger.debug("files are the same, so we don't want to do anything")
        shutil.rmtree(tmpdir)
        return False
    else:
        logger.debug("files are different, so we return True to indicate the new file should be imported")
        shutil.rmtree(tmpdir)
        return True
