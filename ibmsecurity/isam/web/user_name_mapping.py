import logging
import os.path
from ibmsecurity.utilities import tools
from io import open

logger = logging.getLogger(__name__)

# URI for this module
uri = "/wga/user_map_cdas"
requires_modules = ["wga"]
requires_version = None


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieving a list of all User Mapping CDAS files
    """
    return isamAppliance.invoke_get("Retrieving a list of all User Mapping CDAS files",
                                    "{0}/".format(uri),
                                    requires_modules=requires_modules, requires_version=requires_version)


def get(isamAppliance, name, check_mode=False, force=False):
    """
    Retrieving a User Mapping CDAS file
    """

    ret_obj = search(isamAppliance, name, check_mode=False, force=False)
    id = ret_obj['data']

    if id == {}:
        warnings = ["Retrieving a User Mapping CDAS file " + name + " does not exist"]
        logger.info("Retrieving a User Mapping CDAS file " + name + " does not exist")
        return isamAppliance.create_return_object(warnings=warnings)

    else:
        return isamAppliance.invoke_get("Retrieving a User Mapping CDAS file",
                                        "{0}/{1}".format(uri, id),
                                        requires_modules=requires_modules,
                                        requires_version=requires_version
                                        )


def get_template(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the user name mapping file template
    """

    return isamAppliance.invoke_get("Retrieving the user name mapping file template",
                                    "/isam/wga_templates/username_mapping_template",
                                    requires_modules=requires_modules,
                                    requires_version=requires_version
                                    )


def add(isamAppliance, name, contents=None, check_mode=False, force=False):
    """
    Creating a User Mapping CDAS file
    """
    ret_obj = search(isamAppliance, name, check_mode=False, force=False)
    id = ret_obj['data']

    if force is True or id == {}:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post(
                "Creating a User Mapping CDAS file",
                "{0}".format(uri),
                {
                    'name': name,
                    'content': contents
                },
                requires_modules=requires_modules, requires_version=requires_version
            )

    return isamAppliance.create_return_object()


def update(isamAppliance, name, filepath=None, contents=None, check_mode=False, force=False):
    """
    Updating an existing User Mapping CDAS file with new file or contents
    """

    warnings = []
    ret_obj = search(isamAppliance, name=name)
    id = ret_obj['data']
    update_required = False
    format = None

    if id != {}:
        ret_obj = get(isamAppliance, name)
        ret_data = ret_obj['data']['contents']

        if filepath != None:
            if os.path.exists(filepath) is True:
                openfile = open(filepath)
                filecontent = openfile.read()

                if filecontent != ret_data:
                    update_required = True
                    format = "file"
                else:
                    logger.info("User Mapping CDAS file content is the same as updates.  Skipping update.")
                    update_required = False
        elif contents != None:
            if ret_data != contents:
                update_required = True
                format = "content"
            else:
                logger.info("User Mapping CDAS file content is the same as updates.  Skipping update.")
                update_required = False
        else:
            warnings = ["Filepath and contents are both None.  Skipping update."]
            logger.info("Filepath and contents are both None.  Skipping update.")
    else:
        update_required = False
        logger.info("Did not find {0}".format(name))

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            if format == "file":
                return isamAppliance.invoke_post_files(
                    "Updating an existing User Mapping CDAS file with new file",
                    "{0}/{1}".format(uri, name),
                    [
                        {
                            'file_formfield': 'file',
                            'filename': filepath,
                            'mimetype': 'application/octet-stream'
                        }
                    ],
                    {},
                    requires_modules=requires_modules, requires_version=requires_version
                )
            else:
                return isamAppliance.invoke_post(
                    "Updating an existing User Mapping CDAS file with new file",
                    "{0}/{1}".format(uri, name),
                    {
                        'content': contents
                    },
                    requires_modules=requires_modules, requires_version=requires_version
                )

    return isamAppliance.create_return_object(warnings=warnings)


def set(isamAppliance, name, filepath=None, contents=None, check_mode=False, force=False):
    """
    Creating or Modifying a User Name Mapping
    """
    ret_obj = search(isamAppliance, name=name)
    if ret_obj['data'] == {}:
        # If no id was found, Force the add
        return add(isamAppliance, name, contents=contents, check_mode=check_mode, force=force)
    else:
        # Update
        return update(isamAppliance, name, filepath=filepath, contents=contents, check_mode=check_mode, force=force)


def delete(isamAppliance, name, check_mode=False, force=False):
    """
    Deleting a User Mapping CDAS file
    """
    ret_obj = search(isamAppliance, name=name)
    id = ret_obj['data']

    if id == {}:
        logger.info("User Mapping CDAS file '{0}' does not exists.  Skipping delete.".format(name))

    if force is True or id != {}:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:

            return isamAppliance.invoke_delete(
                "Deleting a User Mapping CDAS file",
                "{0}/{1}".format(uri, id),
                requires_modules=requires_modules, requires_version=requires_version
            )

    return isamAppliance.create_return_object()


def export_file(isamAppliance, name, filepath, check_mode=False, force=False):
    """
    Exporting a User Mapping CDAS file

    """

    ret_obj = search(isamAppliance, name=name)
    id = ret_obj['data']

    if id == {}:
        logger.info("User Mapping CDAS file '{0}' does not exists.  Skipping export file.".format(name))
        warnings = ["User Mapping CDAS file '{0}' does not exists.  Skipping export file.".format(name)]
        return isamAppliance.create_return_object(warnings=warnings)

    if os.path.exists(filepath) is True:
        logger.info("File '{0}' already exists.  Skipping export.".format(filepath))
        warnings = ["File '{0}' already exists.  Skipping export.".format(filepath)]
        return isamAppliance.create_return_object(warnings=warnings)

    if force is True or id != {}:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:

            return isamAppliance.invoke_get_file(
                "Exporting a User Mapping CDAS file",
                "{0}/{1}?export".format(uri, name), filepath,
                requires_modules=requires_modules, requires_version=requires_version
            )

    return isamAppliance.create_return_object()


def import_file(isamAppliance, filepath, check_mode=False, force=False):
    """
    Importing a User Mapping CDAS file
    """
    filename = os.path.basename(filepath)

    ret_obj = search(isamAppliance, name=filename)
    id = ret_obj['data']

    if os.path.exists(filepath) is False:
        logger.info("File '{0}' does not exists.  Skipping import.".format(filepath))
        warnings = ["File '{0}' does not exists.  Skipping import.".format(filepath)]
        return isamAppliance.create_return_object(warnings=warnings)

    if id != {}:
        logger.info("User Mapping CDAS file name '{0}' already exists.  Skipping import file.".format(filename))
        warnings = ["User Mapping CDAS file name '{0}' already exists.  Skipping import file.".format(filename)]
        return isamAppliance.create_return_object(warnings=warnings)

    if force is True or id == {}:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post_files(
                "Importing a User Mapping CDAS file",
                "{0}/".format(uri),
                [
                    {
                        'file_formfield': 'file',
                        'filename': filepath,
                        'mimetype': 'application/octet-stream'
                    }
                ],
                {},
                requires_modules=requires_modules, requires_version=requires_version
            )
    return isamAppliance.create_return_object()


def rename(isamAppliance, name, new_name, check_mode=False, force=False):
    """
    Renaming a User Mapping CDAS file
    """

    ret_obj = search(isamAppliance, name=name)
    id = ret_obj['data']

    if id == {}:
        logger.info("User Mapping CDAS file name '{0}' does not exists.  Skipping rename.".format(name))
        warnings = ["User Mapping CDAS file name '{0}' does not exists.  Skipping rename.".format(name)]
        return isamAppliance.create_return_object(warnings=warnings)

    if name == new_name:
        logger.info(
            "User Mapping CDAS file name '{0}' and new name {1} are the same.  Skipping rename.".format(name, new_name))
        return isamAppliance.create_return_object()

    if force is True or id != {}:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:

            return isamAppliance.invoke_put(
                "Renaming a User Mapping CDAS file",
                "{0}/{1}".format(uri, name),
                {"new_name": new_name},
                requires_modules=requires_modules, requires_version=requires_version
            )

    return isamAppliance.create_return_object()


def compare(isamAppliance1, isamAppliance2):
    """
    Compare user name mapping
    """

    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    for obj in ret_obj1['data']:
        ret_obj = get(isamAppliance1, obj['id'])['data']
        del obj['version']
        obj['contents'] = ret_obj['contents']
    for obj in ret_obj2['data']:
        ret_obj = get(isamAppliance2, obj['id'])['data']
        del obj['version']
        obj['contents'] = ret_obj['contents']

    return tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['version'])


def search(isamAppliance, name, force=False, check_mode=False):
    """
    Retrieve ID for named user name mapping
    """
    ret_obj = get_all(isamAppliance)

    ret_obj_new = isamAppliance.create_return_object()

    for obj in ret_obj['data']:
        if obj['id'] == name:
            logger.info("Found user name mapping '{0}' id: '{1}'".format(name, obj['id']))
            ret_obj_new['data'] = obj['id']

    return ret_obj_new
