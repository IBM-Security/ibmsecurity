import logging

logger = logging.getLogger(__name__)

uri = "/isam/container_ext/image"

requires_version = "10.0.7.0"
requires_model = "Appliance"


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieving all known images

    """
    return isamAppliance.invoke_get(
        "Retrieving images",
        uri,
        requires_model=requires_model,
        requires_version=requires_version,
    )


def get(isamAppliance, image_id, check_mode=False, force=False):
    """
    Get image properties
    """
    return isamAppliance.invoke_get(
        "Retrieving configuration for image",
        f"{uri}/{image_id}",
        requires_model=requires_model,
        requires_version=requires_version,
    )


def search(isamAppliance, image, check_mode=False, force=False):
    """
    Return the id of the image

    :param isamAppliance:
    :param image:
    :param check_mode:
    :param force:
    :return:
    """
    ret_obj = get_all(isamAppliance, check_mode, force)
    return_obj = isamAppliance.create_return_object()
    return_obj["data"] = None
    for obj in ret_obj["data"]:
        if obj["image"] == image:
            return_obj["data"] = obj["id"]
            return_obj["rc"] = 0
            logger.debug(f"Found id: {obj['id']} for {image}")
            break

    return return_obj


def add(isamAppliance, image, check_mode=False, force=False, warnings=None):
    """
    Pull an image
    Set force to True to force pull
    OR use update
    """
    if force or not _check(isamAppliance, image):
        if check_mode:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            post_data = {"image": image}

            return isamAppliance.invoke_post(
                "Pull image",
                uri,
                post_data,
                requires_model=requires_model,
                requires_version=requires_version,
            )

    return isamAppliance.create_return_object()


def set(isamAppliance, image, check_mode=False, force=False, warnings=None):
    if _check(isamAppliance, image):
        return update(isamAppliance, image, check_mode, force, warnings)
    else:
        return add(isamAppliance, image, check_mode, force, warnings)


def update(isamAppliance, image, check_mode=False, force=False, warnings=None):
    """
    Pull a new version of (existing) image
    Only do this if force = true
    """
    image_id = search(isamAppliance, image)
    image_id = image_id.get("data", None)

    if force and image_id is not None:
        logger.debug(f"(Force) Updating {image_id}")
        if check_mode:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            put_data = {"image": image}
            return isamAppliance.invoke_put(
                "Force pull image",
                f"{uri}/{image_id}",
                put_data,
                requires_model=requires_model,
                requires_version=requires_version,
            )
    else:
        if warnings is None:
            warnings = [f"Image {image} does not exist yet, or not set to force=True"]
        else:
            warnings.append(f"Image {image} does not exist yet, or not set to force=True")
        return isamAppliance.create_return_object(changed=False, warnings=warnings)


def _check(isamAppliance, name):
    """
    Check if there's a image going by name
    """
    ret_obj = get_all(isamAppliance)
    for c in ret_obj["data"]:
        if c.get("image") == name:
            logger.debug(f"Volume {name} exists")
            return True
    return False


def delete(isamAppliance, name, check_mode=False, force=False):
    """
    Delete an image by name
    ./testisam_cmd.py --hostname=${ISAM_LMI} --method=ibmsecurity.isam.base.container_ext.image.delete --method_options="name=icr.io/isva/verify-access-oidc-provider:23.03"
    """
    ret_obj = search(isamAppliance, name)
    image_id = ret_obj.get("data", None)

    if force or image_id is not None:
        if check_mode:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Delete an image",
                f"{uri}/{image_id}"
            )

    return isamAppliance.create_return_object()
