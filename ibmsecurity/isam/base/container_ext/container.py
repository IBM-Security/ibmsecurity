import logging
import ibmsecurity.isam.base.container_ext.volume as volume

logger = logging.getLogger(__name__)

uri = "/isam/container_ext/container"

requires_version = "10.0.7.0"
requires_model = "Appliance"


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieving all known deployment properties for managed containers
    ./testisam_cmd.py --hostname=${ISAM_LMI} --method=ibmsecurity.isam.base.container_ext.container.get_all
    """
    return isamAppliance.invoke_get(
        "Retrieving managed container properties",
        f"{uri}",
        requires_model=requires_model,
        requires_version=requires_version,
    )


def get(isamAppliance, container_id, check_mode=False, force=False):
    """
    Get specific configuration for a specific container
    """
    return isamAppliance.invoke_get(
        "Retrieving configuration for container",
        f"{uri}/{container_id}",
        requires_model=requires_model,
        requires_version=requires_version,
    )


def add(
    isamAppliance,
    name,
    image,
    type,
    ports,
    volumes,
    env=None,
    logging=None,
    command=None,
    args=None,
    check_mode=False,
    force=False,
    warnings=None,
):
    """
    Add a container
    """
    if force or not _check(isamAppliance, name):
        if check_mode:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            post_data = {"name": name, "image": image, "type": type, "ports": ports}
            # Allow volume_name or value in volumes configuraiton
            # volume_name will do a lookup
            new_volumes = []
            for v in volumes:
                if v.get("value", None) is None:
                    volume_name = v.get("volume_name", None)
                    if volume_name is None:
                        new_volumes.append(v)
                    else:
                        new_value = volume.search(isamAppliance, volume_name)

                        new_volumes.append(
                            {
                                "name": v.get("name", "volume1"),
                                "value": new_value.get("data", None),
                            }
                        )
                else:
                    new_volumes.append(v)
            post_data["volumes"] = new_volumes
            if env:
                post_data["env"] = env
            if logging:
                post_data["logging"] = logging
            if command:
                post_data["command"] = command
            if args:
                post_data["args"] = args
            return isamAppliance.invoke_post(
                "Create new container",
                uri,
                post_data,
                requires_model=requires_model,
                requires_version=requires_version,
            )

    return isamAppliance.create_return_object()


def update(
    isamAppliance,
    name,
    operation=None,
    command=None,
    args=None,
    check_mode=False,
    force=False,
    warnings=None,
):
    """
    Update the pod state container deployment
    """
    container_id = search(isamAppliance, name, check_mode, force)
    container_id = container_id.get('data', None)

    if force or container_id is not None:
        if check_mode:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            put_data = {}
            if operation:
                put_data["operation"] = operation
            if command:
                put_data["command"] = command
            if args:
                put_data["args"] = args
            return isamAppliance.invoke_put(
                "Update the pod state of a container",
                f"{uri}/{container_id}",
                put_data,
                requires_model=requires_model,
                requires_version=requires_version,
            )

    return isamAppliance.create_return_object()


def set(
    isamAppliance,
    name,
    image,
    type,
    ports,
    volumes,
    env=None,
    logging=None,
    command=None,
    args=None,
    replace=False,
    check_mode=False,
    force=False,
    warnings=None,
):
    """
    Replace or create a container
    Use replace as variable to control what will happen (in addition to force)
    """
    if not _check(isamAppliance, name):
        return add(
            isamAppliance,
            name,
            image,
            type,
            ports,
            volumes,
            env,
            logging,
            command,
            args,
            check_mode,
            force,
            warnings,
        )
    else:
        # Delete container and then add it again.

        if force or replace:
            if check_mode:
                return isamAppliance.create_return_object(changed=True, warnings=warnings)
            else:
                logger.debug(f"Replace {name}")
                delete(isamAppliance, name, check_mode, force)
                return add(
                    isamAppliance,
                    name,
                    image,
                    type,
                    ports,
                    volumes,
                    env,
                    logging,
                    command,
                    args,
                    check_mode,
                    force,
                    warnings,
                )

        return isamAppliance.create_return_object()


def delete(isamAppliance, name, check_mode=False, force=False):
    """
    Delete a container by name
    ./testisam_cmd.py --hostname=${ISAM_LMI} --method=ibmsecurity.isam.base.container_ext.container.delete --method_options="name=iag-deployment"
    """
    ret_obj = search(isamAppliance, name)
    container_id = ret_obj.get("data", None)
    if force or container_id is not None:
        if check_mode:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Delete a container",
                f"{uri}/{container_id}"
            )

    return isamAppliance.create_return_object()


def _check(isamAppliance, name):
    """
    Check if there's a container going by name
    """
    ret_obj = get_all(isamAppliance)
    for c in ret_obj["data"]:
        if c.get("name") == name:
            logger.debug(f"Container exists {name}")
            return True
    return False


def search(isamAppliance, name, check_mode=False, force=False):
    """
    Return the id of the container

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
        if obj["name"] == name:
            return_obj["data"] = obj["id"]
            return_obj["rc"] = 0
            logger.debug(f"Found id: {obj['id']} for container {name}")
            break

    return return_obj
