import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get(isamAppliance, check_mode=False, force=False):
    """
    Get current date/time settings
    """
    return isamAppliance.invoke_get("Retrieving current date and time settings",
                                    "/time_cfg")


def get_timezones(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the list of valid timezones
    """
    return isamAppliance.invoke_get("Retrieving the list of valid timezones",
                                    "/time_cfg/I18nTimezone")


def set(isamAppliance, ntpServers, timeZone="America/New_York", check_mode=False, force=False):
    """
    Update date/time settings (set NTP server and timezone)
    """
    if force is True or _check(isamAppliance, timeZone, ntpServers) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Setting date/time settings (NTP)",
                "/time_cfg",
                {
                    "dateTime": "0000-00-00 00:00:00",
                    "timeZone": timeZone,
                    "enableNtp": True,
                    "ntpServers": ntpServers
                })

    return isamAppliance.create_return_object()


def disable(isamAppliance, check_mode=False, force=False):
    """
    Disable NTP settings, leaves all other settings intact
    """
    if force is False:
        ret_obj = get(isamAppliance)

    if force is True or ret_obj['data']['ntpConfig']['enableNtp'] == True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Setting date/time settings (NTP)",
                "/time_cfg",
                {
                    'dateTime': ret_obj['data']['dateTime'],
                    'timeZone': ret_obj['data']['timeZone'],
                    'enableNtp': False,
                    'ntpServers': ','.join(ns['ntpServer'] for ns in ret_obj['data']['ntpConfig']['ntpServers'])
                })

    return isamAppliance.create_return_object()


def _check(isamAppliance, timeZone=None, ntpServers=None):
    """
    Check if NTP is already set for syncing date/time
    If timezone or ntpservers provided then also check if those values match what is currently set
    """
    ret_obj = get(isamAppliance)

    if ret_obj['data']['ntpConfig']['enableNtp']:
        logger.info("NTP is already enabled")
        if timeZone is not None and ret_obj['data']['timeZone'] != timeZone:
            logger.info("Existing timeZone is different")
            return False
        if ntpServers != None:
            existing_ntpServers = list()
            for ntps in ret_obj['data']['ntpConfig']['ntpServers']:
                existing_ntpServers.append(ntps['ntpServer'])
            logger.debug(str(sorted(existing_ntpServers)))
            logger.debug(str(sorted(ntpServers.split(','))))
            if sorted(ntpServers.split(',')) != sorted(existing_ntpServers):
                logger.debug("Existing ntpServers are different")
                return False
        return True
    else:
        return False


def compare(isamAppliance1, isamAppliance2):
    """
    Compare date/time settings between two appliances
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    # Ignore actual date / time on servers - they should be same if synced correctly
    del ret_obj1['data']['dateTime']
    del ret_obj2['data']['dateTime']

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['datetime'])
