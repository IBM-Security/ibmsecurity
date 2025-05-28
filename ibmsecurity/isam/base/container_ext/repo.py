import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

uri = "/isam/container_ext/repo"

requires_version = "10.0.7.0"
requires_model = "Appliance"


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieving health for all (running?) containers
    ./testisam_cmd.py --hostname=${ISAM_LMI} --method=ibmsecurity.isam.base.container_ext.repo.get_all

    """
    return isamAppliance.invoke_get(
        "Retrieving all Registry Authentication",
        f"{uri}",
        requires_model=requires_model,
        requires_version=requires_version,
    )


def get(isamAppliance, registry_id, check_mode=False, force=False):
    """
    Get credential for known users of container registry
    """
    return isamAppliance.invoke_get(
        "Retrieving health for container",
        f"{uri}/{registry_id}",
        requires_model=requires_model,
        requires_version=requires_version,
    )


def add(
    isamAppliance,
    registry,
    user=None,
    secret=None,
    **kwargs,
):
    """
    Add a credential for a user and container registry

    :param isamAppliance:
    :param registry: hostname of the registry, eg. icr.io
    :param user: user (optional)
    :param secret: the secret for the user (optional)
    :param proxy_host (optional)
    :param proxy_port (optional)
    :param proxy_user (optional)
    :param proxy_pass (optional)
    :param proxy_schema (optional)
    :param warnings
    :param check_mode
    :param force
    """
    input_args = {}
    force = False
    check_mode = False
    warnings = []
    for k, v in kwargs.items():
        if k == "force":
            force = v
            continue
        if k == "check_mode":
            check_mode = v
            continue
        if k == "warnings":
            warnings = v
        input_args[k] = v

    if force or not _check(isamAppliance, registry, user):
        if check_mode:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            post_data = {
                "host": registry,
                "user": user,
                "secret": secret,
            }

            post_data.update(input_args)

            return isamAppliance.invoke_post(
                "Create new registry",
                uri,
                post_data,
                requires_model=requires_model,
                requires_version=requires_version,
                warnings=warnings,
            )

    return isamAppliance.create_return_object()


def update(
    isamAppliance,
    registry,
    user=None,
    secret=None,
    **kwargs,
):
    """
    Update a credential for a user and container registry
    (user and secret are NOT required values, although it is stated like that in the documentation)

    :param isamAppliance:
    :param registry: hostname of the registry, eg. icr.io
    :param user: user
    :param secret: the secret for the user
    :param warnings
    :param check_mode
    :param force
    """
    input_args = {}
    force = False
    check_mode = False
    warnings = []
    for k, v in kwargs.items():
        if k == "force":
            force = v
            continue
        if k == "check_mode":
            check_mode = v
            continue
        if k == "warnings":
            warnings = v
        input_args[k] = v
    registry_id = search(isamAppliance, registry, user)
    registry_id = registry_id.get('data', None)
    if force or registry_id is not None:
        if check_mode:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            if tools.version_compare(isamAppliance.facts['version'], "10.0.9.0") < 0:
                warnings.append(f"Appliance is at version: {isamAppliance.facts['version']}. Using the previous format")
                put_data = {
                    "host": registry,
                    "user": user,
                }

            else:
                put_data = {
                    "host": registry,
                    "user": user,
                }
                # append other fields from input parameters
                put_data.update(input_args)
            if secret is not None:
                put_data['secret'] = secret

            return isamAppliance.invoke_put(
                "Update registry",
                f"{uri}/{registry_id}",
                put_data,
                requires_model=requires_model,
                requires_version=requires_version,
                warnings=warnings,
            )

    return isamAppliance.create_return_object()


def set(
    isamAppliance,
    registry,
    user=None,
    secret=None,
    **kwargs,
):
    """
    Set - we can't make this function idempotent if a secret is set.
    (user and secret are NOT required values, although it is stated like that in the documentation)
    TODO: execute every time ?
    """
    if _check(isamAppliance, registry, user):
        logger.debug(f"\nUpdating {registry} with {user}")
        # TODO: make this idempotent
        return update(
            isamAppliance,
            registry,
            user,
            secret,
            warnings=["No idempotency because of secrets"],
            **kwargs)
    else:
        logger.debug(f"\nCreating {registry} with {user}")
        return add(
            isamAppliance,
            registry,
            user,
            secret,
            **kwargs)


def search(isamAppliance, host, user=None, check_mode=False, force=False):
    """
    Return the id of the repository

    :param isamAppliance:
    :param host:
    :param user:
    :param check_mode:
    :param force:
    :return:
    """
    ret_obj = get_all(isamAppliance, check_mode, force)
    return_obj = isamAppliance.create_return_object()
    return_obj["data"] = None
    for obj in ret_obj["data"]:
        if user is None:
            if obj.get("host", "") == host:
                return_obj["data"] = obj["id"]
                return_obj["rc"] = 0
                break
        else:
            if obj.get("host", "") == host and obj.get("user", "") == user:
                return_obj["data"] = obj["id"]
                return_obj["rc"] = 0
                break

    return return_obj


def _check(isamAppliance, registry, user):
    """
    Check if there's a repository already for this host
    I'll make a combination of registry and user....

    """
    ret_obj = get_all(isamAppliance)
    for c in ret_obj["data"]:
        if c.get("host") == registry and c.get("user") == user:
            logger.debug(f"Repository by host {registry} and user {user} exists...")
            return True
            break
    return False


def delete(isamAppliance, registry, user=None, check_mode=False, force=False):
    """
    Delete a repo by host (and user)
    """
    ret_obj = search(isamAppliance, registry, user)
    registry_id = ret_obj.get("data", None)

    if force or registry_id is not None:
        if check_mode:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Delete a repository configuration",
                f"{uri}/{registry_id}"
            )

    return isamAppliance.create_return_object()
