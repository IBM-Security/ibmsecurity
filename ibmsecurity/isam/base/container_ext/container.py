import logging

logger = logging.getLogger(__name__)

uri = "/isam/container_ext/container"

requires_version = "10.0.7.0"
requires_model = "Appliance"

def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieving all known deployment properties for managed containers
    """
    return isamAppliance.invoke_get("Retrieving managed container properties",
                                    f"{uri}",
                                    requires_model=requires_model,
                                    requires_version=requires_version)

def get(isamAppliance, container_id, check_mode=False, force=False):
    """
    Get specific configuration for a specific container
    """
    return isamAppliance.invoke_get("Retrieving configuration for container",
                                    f"{uri}/{container_id}",
                                    requires_model=requires_model,
                                    requires_version=requires_version)


def add(isamAppliance, name, image, type, ports, volumes, env=None, logging=None, command=None, args=None, check_mode=False, force=False, warnings=None):
    """
    Add a container
    """
    if force or not _check(isamAppliance, name):
        if check_mode:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            post_data = {
                            'name': name,
                            'image': image,
                            'type': type,
                            'ports': ports,
                            'volumes': volumes
                        }
            if env:
                post_data['env'] = env
            if logging:
                post_data['logging'] = logging
            if command:
                post_data['command'] = command
            if args:
                post_data['args'] = args
            return isamAppliance.invoke_post(
                "Create new container",
                uri,
                post_data,
                requires_model=requires_model,
                requires_version=requires_version
            )

    return isamAppliance.create_return_object()



def _check(isamAppliance, name):
    """
    Check if there's a container going by name
    """
    ret_obj = get_all(isamAppliance)
    for c in ret_obj['data']:
        if c.get('name') == name:
            logger.debug(f"Container exists {name}")
            return True
    return False
