import json
import time
import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get(isdsAppliance, check_mode=False, force=False):
    """
    Get current configured server type
    """
    return isdsAppliance.invoke_get("Retrieving Server Status", "/widgets/server")


def start(isdsAppliance, serverID='directoryserver', check_mode=False, force=False):
    """
    Restart the specified appliance server
    """
    if force is True or _check(isdsAppliance, serverID, action='start') is True:
        if check_mode is True:
            return isdsAppliance.create_return_object(changed=True)
        else:
            return isdsAppliance.invoke_post("Restarting the service " + serverID,
                                             "/widgets/server/start/" + serverID,
                                             {})

    return isdsAppliance.create_return_object()


def startconfig(isdsAppliance, serverID='directoryserver', check_mode=False, force=False):
    """
    Restart the specified appliance server
    """
    if force is True or _check(isdsAppliance, serverID, action='startconfig') is True:
        if check_mode is True:
            return isdsAppliance.create_return_object(changed=True)
        else:
            return isdsAppliance.invoke_post("Restarting the service " + serverID,
                                             "/widgets/server/startconfig/" + serverID,
                                             {})

    return isdsAppliance.create_return_object()


def stop(isdsAppliance, serverID='directoryserver', check_mode=False, force=False):
    """
    Restart the specified appliance server
    """
    if force is True or _check(isdsAppliance, serverID, action='stop') is True:
        if check_mode is True:
            return isdsAppliance.create_return_object(changed=True)
        else:
            return isdsAppliance.invoke_post("Restarting the service " + serverID,
                                             "/widgets/server/stop/" + serverID,
                                             {})

    return isdsAppliance.create_return_object()


def restart(isdsAppliance, serverID='directoryserver', check_mode=False, force=False):
    """
    Restart the specified appliance server
    """
    if force is True or _check(isdsAppliance, serverID, action='restart') is True:
        if check_mode is True:
            return isdsAppliance.create_return_object(changed=True)
        else:
            return isdsAppliance.invoke_post("Restarting the service " + serverID,
                                             "/widgets/server/restart/" + serverID,
                                             {})

    return isdsAppliance.create_return_object()


def _check(isdsAppliance, serverID, action):
    """
    Check if serverID one of these acceptable values:
        directoryserver
        directoryadminserver
        directorywat
        directoryintegrator
        directoryintegratorscimtarget
        scimservice
    Note: only directoryserver supports "startconfig" action
    """

    if serverID == 'directoryserver':
        if action == 'startconfig':
            return True
        return True
    elif serverID == 'directoryadminserver':
        if action == 'startconfig':
            return False
        return True
    elif serverID == 'directorywat':
        if action == 'startconfig':
            return False
        return True
    elif serverID == 'directoryintegrator':
        if action == 'startconfig':
            return False
        return True
    elif serverID == 'directoryintegratorscimtarget':
        if action == 'startconfig':
            return False
        return True
    elif serverID == 'scimservice':
        if action == 'startconfig':
            return False
        return True
    else:
        return False
