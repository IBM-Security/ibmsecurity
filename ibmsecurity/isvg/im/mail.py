import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/mail_object"


def get(isvgAppliance, check_mode=False, force=False):
    """
    Retrieve mail configuration
    """
    return isvgAppliance.invoke_get("Retrieve mail configuration entries", "{0}".format(uri))


def search(isvgAppliance, name="Mail Configuration", check_mode=False, force=False):
    """
    Search for existing mail configuration.
    """
    ret_obj = get(isvgAppliance)
    return_obj = isvgAppliance.create_return_object()

    for obj in ret_obj['data']:
        if 'name' in obj and obj['name'] == name:
            logger.info("Found mail entry: {0}".format(obj['name']))
            return_obj['data'] = obj
            return_obj['rc'] = 0

    return return_obj


def add(isvgAppliance, mailFrom, mailServer, mailUser, mailPwd, mailBaseUrl, port, useSSL, check_mode=False, force=False):
    """
    Updating mail configuration
    """
    if force is True:
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True)
        else:
            return isvgAppliance.invoke_post(
                "Configure mail configuration", "{0}".format(uri),
                    {
                      "mailFrom": mailFrom,
                      "mailServer": mailServer,
                      "mailUser": mailUser,
                      "mailPwd": mailPwd,
                      "mailBaseUrl": mailBaseUrl,
                      "name":"Mail Configuration",
                      "port": port,
                      "useSSL": useSSL,
                      "_isNew": True,
                      "action": "configure"
                    })

    return isvgAppliance.create_return_object(changed=False)


def delete(isvgAppliance, name="Mail Configuration", check_mode=False, force=False):
    """
    Un-configure mail configuration
    """
    ret_obj = search(isvgAppliance, name)
    warnings = ret_obj['warnings']

    if force is True or ret_obj['data'] != {}:
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            ret_obj['data'] = ret_obj['data']
            uuid = ret_obj['data']['uuid']
            return isvgAppliance.invoke_delete(
                "Un-configure mail configuration", "{0}/{1}".format(uri, uuid), warnings=warnings)

    return isvgAppliance.create_return_object(warnings=warnings)


def update(isvgAppliance, mailFrom, mailServer, mailUser, mailPwd, mailBaseUrl, port, useSSL, check_mode=False, force=False):
    """
    Updating mail configuration
    """
    ret_obj = get(isvgAppliance)
    warnings = ret_obj['warnings']

    # JSON payload of interest is at first (and only) position of array
    ret_obj['data'] = ret_obj['data'][0]

    uuid = ret_obj['data']['uuid']

    needs_update = False

    # Create a simple json with just the attributes
    json_data = {
        "name": "Mail Configuration",
        "uuid": uuid
    }

    if 'lastModified' in ret_obj['data']:
        del ret_obj['data']['lastModified']
    if 'certCheckSum' in ret_obj['data']:
        del ret_obj['data']['certCheckSum']

    # mandatory attributes
    if mailFrom is not None:
        json_data['mailFrom'] = mailFrom
    elif 'mailFrom' in ret_obj['data']:
        if ret_obj['data']['mailFrom'] is not None:
            json_data['mailFrom'] = ret_obj['data']['mailFrom']
        else:
            del ret_obj['data']['mailFrom']
    if mailServer is not None:
        json_data['mailServer'] = mailServer
    elif 'mailServer' in ret_obj['data']:
        if ret_obj['data']['mailServer'] is not None:
            json_data['mailServer'] = ret_obj['data']['mailServer']
        else:
            del ret_obj['data']['mailServer']
    if port is not None:
        json_data['port'] = port
    elif 'port' in ret_obj['data']:
        if ret_obj['data']['port'] is not None:
            json_data['port'] = ret_obj['data']['port']
        else:
            del ret_obj['data']['port']
    if useSSL is not None:
        json_data['useSSL'] = useSSL
    elif 'useSSL' in ret_obj['data']:
        if ret_obj['data']['useSSL'] is not None:
            json_data['useSSL'] = ret_obj['data']['useSSL']
        else:
            del ret_obj['data']['useSSL']
    # optional attributes
    if mailUser is not None:
        json_data['mailUser'] = mailUser
    elif 'mailUser' in ret_obj['data']:
        if ret_obj['data']['mailUser'] is not None:
            json_data['mailUser'] = ret_obj['data']['mailUser']
        else:
            del ret_obj['data']['mailUser']
    if mailPwd is not None:
        json_data['mailPwd'] = mailPwd
    elif 'mailPwd' in ret_obj['data']:
        if ret_obj['data']['mailPwd'] is not None:
            json_data['mailPwd'] = ret_obj['data']['mailPwd']
        else:
            del ret_obj['data']['mailPwd']
    if mailBaseUrl is not None:
        json_data['mailBaseUrl'] = mailBaseUrl
    elif 'mailBaseUrl' in ret_obj['data']:
        if ret_obj['data']['mailBaseUrl'] is not None:
            json_data['mailBaseUrl'] = ret_obj['data']['mailBaseUrl']
        else:
            del ret_obj['data']['mailBaseUrl']

    sorted_ret_obj = tools.json_sort(ret_obj['data'])
    sorted_json_data = tools.json_sort(json_data)
    logger.debug("Sorted Existing Data:{0}".format(sorted_ret_obj))
    logger.debug("Sorted Desired  Data:{0}".format(sorted_json_data))
    if sorted_ret_obj != sorted_json_data:
        json_data['_isNew'] = False
        json_data['action'] = "reconfigure"
        needs_update = True

    if force is True or needs_update is True:
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True)
        else:
            return isvgAppliance.invoke_put(
                "Update mail configuration", "{0}/{1}".format(uri, uuid),
                json_data, warnings=warnings)

    return isvgAppliance.create_return_object(changed=False)


def set(isvgAppliance, mailFrom, mailServer, mailUser=None, mailPwd=None, mailBaseUrl=None, port=25, useSSL=False, check_mode=False, force=False):
    """
    Creating or Modifying a mail configuration
    """
    name = "Mail Configuration"
    if (search(isvgAppliance, name))['data'] == {}:
        # Force the add - we already know object does not exist
        logger.info("Mail entry {0} had no match, requesting to configure.".format(name))
        return add(isvgAppliance, mailFrom, mailServer, mailUser, mailPwd, mailBaseUrl, port, useSSL, check_mode=check_mode, force=True)
    else:
        # Update request
        logger.info("Mail entry {0} exists, requesting to reconfigure.".format(name))
        return update(isvgAppliance, mailFrom, mailServer, mailUser, mailPwd, mailBaseUrl, port, useSSL, check_mode=check_mode, force=force)
