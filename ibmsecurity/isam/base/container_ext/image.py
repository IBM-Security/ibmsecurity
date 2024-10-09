import logging

logger = logging.getLogger(__name__)

uri = "/isam/container_ext/image"

requires_version = "10.0.7.0"
requires_model = "Appliance"

def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieving all known images
    """
    return isamAppliance.invoke_get("Retrieving images",
                                    uri,
                                    requires_model=requires_model,
                                    requires_version=requires_version)

def get(isamAppliance, image_id, check_mode=False, force=False):
    """
    Get image properties
    """
    return isamAppliance.invoke_get("Retrieving configuration for image",
                                    f"{uri}/{image_id}",
                                    requires_model=requires_model,
                                    requires_version=requires_version)



def add(isamAppliance, image, check_mode=False, force=False, warnings=None):
    """
    Pull an image
    Set force to True to force pull
    """
    if force or not _check(isamAppliance, image):
        if check_mode:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            post_data = {
                            'image': image                        }

            return isamAppliance.invoke_post(
                "Pull image",
                uri,
                post_data,
                requires_model=requires_model,
                requires_version=requires_version
            )

    return isamAppliance.create_return_object()



def _check(isamAppliance, name):
    """
    Check if there's a image going by name
    """
    ret_obj = get_all(isamAppliance)
    for c in ret_obj['data']:
        if c.get('name') == name:
            logger.debug(f"Volume {name} exists")
            return True
    return False
