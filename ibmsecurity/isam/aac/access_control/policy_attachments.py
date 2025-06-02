import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/iam/access/v8/policyattachments"


def get_all(isamAppliance, filter=None, sortBy=None, check_mode=False, force=False):
    """
    Retrieve a list of configured resources
    """
    return isamAppliance.invoke_get(
        "Retrieve a list of configured resources",
        f"{uri}{tools.create_query_string(filter=filter, sortBy=sortBy)}",
    )


def get(isamAppliance, server, resourceUri, check_mode=False, force=False):
    """
    Retrieve a specific configured resource
    """
    ret_obj = search(
        isamAppliance,
        server=server,
        resourceUri=resourceUri,
        check_mode=check_mode,
        force=force,
    )
    resource_id = ret_obj["data"]

    if resource_id == {}:
        logger.info(
            f"Resource {server}/{resourceUri} had no match, skipping retrieval."
        )
        return isamAppliance.create_return_object()
    else:
        return isamAppliance.invoke_get(
            "Retrieve a specific configured resource",
            f"{uri}/{resource_id}",
        )


def get_attachments(isamAppliance, server, resourceUri, check_mode=False, force=False):
    """
    Retrieve a list of attachments for a resource
    """
    ret_obj = search(
        isamAppliance,
        server=server,
        resourceUri=resourceUri,
        check_mode=check_mode,
        force=force,
    )
    resource_id = ret_obj["data"]

    if resource_id == {}:
        logger.info(
            f"Resource {server}/{resourceUri} had no match, skipping retrieval."
        )
        return isamAppliance.create_return_object()
    else:
        return isamAppliance.invoke_get(
            "Retrieve a list of attachments for a resource",
            f"{uri}/{resource_id}/policies",
        )


def search(isamAppliance, server, resourceUri, force=False, check_mode=False):
    """
    Search server/resource uri id by name
    """
    ret_obj = get_all(isamAppliance)
    return_obj = isamAppliance.create_return_object()

    for obj in ret_obj["data"]:
        if obj["resourceUri"] == resourceUri and obj["server"] == server:
            logger.info(
                f"Found server/resourceUri {server}/{resourceUri} id: {obj['id']}"
            )
            return_obj["data"] = obj["id"]
            return_obj["rc"] = 0

    return return_obj


def authenticate(
    isamAppliance, username, password, domain="Default", check_mode=False, force=False
):
    """
    Authenticate with Security Access Manager
    """
    ret_obj = isamAppliance.invoke_post(
        "Authenticate with Security Access Manager",
        f"{uri}/pdadmin",
        {
            "command": "setCredential",
            "username": username,
            "password": password,
            "domain": domain,
        },
    )

    ret_obj["changed"] = (
        False  # Authentication call changes nothing on the appliance (HTTP POST defaults to change)
    )

    return ret_obj


def get_resources(isamAppliance, object="/WebSEAL", check_mode=False, force=False):
    """
    Retrieve a list of resources in a protected object space
    """
    ret_obj = isamAppliance.invoke_post(
        "Retrieve a list of resources in a protected object space",
        f"{uri}/pdadmin",
        {"command": "object list", "object": object},
    )

    ret_obj["changed"] = (
        False  # Resource get call changes nothing on the appliance (HTTP POST defaults to change)
    )

    return ret_obj


def config(
    isamAppliance,
    server,
    resourceUri,
    policies=[],
    policyType=None,
    policyCombiningAlgorithm=None,
    cache=None,
    check_mode=False,
    force=False,
):
    """
    Configure a resource
    Note: Please input policies with policy names (it will be converted to id's), like so:
     [{'name': '<policy name>', 'type': 'policy'}, {'name': '<policyset name>', 'type': 'policyset'},
      {'name': '<definition name>', 'type': 'definition'}]
    """
    warnings = []
    if force is False:
        ret_obj = search(isamAppliance, server, resourceUri)

    if force is True or ret_obj["data"] == {}:
        json_data = {"server": server, "resourceUri": resourceUri}
        if policyType is not None:
            if tools.version_compare(isamAppliance.facts["version"], "9.0.6.0") < 0:
                warnings.append(
                    f"Appliance at version: {isamAppliance.facts['version']}, policyType: {cache} is not supported. Needs 9.0.6.0 or higher. Ignoring policyType for this call."
                )
            else:
                json_data["type"] = policyType

        json_data["policies"] = _convert_policy_name_to_id(isamAppliance, policies)
        if policyCombiningAlgorithm is not None:
            json_data["policyCombiningAlgorithm"] = policyCombiningAlgorithm
        if cache is not None:
            if tools.version_compare(isamAppliance.facts["version"], "9.0.3.0") < 0:
                warnings.append(
                    f"Appliance at version: {isamAppliance.facts['version']}, cache: {cache} is not supported. Needs 9.0.3.0 or higher. Ignoring cache for this call."
                )
            else:
                json_data["cache"] = int(cache)
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_post(
                "Configure a resource", uri, json_data, warnings=warnings
            )

    return isamAppliance.create_return_object()


def update(
    isamAppliance,
    server,
    resourceUri,
    policyCombiningAlgorithm,
    cache=None,
    check_mode=False,
    force=False,
):
    """
    Update the policy attachment combining algorithm
    """
    warnings = []
    ret_obj = get(isamAppliance, server, resourceUri)

    if force or (
        ret_obj["data"] != {} and (
            ret_obj["data"]["policyCombiningAlgorithm"] != policyCombiningAlgorithm or ret_obj["data"]["cache"] != cache
        )
    ):
        json_data = {"policyCombiningAlgorithm": policyCombiningAlgorithm}
        if cache is not None:
            if tools.version_compare(isamAppliance.facts["version"], "9.0.3.0") < 0:
                warnings.append(
                    f"Appliance at version: {isamAppliance.facts['version']}, cache: {cache} is not supported. Needs 9.0.3.0 or higher. Ignoring cache for this call."
                )
            else:
                json_data["cache"] = int(cache)
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_put(
                "Update the policy attachment combining algorithm and cache",
                f"{uri}/{ret_obj['data']['id']}/properties",
                json_data,
                warnings=warnings,
            )

    return isamAppliance.create_return_object()


def update_attachments(
    isamAppliance,
    server,
    resourceUri,
    attachments,
    action,
    check_mode=False,
    force=False,
):
    """
    Update the attachments for a resource

    Provide attachemnts like so:
     [{'name': '<policy name>', 'type': 'policy'}, {'name': '<policyset name>', 'type': 'policyset'},
      {'name': '<definition name>', 'type': 'definition'}]
    """
    ret_obj = get(isamAppliance, server, resourceUri)
    cur_policies = ret_obj["data"]["policies"]

    if force is True or _check(cur_policies, attachments, action) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            new_policies = _convert_policy_name_to_id(isamAppliance, attachments)
            return isamAppliance.invoke_put(
                "Update the attachments for a resource",
                f"{uri}/{ret_obj['data']['id']}/policies{tools.create_query_string(action=action)}",
                new_policies,
            )
    return isamAppliance.create_return_object()


def _check(policies, attachments, action):
    # Check and see if there is even one match
    full_match = True
    partial_match = False
    for new_pol in attachments:
        match = False
        for cur_pol in policies:
            if (
                new_pol["name"] == cur_pol["name"] and new_pol["type"] == cur_pol["type"]
            ):
                logger.info(
                    f"At least one policy already exists {new_pol['type']}/{new_pol['name']}"
                )
                match = True
                break
        if match is False:
            full_match = False
        elif partial_match is False:
            partial_match = True

    # Add will be rejected if there is even one match
    if action == "add":
        logger.info(
            f"Check if there is at least one match returned: {partial_match}"
        )
        return not partial_match
    # Delete will be rejected if there is a partial match (has to be full match)
    elif action == "remove":
        logger.info(
            f"Check if there is a full match of provided policies: {full_match}"
        )
        return full_match
    # Set requires that there be a full match and the number of elements match
    elif action == "set":
        if len(policies) == len(attachments) and full_match is True:
            return False
        else:
            return True
    # Force delete will be rejected if there is no match
    elif action == "force_remove":
        logger.info(
            f"Check if there is at least one match returned: {partial_match}"
        )
        return partial_match
    else:
        from ibmsecurity.appliance.ibmappliance import IBMError

        raise IBMError("999", f"Unknown action provided: {action}")


def publish(isamAppliance, server, resourceUri, check_mode=False, force=False):
    """
    Publish the policy attachments for a resource
    """
    ret_obj = get(isamAppliance, server, resourceUri)

    if force or (
        ret_obj["data"] != {} and (
            ret_obj["data"]["deployrequired"] or not ret_obj["data"]["deployed"]
        ) and ret_obj["data"]["policies"] != []
    ):
        if check_mode:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Publish the policy attachments for a resource",
                f"{uri}/deployment/{ret_obj['data']['id']}",
                {},
            )

    return isamAppliance.create_return_object()


def publish_list(isamAppliance, attachments, check_mode=False, force=False):
    """
    Publish a list of policy attachments

    Note: provide attachments like so:
    [{'server': '<server1>', 'resourceUri': '<resourceuri1>'}, {'server': '<server2>', 'resourceUri': '<resourceuri2>'}]
    """
    id_list = []
    for attach in attachments:
        ret_obj = get(isamAppliance, attach["server"], attach["resourceUri"])
        if force is True or ret_obj["data"]["deployrequired"] is True:
            id_list.append(ret_obj["data"]["id"])
    logger.debug(f"Attachments: {id_list}")

    if len(id_list) > 0:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Publish a list of policy attachments",
                f"{uri}/deployment",
                {"policyAttachmentIds": ",".join(id_list)},
            )

    return isamAppliance.create_return_object()


def _convert_policy_name_to_id(isamAppliance, policies):
    """
    Converts this:
    [{'name': '<policy name>', 'type': 'policy'}, {'name': '<policyset name>', 'type': 'policyset'},
     {'name': '<definition name>}, 'type': 'definition'}]
    to:
    [{'id': '<policy id>', 'type': 'policy'}, {'id': '<policyset id>', 'type': 'policyset'},
     {'id': '<definition id>, 'type': 'definition'}]
    """
    pol_ids = []
    import ibmsecurity.isam.aac.access_control.policies
    import ibmsecurity.isam.aac.access_control.policy_sets
    import ibmsecurity.isam.aac.api_protection.definitions

    for pol in policies:
        name = pol["name"]
        type = pol["type"]
        if type == "policy":
            ret_obj = ibmsecurity.isam.aac.access_control.policies.search(
                isamAppliance, name
            )
            pol_id = ret_obj["data"]
            if pol_id != {}:
                logger.debug(f"Converting policy {name} to ID: {pol_id}")
            else:
                logger.warning(f"Unable to find policy {name}, skipping.")
        elif type == "policyset":
            ret_obj = ibmsecurity.isam.aac.access_control.policy_sets.search(
                isamAppliance, name
            )
            pol_id = ret_obj["data"]
            if pol_id != {}:
                logger.debug(
                    f"Converting policy set {name} to ID: {pol_id}"
                )
            else:
                logger.warning(f"Unable to find policy set {name}, skipping.")
        elif type == "definition":
            ret_obj = ibmsecurity.isam.aac.api_protection.definitions.search(
                isamAppliance, name
            )
            pol_id = ret_obj["data"]
            if pol_id != {}:
                logger.debug(
                    f"Converting api definition {name} to ID: {pol_id}"
                )
            else:
                logger.warning(
                    f"Unable to find api definition {name}, skipping."
                )
        else:
            from ibmsecurity.appliance.ibmappliance import IBMError

            raise IBMError(
                "999", f"Policy specified with unknown type: {type}/{name}"
            )

        pol_ids.append({"id": pol_id, "type": type})

    return pol_ids


def _convert_policy_id_to_name(isamAppliance, policies):
    """
    Converts this:
    [{'id': '<policy id>', 'type': 'policy'}, {'id': '<policyset id>', 'type': 'policyset'},
     {'id': '<definition id>, 'type': 'definition'}]
    to:
    [{'name': '<policy name>', 'type': 'policy'}, {'name': '<policyset name>', 'type': 'policyset'},
     {'name': '<definition name>}, 'type': 'definition'}]
    """
    pol_ids = []
    import ibmsecurity.isam.aac.access_control.policies
    import ibmsecurity.isam.aac.access_control.policy_sets
    import ibmsecurity.isam.aac.api_protection.definitions

    for pol in policies:
        pol_id = pol["id"]
        type = pol["type"]
        if type == "policy":
            ret_obj = ibmsecurity.isam.aac.access_control.policies._get(
                isamAppliance, pol_id
            )
            pol_name = ret_obj["data"]["name"]
            if pol_name != {}:
                logger.debug(
                    f"Converting policy {pol_id} to Name: {pol_name}"
                )
            else:
                logger.warning(f"Unable to find policy {pol_id}, skipping.")
        elif type == "policyset":
            ret_obj = ibmsecurity.isam.aac.access_control.policy_sets._get(
                isamAppliance, pol_id
            )
            pol_name = ret_obj["data"]["name"]
            if pol_name != {}:
                logger.debug(
                    f"Converting policy set {pol_id} to Name: {pol_name}"
                )
            else:
                logger.warning(
                    f"Unable to find policy set {pol_id}, skipping."
                )
        elif type == "definition":
            ret_obj = ibmsecurity.isam.aac.api_protection.definitions._get(
                isamAppliance, pol_id
            )
            pol_name = ret_obj["data"]["name"]
            if pol_name != {}:
                logger.debug(
                    f"Converting api definition {pol_id} to Name: {pol_name}"
                )
            else:
                logger.warning(
                    f"Unable to find api definition {pol_id}, skipping."
                )
        else:
            from ibmsecurity.appliance.ibmappliance import IBMError

            raise IBMError(
                "999",
                f"Policy specified with unknown type: {type}/{pol_id}",
            )

        pol_ids.append({"name": pol_name, "type": type})

    return pol_ids


def delete(isamAppliance, server, resourceUri, check_mode=False, force=False):
    """
    Delete a configured resource
    """
    ret_obj = search(
        isamAppliance, server, resourceUri, check_mode=check_mode, force=force
    )
    resourceID = ret_obj["data"]

    if resourceID == {}:
        logger.info(
            f"ResourceURI {server}/{resourceUri} not found, skipping delete."
        )
    else:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Delete a configured resource", f"{uri}/{resourceID}"
            )

    return isamAppliance.create_return_object()


def compare(isamAppliance1, isamAppliance2):
    """
    Compare Policy Sets between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    for obj in ret_obj1["data"]:
        del obj["id"]
        del obj["userlastmodified"]
        del obj["lastmodified"]
        del obj["datecreated"]
        del obj["lastdeployed"]
        for pol in obj["policies"]:
            del pol["id"]
            del pol["lastmodified"]
    for obj in ret_obj2["data"]:
        del obj["id"]
        del obj["userlastmodified"]
        del obj["lastmodified"]
        del obj["datecreated"]
        del obj["lastdeployed"]
        for pol in obj["policies"]:
            del pol["id"]
            del pol["lastmodified"]

    return tools.json_compare(
        ret_obj1,
        ret_obj2,
        deleted_keys=[
            "id",
            "userlastmodified",
            "lastmodified",
            "datecreated",
            "lastdeployed",
        ],
    )
