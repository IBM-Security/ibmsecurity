import logging

logger = logging.getLogger(__name__)

uri = "/isam/container_ext/volume"

requires_version = "10.0.7.0"
requires_model = "Appliance"

def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieving all known deployment properties for volumes
    """
    return isamAppliance.invoke_get("Retrieving container volume properties",
                                    uri,
                                    requires_model=requires_model,
                                    requires_version=requires_version)

def get(isamAppliance, volume_id, filename=None, check_mode=False, force=False):
    """
    Export volume
    """
    import os.path

    if filename is None:
        filename = f"{volume_id}.zip"

    if force or (not os.path.exists(filename)):
          return isamAppliance.invoke_get_file("Retrieving configuration for volume",
                                    f"{uri}/{volume_id}",
                                    filename,
                                    requires_model=requires_model,
                                    requires_version=requires_version)

    return isamAppliance.create_return_object()

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
    id = None
    for obj in ret_obj['data']:
        if obj['name'] == volume_name:
            id = obj['id']
            break

    return id


def add(isamAppliance, name, check_mode=False, force=False, warnings=None):
    """
    Add a volume
    """
    if force or not _check(isamAppliance, name):
        if check_mode:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            post_data = {
                            'name': name
                        }

            return isamAppliance.invoke_post(
                "Create new volume",
                uri,
                post_data,
                requires_model=requires_model,
                requires_version=requires_version
            )

    return isamAppliance.create_return_object()



def _check(isamAppliance, name):
    """
    Check if there's a volume going by name
    """
    ret_obj = get_all(isamAppliance)
    for c in ret_obj['data']:
        if c.get('name') == name:
            logger.debug(f"Volume {name} exists")
            return True
    return False
