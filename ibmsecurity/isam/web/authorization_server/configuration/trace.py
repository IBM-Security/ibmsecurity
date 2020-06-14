import logging
import os.path
import shutil
from ibmsecurity.utilities.tools import get_random_temp_dir, files_same
from io import open

logger = logging.getLogger(__name__)
uri = "/isam/authzserver"
requires_modules = None
requires_version = None
requires_model = "Appliance"


def get(isamAppliance, id, check_mode=False, force=False):
    """
    Retrieve the tracing configuration file of an existing instance

    """
    return isamAppliance.invoke_get("Retrieve the tracing configuration file of an existing instance",
                                    "{0}/{1}/tracing_configuration/v1".format(uri, id),
                                    requires_modules=requires_modules,
                                    requires_version=requires_version,
                                    requires_model=requires_model)


def update(isamAppliance, id, contents, check_mode=False, force=False):
    """
    Update the tracing configuration file of an existing instance

    """
    update_required = False

    ret_obj = get(isamAppliance, id)
    warnings = ret_obj['warnings']
    if warnings and 'Docker' in warnings[0]:
        return isamAppliance.create_return_object(warnings=ret_obj['warnings'])

    ret_contents = ret_obj['data']['contents']

    if ret_contents.strip() != contents.strip():
        update_required = True

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=ret_obj['warnings'])
        else:

            return isamAppliance.invoke_put(
                "Update the tracing configuration file of an existing instance",
                "{0}/{1}/tracing_configuration/v1".format(uri, id),
                {
                    'contents': contents
                },
                requires_modules=requires_modules,
                requires_version=requires_version,
                requires_model=requires_model
            )

    return isamAppliance.create_return_object(warnings=ret_obj['warnings'])


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
                requires_modules=requires_modules,
                requires_version=requires_version,
                requires_model=requires_model
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
            "{0}/{1}/tracing_configuration/v1?export".format(uri, id), filepath, requires_model=requires_model
        )


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
