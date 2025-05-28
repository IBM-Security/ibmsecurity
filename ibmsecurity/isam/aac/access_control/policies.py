import logging
import json
from ibmsecurity.utilities import tools
from io import open

logger = logging.getLogger(__name__)

# URI for this module
uri = "/iam/access/v8/policies"
uri_json = "/iam/access/v8/policies/json"  # new in 10.0.6.0


def get_all(
    isamAppliance,
    filter=None,
    sortBy=None,
    count=None,
    formatting="xml",
    check_mode=False,
    force=False,
):
    """
    Retrieve a list of policies

    formatting can be xml or json (actually, if it's not json, it's going to return xml) for version 10.0.6+
    """
    warnings = []
    if formatting == "json":
        if tools.version_compare(isamAppliance.facts["version"], "10.0.6.0") < 0:
            warnings.append(
                f"Appliance is at version: {isamAppliance.facts['version']}. JSON format not supported unless at least 10.0.6.0. Setting to xml."
            )
            formatting = "xml"
    if formatting == "json":
        return isamAppliance.invoke_get(
            "Retrieve a list of policies (JSON)",
            f"{uri_json}/{tools.create_query_string(filter=filter, sortBy=sortBy, count=count)}",
            warnings=warnings,
        )
    else:
        return isamAppliance.invoke_get(
            "Retrieve a list of policies",
            f"{uri}/{tools.create_query_string(filter=filter, sortBy=sortBy)}",
            warnings=warnings,
        )


def get(isamAppliance, name, formatting="xml", check_mode=False, force=False):
    """
    Retrieve a specific policy
    """
    ret_obj = search(
        isamAppliance,
        name=name,
        formatting=formatting,
        check_mode=check_mode,
        force=force,
    )
    pol_id = ret_obj["data"]

    if pol_id == {}:
        logger.info(f"Policy {name} had no match, skipping retrieval.")
        return isamAppliance.create_return_object()
    else:
        return _get(isamAppliance, pol_id, formatting=formatting)


def _get(isamAppliance, pol_id, formatting="xml"):
    """
    Retrieve a specific access control policy by id
    """
    warnings = []
    if formatting == "json":
        if tools.version_compare(isamAppliance.facts["version"], "10.0.6.0") < 0:
            warnings.append(
                "Appliance is at version: {0}. JSON format not supported unless at least 10.0.6.0. Setting to xml.".format(                    isamAppliance.facts["version"]
                )
            )
            formatting = "xml"
    if formatting == "json":
        return isamAppliance.invoke_get(
            "Retrieve a specific policy (JSON)",
            f"{uri_json}/{pol_id}",
            warnings=warnings,
        )
    else:
        return isamAppliance.invoke_get(
            "Retrieve a specific policy",
            f"{uri}/{pol_id}",
            warnings=warnings,
        )


def export_xacml(
    isamAppliance,
    name,
    filename,
    formatting="xml",
    overwrite=False,
    check_mode=False,
    force=False,
):
    """
    Export XACML for a specific policy
    """
    warnings = []
    import os.path

    if formatting == "json":
        if tools.version_compare(isamAppliance.facts["version"], "10.0.6.0") < 0:
            warnings.append(
                f"Appliance is at version: {isamAppliance.facts['version']}. JSON format not supported unless at 10.0.6.0 or higher. Setting to xml."
            )
            formatting = "xml"
    if not force:
        ret_obj = get(
            isamAppliance,
            name=name,
            formatting=formatting,
            check_mode=check_mode,
            force=force,
        )

    if force or (ret_obj["data"] != {} and not os.path.exists(filename)):
        logger.debug("\n\nDOWNLOADING\n\n")
        if not check_mode:  # No point downloading a file if in check_mode
            f = open(filename, "w")
            if formatting == "json":
                logger.debug(f"JSON DATA:\n{ret_obj['data']['policy']}")
                f.write(json.dumps(ret_obj["data"]["policy"]))
            else:
                f.write(ret_obj["data"]["policy"])
    elif ret_obj["data"] != {} and os.path.exists(filename):
        warnings.append(f"File {filename} exists already. Overwriting = {overwrite}")
        if overwrite:
            if formatting == "json":
                logger.debug(f"JSON DATA:\n{ret_obj['data']['policy']}")
                new_policy = json.dumps(ret_obj["data"]["policy"])
            else:
                new_policy = ret_obj["data"]["policy"]
            # Compare checksums
            with open(filename, "r") as myfile:
                policy = myfile.read()

            if policy == new_policy:
                warnings.append("The content is the same.")
            else:
                myfile.close()
                f = open(filename, "w")
                f.write(new_policy)
    return isamAppliance.create_return_object(warnings=warnings)


def search(isamAppliance, name, formatting="xml", force=False, check_mode=False):
    """
    Search policy id by name
    """
    ret_obj = get_all(isamAppliance, formatting=formatting)
    return_obj = isamAppliance.create_return_object()

    for obj in ret_obj["data"]:
        if obj["name"] == name:
            logger.info(f"Found Policy {name} id: {obj['id']}")
            return_obj["data"] = obj["id"]
            return_obj["rc"] = 0

    return return_obj


def set_file(
    isamAppliance,
    name,
    attributesrequired,
    policy_file,
    description="",
    dialect="urn:oasis:names:tc:xacml:2.0:policy:schema:os",
    predefined=False,
    new_name=None,
    formatting="xml",
    check_mode=False,
    force=False,
):
    import re

    # Read policy from file and call set()
    # The policy file no longer needs to contain the xml as a single line.

    with open(policy_file, "r") as myfile:
        policy = myfile.read()
        if formatting == "xml":
            # // 4. remove \n before an end tag
            policy = re.sub(r"([\w0-9>*$-._]+)\n\s+", r"\1", policy)
            # // 1. remove all white space preceding a begin element tag:
            policy = re.sub(r"[\n\s]+(<[^/])", r"\1", policy)
            # // 2. remove all white space following an end element tag:
            policy = re.sub(r"(</[a-zA-Z0-9-_.:]+>)\s+", r"\1", policy)
            # // 3. remove all white space following an empty element tag
            policy = re.sub(r"(/>)\s+", r"\1", policy)
            # // 5. remove remaining /n+any whitespace
            policy = re.sub(r"\n\s+", " ", policy)
        else:
            policy = json.loads(policy)

    return set(
        isamAppliance,
        name,
        attributesrequired,
        policy=policy,
        description=description,
        dialect=dialect,
        predefined=predefined,
        new_name=new_name,
        formatting=formatting,
        check_mode=check_mode,
        force=force,
    )


def set(
    isamAppliance,
    name,
    attributesrequired,
    policy,
    description="",
    dialect="urn:oasis:names:tc:xacml:2.0:policy:schema:os",
    predefined=False,
    new_name=None,
    formatting="xml",
    check_mode=False,
    force=False,
):
    """
    Creating or Modifying a Policy
    """
    if (search(isamAppliance, name=name, formatting=formatting))["data"] == {}:
        # Force the add - we already know policy does not exist
        logger.info(f"Policy {name} had no match, requesting to add new one.")
        return add(
            isamAppliance,
            name,
            attributesrequired,
            policy,
            description=description,
            dialect=dialect,
            predefined=predefined,
            formatting=formatting,
            check_mode=check_mode,
            force=True,
        )
    else:
        # Update request
        logger.info(f"Policy {name} exists, requesting to update.")
        return update(
            isamAppliance,
            name,
            attributesrequired,
            policy,
            description=description,
            dialect=dialect,
            predefined=predefined,
            new_name=new_name,
            formatting=formatting,
            check_mode=check_mode,
            force=force,
        )


def add(
    isamAppliance,
    name,
    attributesrequired,
    policy,
    description="",
    dialect="urn:oasis:names:tc:xacml:2.0:policy:schema:os",
    predefined=False,
    formatting="xml",
    check_mode=False,
    force=False,
):
    """
    Create a new Policy is not supported through the API in xml format

    The documentation basically states that you can only create a new policy by `duplicating` an existing policy (which means the output from a GET command)
    """
    if not force:
        ret_obj = search(isamAppliance, name, formatting=formatting)

    if force or ret_obj["data"] == {}:
        if check_mode:
            return isamAppliance.create_return_object(changed=True)
        else:
            warnings = []
            if formatting == "json":
                if (
                    tools.version_compare(isamAppliance.facts["version"], "10.0.6.0") < 0
                ):
                    warnings.append(
                        f"Appliance is at version: {isamAppliance.facts['version']}. JSON format not supported unless at least 10.0.6.0. Setting to xml."
                    )
                    formatting = "xml"
            if formatting == "json":
                logger.debug("\n\nJSON\n\n")
                json_data = {
                    "name": name,
                    "attributesRequired": attributesrequired,
                    "description": description,
                    "predefined": predefined,
                    "policy": policy,
                    "dialect": dialect,
                }
                return isamAppliance.invoke_post(
                    "Create a new Policy (JSON)", uri_json, json_data, warnings=warnings
                )
            else:
                # json.loads fails all the time with little information, also when using the output of GET (as supported/documented)
                #   to make this work, you need to ' double escape ' the xml in the output of the GET (so it looks like this : `<Policy PolicyId=\\"urn:ibm:security:rule-container:4\\"` )
                #   alternatively, use the new full json API of course, or use an xml file using set_file
                #
                #       json_data = json.loads(policy)
                # So ... lets just to string based checks on the object.
                # For it to be valid XML, it has to start with <?xml (this is not true, but it is what the output of ISVA looks like)
                if policy.startswith("<?xml"):
                    # this is xml
                    logger.info(f"Policy {name} only contains policy data")
                    json_data = {
                        "name": name,
                        "attributesrequired": attributesrequired,
                        "description": description,
                        "predefined": predefined,
                        "policy": policy,
                        "dialect": dialect,
                    }
                else:
                    # strip off the surrounding [ and ]
                    json_data = policy[1:-1]
                    logger.debug(f"\njson_data: {json_data}")
                    json_data = json.loads(json_data)
                    logger.info(f"Policy {name} contains full policy export")

                return isamAppliance.invoke_post(
                    "Create a new Policy", uri, json_data, warnings=warnings
                )

    return isamAppliance.create_return_object()


def delete(isamAppliance, name, check_mode=False, force=False):
    """
    Delete a Policy
    """
    ret_obj = search(isamAppliance, name, check_mode=check_mode, force=force)
    mech_id = ret_obj["data"]

    if mech_id == {}:
        logger.info(f"Policy {name} not found, skipping delete.")
    else:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Delete a Policy", f"{uri}/{mech_id}"
            )

    return isamAppliance.create_return_object()


def update(
    isamAppliance,
    name,
    attributesrequired,
    policy,
    description=None,
    dialect="urn:oasis:names:tc:xacml:2.0:policy:schema:os",
    predefined=False,
    new_name=None,
    formatting="xml",
    check_mode=False,
    force=False
):
    """
    Update a specified policy
    """
    warnings = []
    if formatting == "json":
        if tools.version_compare(isamAppliance.facts["version"], "10.0.6.0") < 0:
            warnings.append(
                f"Appliance is at version: {isamAppliance.facts['version']}. JSON format not supported unless at least 10.0.6.0. Setting to xml."
            )
            formatting = "xml"

    pol_id, update_required, json_data = _check(
        isamAppliance,
        name,
        attributesrequired,
        policy,
        description=description,
        dialect=dialect,
        predefined=predefined,
        new_name=new_name,
        formatting=formatting,
        warnings=warnings
    )

    if pol_id is None:
        from ibmsecurity.appliance.ibmappliance import IBMError

        raise IBMError("999", f"Cannot update data for unknown policy: {name}")

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            if formatting == "json":
                return isamAppliance.invoke_put(
                    "Update a specified policy (JSON)",
                    f"{uri_json}/{pol_id}",
                    json_data,
                )
            else:
                return isamAppliance.invoke_put(
                    "Update a specified policy",
                    f"{uri}/{pol_id}",
                    json_data,
                )

    return isamAppliance.create_return_object()


def _check(
    isamAppliance,
    name,
    attributesrequired,
    policy,
    description=None,
    dialect="urn:oasis:names:tc:xacml:2.0:policy:schema:os",
    predefined=False,
    new_name=None,
    formatting="xml",
    warnings=[]
):
    """
    Check and return True if update needed
    """
    update_required = False
    if formatting == "json":
        if tools.version_compare(isamAppliance.facts["version"], "10.0.6.0") < 0:
            warnings.append(
                f"Appliance is at version: {isamAppliance.facts['version']}. JSON format not supported unless at least 10.0.6.0. Setting to xml."
            )
            formatting = "xml"

    if formatting == "json":
        logger.info(f"Loading JSON formatted Policy with name {name}")
        json_data = {
            "attributesRequired": attributesrequired,
            "policy": policy,
            "dialect": dialect,
            "predefined": predefined,
        }
    else:
        try:
            json_data = json.loads(policy)[0]
            logger.info(f"Policy {name} contains full policy export")
            logger.info(json_data)
            json_data.pop("id", None)
            json_data.pop("datecreated", None)
            json_data.pop("dateCreated", None)
            json_data.pop("lastmodified", None)
            json_data.pop("lastModified", None)
            json_data.pop("userlastmodified", None)
            json_data.pop("userLastModified", None)
            json_data.pop("predefined", None)
        except json.decoder.JSONDecodeError:
            logger.info(f"Policy {name} only contains policy data")
            json_data = {
                "attributesrequired": attributesrequired,
                "policy": policy,
                "dialect": dialect,
                "predefined": predefined,
            }

    ret_obj = get(isamAppliance, name, formatting=formatting)
    if ret_obj["data"] == {}:
        logger.warning("Policy not found, returning no update required.")
        return None, update_required, json_data
    else:
        pol_id = ret_obj["data"]["id"]
        if new_name is not None:
            json_data["name"] = new_name
        else:
            json_data["name"] = name
        if description is not None:
            json_data["description"] = description
        else:
            ret_obj["data"].pop("description", None)
        ret_obj["data"].pop("id", None)
        ret_obj["data"].pop("datecreated", None)
        ret_obj["data"].pop("dateCreated", None)
        ret_obj["data"].pop("lastmodified", None)
        ret_obj["data"].pop("lastModified", None)
        ret_obj["data"].pop("userlastmodified", None)
        ret_obj["data"].pop("userLastModified", None)

        sorted_json_data = tools.json_sort(json_data)
        logger.debug(f"\n\nSorted input: {sorted_json_data}")
        sorted_ret_obj = tools.json_sort(ret_obj["data"])
        logger.debug(f"\n\nSorted existing data: {sorted_ret_obj}")
        if sorted_ret_obj != sorted_json_data:
            logger.info("\n\nChanges detected, update needed.\n\n")
            update_required = True

        return pol_id, update_required, json_data


def compare(isamAppliance1, isamAppliance2, formatting="json"):
    """
    Compare Policies between two appliances
    """
    ret_obj1 = get_all(isamAppliance1, formatting=formatting)
    ret_obj2 = get_all(isamAppliance2, formatting=formatting)

    for obj in ret_obj1["data"]:
        obj.pop("id")
        obj.pop("datecreated", None)
        obj.pop("dateCreated", None)
        obj.pop("lastmodified", None)
        obj.pop("lastModified", None)
        obj.pop("userlastmodified", None)
        obj.pop("userLastModified", None)
        ret_obj = get(isamAppliance1, obj["name"], formatting=formatting)
        obj["policy"] = ret_obj["data"]["policy"]
    for obj in ret_obj2["data"]:
        obj.pop("id")
        obj.pop("datecreated", None)
        obj.pop("dateCreated", None)
        obj.pop("lastmodified", None)
        obj.pop("lastModified", None)
        obj.pop("userlastmodified", None)
        obj.pop("userLastModified", None)
        ret_obj = get(isamAppliance2, obj["name"], formatting=formatting)
        obj["policy"] = ret_obj["data"]["policy"]

    return tools.json_compare(
        ret_obj1,
        ret_obj2,
        deleted_keys=["id", "userlastmodified", "lastmodified", "datecreated"],
    )
