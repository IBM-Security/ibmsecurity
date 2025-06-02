import json
import logging
import ibmsecurity.utilities.tools
from ibmsecurity.utilities import tools
from io import open

logger = logging.getLogger(__name__)

uri = "/extensions"
requires_modules = None
requires_version = "9.0.5.0"

try:
    basestring
except NameError:
    basestring = (str, bytes)


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieve installed extensions list
    """
    return isamAppliance.invoke_get(
        "Retrieve installed extensions list",
        f"{uri}/",
        requires_modules=requires_modules,
        requires_version=requires_version,
    )


def get(isamAppliance, extId, detailed=False, check_mode=False, force=False):
    """
    Retrieve installed extension by id
    """
    if detailed:
        ret_obj = isamAppliance.invoke_get(
            "Retrieve details about installed extension",
            f"{uri}/{extId}",
            requires_modules=requires_modules,
            requires_version=requires_version,
        )
        return ret_obj
    else:
        ret_obj = isamAppliance.create_return_object()
        extensions = get_all(isamAppliance)
        for obj in extensions["data"]:
            if obj["id"] == extId:
                ret_obj["data"] = obj
                break
        return ret_obj


def add(
    isamAppliance,
    extension,
    config_data=None,
    third_party_package=None,
    check_mode=False,
    force=False,
):
    """
    Installing an Extension

    :param isamAppliance:
    :param extension: path/filename to .ext file
    :param config_data: all the config data in a single string.  For example, "agentName:ISAM_Monitoring,ipAddress:10.10.10.10,port:9998"
    :                   or pass dictionary of parameters
    :param third_party_package: an array of the supporting files required.
    :param check_mode:
    :param force:
    :return:
    """

    if extension is None:
        warning_str = "extension is required for add"
        return isamAppliance.create_return_object(warnings=[warning_str])
    try:
        extId = inspect(isamAppliance, extension)
        logger.debug(f"We got {extId}")
    except Exception as e:
        warning_str = f"Exception occurred: {e}"
        return isamAppliance.create_return_object(warnings=[warning_str])

    config_str = _get_config_data(extId, config_data)

    files = {}

    # files['extension_support_package'] = (tools.path_leaf(extension), open(extension, 'rb'))
    files["config_data"] = (None, config_str)

    if third_party_package:
        if isinstance(third_party_package, basestring):
            files["third_party_package"] = (
                tools.path_leaf(third_party_package),
                open(third_party_package, "rb"),
            )
        elif len(third_party_package) == 1:
            files["third_party_package"] = (
                tools.path_leaf(third_party_package[0]),
                open(third_party_package[0], "rb"),
            )
        else:
            counter = 0
            for file in third_party_package:
                third_party = f"third_party_package{counter}"
                files[third_party] = (tools.path_leaf(file), open(file, "rb"))
                counter = counter + 1

    if check_mode:
        return isamAppliance.create_return_object(changed=True)

    return isamAppliance.invoke_post_files(
        "Installing an Extension",
        f"{uri}/activate",
        [],
        files,
        requires_modules=requires_modules,
        requires_version=requires_version,
        json_response=False,
        data_as_files=True,
    )


def update(
    isamAppliance,
    extId,
    config_data=None,
    third_party_package=None,
    check_mode=False,
    force=False,
):
    """
    Update an existing installed extension

    :param isamAppliance:
    :param extId: extension id
    :param config_data: all the config data in a single string.  For example, "agentName:ISAM_Monitoring,ipAddress:10.10.10.10,port:9998"
    :param third_party_package: list of third_party files
    :param check_mode:
    :param force:
    :return:
    """

    if force or search(isamAppliance, extId=extId):
        if check_mode:
            return isamAppliance.create_return_object(changed=True)
        else:
            config_str = _get_config_data(extId, config_data)
            logger.debug("\nCONFIGDATA from input\n" + config_str)
            if not force:
                # Compare .  It's not possible to compare the extension (gui_json) itself, since we don't expect the extension here
                currentConfigData = get(isamAppliance, extId=extId, detailed=True)
                currentConfigData = currentConfigData.get('data', {'config_data': ''})
                currentConfigData = currentConfigData.get('config_data', '')

                currentConfigDataStr = json.dumps(currentConfigData, skipkeys=True, sort_keys=True)

                logger.debug("\nCURRENT CONFIGDATA\n" + currentConfigDataStr)

                if config_str == currentConfigDataStr:
                    return isamAppliance.create_return_object(changed=False)

            files = {}
            files["config_data"] = (None, config_str)

            if third_party_package:
                if isinstance(third_party_package, basestring):
                    files["third_party_package"] = (
                        tools.path_leaf(third_party_package),
                        open(third_party_package, "rb"),
                    )
                elif len(third_party_package) == 1:
                    files["third_party_package"] = (
                        tools.path_leaf(third_party_package[0]),
                        open(third_party_package[0], "rb"),
                    )
                else:
                    counter = 0
                    for file in third_party_package:
                        third_party = f"third_party_package{counter}"
                        files[third_party] = (tools.path_leaf(file), open(file, "rb"))
                        counter = counter + 1

            return isamAppliance.invoke_post_files(
                "Update an Extension",
                f"{uri}/{extId}",
                [],
                files,
                requires_modules=requires_modules,
                requires_version=requires_version,
                json_response=False,
                data_as_files=True,
            )

    return isamAppliance.create_return_object()


def set(
    isamAppliance,
    extension=None,
    extId=None,
    config_data=None,
    third_party_package=None,
    check_mode=False,
    force=False,
):

    # MUST have an extId to do an update.
    # Also, some extensions do not like updates, they require delete/add
    if extId and search(isamAppliance, extId):
        return update(
            isamAppliance=isamAppliance,
            extId=extId,
            config_data=config_data,
            third_party_package=third_party_package,
            check_mode=check_mode,
            force=force,
        )
    else:
        return add(
            isamAppliance=isamAppliance,
            extension=extension,
            config_data=config_data,
            third_party_package=third_party_package,
            check_mode=check_mode,
            force=force,
        )


def delete(isamAppliance, extId, check_mode=False, force=False):
    """
    Delete an installed extension
    """
    if force is True or search(isamAppliance, extId=extId):
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Delete an installed extension", f"{uri}/{extId}"
            )

    return isamAppliance.create_return_object(changed=False)


def inspect(isamAppliance, extension, check_mode=False, force=False):
    """
    Inspect the extension file to find the id for the extension.

    :param isamAppliance:
    :param extension:
    :param check_mode:
    :param force:
    :return:
    """
    obj = isamAppliance.invoke_post_files(
        "Inspect extension",
        f"{uri}/inspect",
        [
            {
                "file_formfield": "extension_support_package",
                "filename": extension,
                "mimetype": "application/octet-stream",
            }
        ],
        {},
        json_response=False,
        data_as_files=False,
        ignore_error=True,
        requires_modules=requires_modules,
        requires_version=requires_version,
    )

    # Catch the errors here
    logger.debug("INSPECT\n" + str(obj))
    if obj.get("rc", 0) == 500:
        logger.debug(
            "Api does not allow to get the name from extension if it already exists"
        )
        return None
    else:
        m_obj = obj.get("data").decode("UTF-8")

        m_obj = m_obj.replace("<textarea>", "")
        m_obj = m_obj.replace("</textarea>", "")
        logger.debug("Returned data:\n" + m_obj)

        json_obj = json.loads(m_obj)

    return json_obj["id"]


def _get_config_data(extId, config_data):
    """
    Generate a JSON payload for activate/update
    """
    if config_data is None:
        return json.dumps({"extId": extId})
    if isinstance(config_data, basestring):
        return '{"extId": "' + extId + '",' + config_data + "}"
    else:
        config_data["extId"] = extId
        return json.dumps(config_data, skipkeys=True, sort_keys=True)


def search(isamAppliance, extId, check_mode=False, force=False):
    """
    Search for the extension
    """

    ret_obj = get_all(isamAppliance)
    if extId is None:
        return False

    for obj in ret_obj["data"]:
        if obj["id"] == extId:
            return True

    return False


def compare(isamAppliance1, isamAppliance2):
    """
    Compare extensions between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    if ret_obj1["data"]:
        del ret_obj1["data"][0]["date"]
    if ret_obj2["data"]:
        del ret_obj2["data"][0]["date"]

    return ibmsecurity.utilities.tools.json_compare(
        ret_obj1, ret_obj2, deleted_keys=["date"]
    )
