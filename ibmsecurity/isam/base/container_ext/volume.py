import logging
from ibmsecurity.appliance.ibmappliance import IBMError
logger = logging.getLogger(__name__)

uri = "/isam/container_ext/volume"

requires_version = "10.0.7.0"
requires_model = "Appliance"


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieving all known deployment properties for volumes
    """
    return isamAppliance.invoke_get(
        "Retrieving container volume properties",
        uri,
        requires_model=requires_model,
        requires_version=requires_version,
    )


def get(isamAppliance, volume_name=None, volume_id=None, filename=None, check_mode=False, force=False):
    """
    Export volume
    """
    import os.path

    if volume_id is None:
        volume_id = search(isamAppliance, volume_name)
        volume_id = volume_id.get('data', None)

    if volume_id is None and volume_name is None:
        return isamAppliance.create_return_object(warnings=["Volume name or volume id need to be specified"])

    if filename is None:
        if volume_name is None:
            filename = f"{volume_id}.zip"
        else:
            filename = f"{volume_name}.zip"
    if force or (not os.path.exists(filename)):
        try:
            return isamAppliance.invoke_get_file(
                "Retrieving configuration for volume",
                f"{uri}/{volume_id}",
                filename,
                requires_model=requires_model,
                requires_version=requires_version,
            )
        except IBMError as e:
            return isamAppliance.create_return_object(warnings=[str(e)])

    return isamAppliance.create_return_object(warnings=[f"File {filename} exists already?"])


# Alias
export = get


def import_zip(isamAppliance, filename, volume_name=None, volume_id=None, check_mode=False, force=False, warnings=[]):
    """
    Import volume

    volume_id - uuid of the volume (the documentation is wrong)
    """
    import os.path
    logger.debug(f"\n\nTrying to import {filename}\n\n")

    if volume_id is None:
        volume_id = search(isamAppliance, volume_name)
        volume_id = volume_id.get('data', None)

    if volume_id is None and volume_name is None:
        return isamAppliance.create_return_object(warnings=["Volume name or volume id need to be specified"])

    if force or os.path.exists(filename):
        return isamAppliance.invoke_put_files(
            "Import a volume zip",
            f"{uri}/{volume_id}",
            [
                {
                    "file_formfield": "volume",
                    "filename": filename,
                    "mimetype": "application/octet-stream",
                }
            ],
            {},
            requires_version=requires_version,
            warnings=warnings,
            requires_model=requires_model,
        )
    return isamAppliance.create_return_object(warnings)


def search(isamAppliance, volume_name, check_mode=False, force=False):
    """
    Return the id of the volume

    :param isamAppliance:
    :param name:
    :param check_mode:
    :param force:
    :return:
    """
    ret_obj = get_all(isamAppliance, check_mode, force)
    return_obj = isamAppliance.create_return_object()
    return_obj["data"] = None
    for obj in ret_obj["data"]:
        if obj["name"] == volume_name:
            return_obj["data"] = obj["id"]
            return_obj["rc"] = 0
            break

    return return_obj


def add(isamAppliance, name, check_mode=False, force=False, warnings=None):
    """
    Add a volume
    """
    if force or not _check(isamAppliance, name):
        if check_mode:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            post_data = {"name": name}

            return isamAppliance.invoke_post(
                "Create new volume",
                uri,
                post_data,
                requires_model=requires_model,
                requires_version=requires_version,
            )

    return isamAppliance.create_return_object()


def _check(isamAppliance, name):
    """
    Check if there's a volume going by name
    """
    ret_obj = get_all(isamAppliance)
    for c in ret_obj["data"]:
        if c.get("name") == name:
            logger.debug(f"Volume {name} exists")
            return True
    return False
