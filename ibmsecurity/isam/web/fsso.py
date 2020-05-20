import logging
import os.path
from ibmsecurity.utilities import tools
from io import open

logger = logging.getLogger(__name__)

# URI for this module
uri = "/wga/fsso_config"
requires_modules = ["wga"]
requires_version = None


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieving a list of all FSSO configuration files
    """
    return isamAppliance.invoke_get("Retrieving a list of all FSSO configuration files",
                                    "{0}/".format(uri),
                                    requires_modules=requires_modules, requires_version=requires_version)


def get(isamAppliance, name, check_mode=False, force=False):
    """
    Retrieving an FSSO configuration file
    """

    ret_obj = search(isamAppliance, name, check_mode=False, force=False)
    id = ret_obj['data']

    if id == {}:
        warnings = ["Retrieving an FSSO configuration file " + name + " does not exist"]
        logger.info("Retrieving an FSSO configuration file " + name + " does not exist")
        return isamAppliance.create_return_object(warnings=warnings)

    else:
        return isamAppliance.invoke_get("Retrieving an FSSO configuration file",
                                        "{0}/{1}".format(uri, id),
                                        requires_modules=requires_modules,
                                        requires_version=requires_version
                                       )


def get_template(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the FSSO configuration file template
    """

    return isamAppliance.invoke_get("Retrieving the FSSO configuration file template",
                                    "/isam/wga_templates/fsso_template",
                                    requires_modules=requires_modules,
                                    requires_version=requires_version
                                   )


def add(isamAppliance, name, data, check_mode=False, force=False):
    """
    Creating an FSSO configuration file
    """
    ret_obj = search(isamAppliance, name, check_mode=False, force=False)
    id = ret_obj['data']

    if id != {}:
        logger.info("FSSO Configuration file '{0}' already exists.  Skipping add.".format(name))

    if force is True or id == {}:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post(
                "Creating an FSSO configuration file",
                "{0}".format(uri),
                {
                    'name': name,
                    'fsso_config_data': data
                },
                requires_modules=requires_modules, requires_version=requires_version
            )

    return isamAppliance.create_return_object()


def update(isamAppliance, name, filepath=None, data=None, check_mode=False, force=False):
    """
    Updating an existing FSSO configuration file

    """

    ret_obj = search(isamAppliance, name=name)
    id = ret_obj['data']

    contents = ""
    update_required = False

    if id != {}:
        ret_obj = get(isamAppliance, name)
        ret_data = ret_obj['data']['contents']

        if filepath != None:
            if os.path.exists(filepath) is True:
                openfile = open(filepath)
                filecontent = openfile.read()
                if filecontent != ret_data:
                    contents = filecontent
                    update_required = True
        elif data != None:
            if ret_data != data:
                contents = data
                update_required = True

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:

            return isamAppliance.invoke_put(
                "Updating an existing FSSO configuration file",
                "{0}/{1}".format(uri, name),
                {
                    'id': name,
                    'fsso_config_data': contents
                },
                requires_modules=requires_modules, requires_version=requires_version
            )

    return isamAppliance.create_return_object()


def set(isamAppliance, name, filepath='', data=None, check_mode=False, force=False):
    """
    Creating or Modifying a FSSO Configuration File
    """
    ret_obj = search(isamAppliance, name=name)
    if ret_obj['data'] == {}:
        # If no id was found, Force the add
        return add(isamAppliance, name, data=data, check_mode=check_mode, force=force)
    else:
        # Update PIP
        return update(isamAppliance, name, filepath=filepath, data=data, check_mode=check_mode, force=force)


def delete(isamAppliance, name, check_mode=False, force=False):
    """
    Deleting an FSSO configuration file
    """
    ret_obj = search(isamAppliance, name=name)
    id = ret_obj['data']

    if id == {}:
        logger.info("FSSO configuration file '{0}' does not exists.  Skipping delete.".format(name))

    if force is True or id != {}:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:

            return isamAppliance.invoke_delete(
                "Deleting an FSSO configuration file",
                "{0}/{1}".format(uri, id),
                requires_modules=requires_modules, requires_version=requires_version
            )

    return isamAppliance.create_return_object()


def export_file(isamAppliance, name, filepath, check_mode=False, force=False):
    """
    Exporting an FSSO configuration file

    """

    ret_obj = search(isamAppliance, name=name)
    id = ret_obj['data']

    if id == {}:
        logger.info("FSSO configuration file '{0}' does not exists.  Skipping export file.".format(name))
        warnings = ["FSSO configuration file '{0}' does not exists.  Skipping export file.".format(name)]
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
                "Exporting an FSSO configuration file",
                "{0}/{1}?export".format(uri, name), filepath,
                requires_modules=requires_modules, requires_version=requires_version
            )

    return isamAppliance.create_return_object()


def import_file(isamAppliance, filepath, check_mode=False, force=False):
    """
    Importing a new FSSO configuration file
    """
    filename = os.path.basename(filepath)

    ret_obj = search(isamAppliance, name=filename)
    id = ret_obj['data']

    if os.path.exists(filepath) is False:
        logger.info("File '{0}' does not exists.  Skipping import.".format(filepath))
        warnings = ["File '{0}' does not exists.  Skipping import.".format(filepath)]
        return isamAppliance.create_return_object(warnings=warnings)

    if id != {}:
        logger.info("FSSO configuration file '{0}' already exists.  Skipping import file.".format(filename))

    if force is True or id == {}:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post_files(
                "Importing a new FSSO configuration file",
                "{0}/".format(uri),
                [
                    {
                        'file_formfield': 'fsso_config_file',
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
    Renaming a FSSO configuration file
    """

    ret_obj = search(isamAppliance, name=name)
    id = ret_obj['data']

    if id == {}:
        logger.info("FSSO configuration file '{0}' does not exists.  Skipping rename.".format(name))
        warnings = ["FSSO configuration file '{0}' does not exists.  Skipping rename.".format(name)]
        return isamAppliance.create_return_object(warnings=warnings)

    if force is True or id != {}:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:

            return isamAppliance.invoke_put(
                "Renaming a FSSO configuration file",
                "{0}/{1}".format(uri, name),
                {"new_name": new_name},
                requires_modules=requires_modules, requires_version=requires_version
            )

    return isamAppliance.create_return_object()


def compare(isamAppliance1, isamAppliance2):
    """
    Compare FSSO configuration files
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
    Retrieve ID for named FSSO
    """
    ret_obj = get_all(isamAppliance)

    ret_obj_new = isamAppliance.create_return_object()

    for obj in ret_obj['data']:
        if obj['id'] == name:
            logger.info("Found FSSO '{0}' id: '{1}'".format(name, obj['id']))
            ret_obj_new['data'] = obj['id']

    return ret_obj_new
