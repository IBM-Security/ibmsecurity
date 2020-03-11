import logging
import os.path
import shutil
from ibmsecurity.utilities.tools import get_random_temp_dir, files_same

logger = logging.getLogger(__name__)
uri = "/isam/authzserver"
requires_modules = None
requires_version = None


def get(isamAppliance, id, check_mode=False, force=False):
    """
    Retrieve the tracing configuration file of an existing instance

    """
    return isamAppliance.invoke_get("Retrieve the tracing configuration file of an existing instance",
                                    "{0}/{1}/tracing_configuration/v1".format(uri, id),
                                    requires_modules=requires_modules, requires_version=requires_version)


def update(isamAppliance, id, contents, check_mode=False, force=False):
    """
    Update the tracing configuration file of an existing instance

    """
    update_required = False

    ret_obj = get(isamAppliance, id)
    ret_contents = ret_obj['data']['contents']

    if ret_contents.strip() != contents.strip():
        update_required = True

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:

            return isamAppliance.invoke_put(
                "Update the tracing configuration file of an existing instance",
                "{0}/{1}/tracing_configuration/v1".format(uri, id),
                {
                    'contents': contents
                },
                requires_modules=requires_modules, requires_version=requires_version
            )

    return isamAppliance.create_return_object()


def import_file(isamAppliance, id, filepath, check_mode=False, force=False):
    """
    Update the tracing configuration file of an existing instance

    """

    if force is True or _check_import(isamAppliance=isamAppliance, id=id, filepath=filepath) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            with open(filepath, 'r') as infile:
                contents = infile.read()

            return isamAppliance.invoke_put(
                "Update the tracing configuration file of an existing instance",
                "{0}/{1}/tracing_configuration/v1".format(uri, id),
                {
                    'contents': contents.strip()
                },
                requires_modules=requires_modules, requires_version=requires_version
            )

    return isamAppliance.create_return_object()


def export_file(isamAppliance, id, filepath, check_mode=False, force=False):
    """
    Exporting the tracing configuration file of an existing instance
    """

    if os.path.exists(filepath) is True:
        logger.info("File '{0}' already exists.  Skipping export.".format(filepath))
        return isamAppliance.create_return_object()

    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:
        return isamAppliance.invoke_get_file(
            "Exporting the tracing configuration file of an existing instance",
            "{0}/{1}/tracing_configuration/v1?export".format(uri, id), filepath
        )

    return isamAppliance.create_return_object()


def _check_import(isamAppliance, id, filepath, check_mode=False):
    """
    Checks if the file to be imported is the same as the file that's already on the instance
    """
    tmpdir = get_random_temp_dir()
    tmp_original_file = os.path.join(tmpdir, os.path.basename("tempfile.txt"))

    export_file(isamAppliance, id=id, filepath=tmp_original_file)

    if files_same(tmp_original_file, filepath):
        logger.debug("files are the same, so we don't want to do anything")
        shutil.rmtree(tmpdir)
        return False
    else:
        logger.debug("files are different, so we return True to indicate the new file should be imported")
        shutil.rmtree(tmpdir)
        return True
