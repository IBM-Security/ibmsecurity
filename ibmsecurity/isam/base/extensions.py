import json
import logging
import requests
from ibmsecurity.appliance.ibmappliance import IBMError
import ibmsecurity.utilities.tools
from ibmsecurity.utilities import tools

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
    return isamAppliance.invoke_get("Retrieve installed extensions list",
                                    "{0}/".format(uri), requires_modules=requires_modules,
                                    requires_version=requires_version)


def add(isamAppliance, extension, config_data=None, third_party_package=None, check_mode=False, force=False):
    """
    Installing an Extension

    :param isamAppliance:
    :param extension: path/filename to .ext file
    :param config_data: all the config data in a single string.  For example, "agentName:ISAM_Monitoring,ipAddress:10.10.10.10,port:9998"
    :param third_party_package: an array of the supporting files required.
    :param check_mode:
    :param force:
    :return:
    """

    try:
        id = inspect(isamAppliance, extension)
    except Exception as e:
        print e
        return isamAppliance.create_return_object(warnings=e)

    if config_data:
        config_str = '{extId:' + id + ',' + config_data + '}'
    else:
        config_str = '{extId:' + id + '}'

    files = {}

    files['extension_support_package'] = (tools.path_leaf(extension), open(extension, 'rb'))
    files['config_data'] = (None, config_str)

    if third_party_package:
        if isinstance(third_party_package, basestring):
            files['third_party_package'] = (tools.path_leaf(third_party_package), open(third_party_package, 'rb'))
        elif len(third_party_package) == 1:
            files['third_party_package'] = (tools.path_leaf(third_party_package[0]), open(third_party_package[0], 'rb'))
        else:
            counter = 0
            for file in third_party_package:
                third_party = 'third_party_package{0}'.format(counter)
                files[third_party] = (tools.path_leaf(file), open(file, 'rb'))
                counter = counter + 1

    if check_mode:
        return isamAppliance.create_return_object(changed=True)

    return _invoke_post_files(isamAppliance, description="Installing an Extension", uri="{0}/activate".format(uri),
                              files=files, requires_modules=requires_modules,
                              requires_version=requires_version, json_response=False)


def update(isamAppliance, extId, config_data=None, third_party_package=None, check_mode=False, force=False):
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

    if force is True or search(isamAppliance, extId=extId):
        if check_mode:
            return isamAppliance.create_return_object(changed=True)
        else:
            if config_data:
                config_str = '{extId:' + extId + ',' + config_data + '}'
            else:
                config_str = '{extId:' + extId + '}'

            files = {}

            files['config_data'] = (None, config_str)

            if third_party_package:
                if isinstance(third_party_package, basestring):
                    files['third_party_package'] = (tools.path_leaf(third_party_package), open(third_party_package, 'rb'))
                elif len(third_party_package) == 1:
                    files['third_party_package'] = (
                        tools.path_leaf(third_party_package[0]), open(third_party_package[0], 'rb'))
                else:
                    counter = 0
                    for file in third_party_package:
                        third_party = 'third_party_package{0}'.format(counter)
                        files[third_party] = (tools.path_leaf(file), open(file, 'rb'))
                        counter = counter + 1

            print files
            return _invoke_post_files(isamAppliance, description="Update an Extension",
                                      uri="{0}/{1}".format(uri, extId), files=files, requires_modules=requires_modules,
                                      json_response=False)


def set(isamAppliance, extension=None, extId=None, config_data=None, third_party_package=None, check_mode=False, force=False):
    if extId:
        if search(isamAppliance, extId):
            return update(isamAppliance=isamAppliance, extId=extId, config_data=config_data,
                          third_party_package=third_party_package, check_mode=check_mode, force=True)
    else:
        return add(isamAppliance=isamAppliance, extension=extension, config_data=config_data,
                   third_party_package=third_party_package, check_mode=check_mode, force=force)


def delete(isamAppliance, extId, check_mode=False, force=False):
    """
    Delete an installed extension
    """
    if force is True or search(isamAppliance, extId=extId):
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Delete an installed extension",
                "{0}/{1}".format(uri, extId))

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
    obj = isamAppliance.invoke_post_files("Inspect extension",
                                          "{0}/inspect".format(uri),

                                          [{
                                              'file_formfield': 'extension_support_package',
                                              'filename': extension,
                                              'mimetype': 'application/octet-stream'
                                          }],
                                          {
                                          },
                                          json_response=False, requires_modules=requires_modules,
                                          requires_version=requires_version)

    m_obj = obj['data']

    m_obj = m_obj.replace('<textarea>', '')
    m_obj = m_obj.replace('</textarea>', '')

    json_obj = json.loads(m_obj)
    return json_obj['id']


def search(isamAppliance, extId, check_mode=False, force=False):
    """
    Search for the extension
    """

    ret_obj = get_all(isamAppliance)

    for obj in ret_obj['data']:
        if obj['id'] == extId:
            return True

    return False


def _invoke_post_files(isamAppliance, description, uri, files, ignore_error=False, requires_modules=None,
                       requires_version=None, warnings=[], json_response=True):
    """
    Send multipart/form-data upload file request to extensions
    """

    isamAppliance._log_desc(description=description)

    warnings, return_call = isamAppliance._process_warnings(uri=uri, requires_modules=requires_modules,
                                                            requires_version=requires_version, warnings=warnings)
    return_obj = isamAppliance.create_return_object(warnings=warnings)
    if return_call:
        return return_obj

    # Build up the URL and header information.
    if json_response:
        headers = {
            'Accept': 'application/json,text/html,application/xhtml+xml,application/xml'
        }
    else:
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml'
        }
    isamAppliance.logger.debug("Headers are: {0}".format(headers))

    isamAppliance._suppress_ssl_warning()

    try:
        r = isamAppliance.session.post(url=isamAppliance._url(uri=uri), files=files, verify=False, headers=headers)
        return_obj['changed'] = True  # POST of file would be a change
        isamAppliance._process_response(return_obj=return_obj, http_response=r, ignore_error=ignore_error)

    except requests.exceptions.ConnectionError:
        if not ignore_error:
            isamAppliance.logger.critical("Failed to connect to server.")
            raise IBMError("HTTP Return code: 502", "Failed to connect to server")
        else:
            isamAppliance.logger.debug("Failed to connect to server.")
            return_obj.rc = 502

    return return_obj


def compare(isamAppliance1, isamAppliance2):
    """
    Compare extensions between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    if ret_obj1['data']:
        del ret_obj1['data'][0]['date']
    if ret_obj2['data']:
        del ret_obj2['data'][0]['date']

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['date'])
