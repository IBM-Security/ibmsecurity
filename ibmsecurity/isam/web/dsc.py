import logging

from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)
uri = "/isam/dsc/admin/replicas"
requires_modules = None
requires_version = None
requires_model = "Appliance"

def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the list of replica sets
    """
    return isamAppliance.invoke_get("Retrieving the list of replica sets",
                                    "{0}".format(uri),
                                    requires_modules=requires_modules, requires_version=requires_version,requires_model=requires_model)


def get_servers(isamAppliance, replica, check_mode=False, force=False):
    """
    Retrieving the list of servers for a replica set
    """
    return isamAppliance.invoke_get("Retrieving the list of servers for a replica set",
                                    "{0}/{1}/servers".format(uri, replica),
                                    requires_modules=requires_modules, requires_version=requires_version,requires_model=requires_model)


def get_session(isamAppliance, replica, user="*", max="1024", check_mode=False, force=False):
    """
    Searching for session within a replica set
    """
    return isamAppliance.invoke_get("Searching for session within a replica set",
                                    "{0}/{1}/sessions{2}".format(uri, replica,
                                                                 tools.create_query_string(user=user, max=max)),
                                    requires_modules=requires_modules, requires_version=requires_version,requires_model=requires_model)


def delete(isamAppliance, replica, session, check_mode=False, force=False):
    """
    Terminating a session
    """
    check_value, warnings = _check(isamAppliance)

    if check_value is True:
        if force is True or search(isamAppliance=isamAppliance, replica=replica, session=session) is True:
            if check_mode is True:
                return isamAppliance.create_return_object(changed=True, warnings=warnings)
            else:
                return isamAppliance.invoke_delete("Terminating a session",
                                                   "{0}/{1}/sessions/session/{2}".format(uri, replica, session),
                                                   requires_modules=requires_modules, requires_version=requires_version,
                                                   requires_model=requires_model)

    return isamAppliance.create_return_object(warnings=warnings)


def delete_all(isamAppliance, replica, username, check_mode=False, force=False):
    """
    Terminating all sessions for a single user
    """
    check_value, warnings = _check(isamAppliance)

    if check_value is True:
        if force is True or search(isamAppliance=isamAppliance, replica=replica, username=username) is True:
            if check_mode is True:
                return isamAppliance.create_return_object(changed=True, warnings=warnings)
            else:
                return isamAppliance.invoke_delete("Terminating all sessions for a single user",
                                                   "{0}/{1}/sessions/user/{2}".format(uri, replica, username),
                                                   requires_modules=requires_modules,
                                                   requires_version=requires_version, requires_model=requires_model)

    return isamAppliance.create_return_object(warnings=warnings)


def search(isamAppliance, replica, session=None, username=None, check_mode=False, force=False):

    ret_obj = get_all(isamAppliance)
    warnings = ret_obj['warnings']

    if warnings and 'Docker' in warnings[0]:
        return False

    if session != None:
        ret_obj = get_session(isamAppliance, replica)
        data = ret_obj['data']['matched_sessions']
        for obj in data:
            if obj['session'] == session:
                return True
    elif username != None:
        ret_obj = get_session(isamAppliance, replica, user=username, max=1)
        data = ret_obj['data']['matched_sessions']
        if len(data) == 1:
            return True


def _check(isamAppliance):
    """
    Check if it's appliance or not
    :param isamAppliance:
    :return: true|false, warnings message
    """
    ret_obj = get_all(isamAppliance)
    check_value, warnings=False, ret_obj['warnings']

    if warnings == []:
        check_value = True
        return check_value, warnings
    else:
        return check_value, warnings
