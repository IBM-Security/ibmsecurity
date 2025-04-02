import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)
requires_model="Appliance"


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the current date and time settings
    """
    return isamAppliance.invoke_get("Retrieving the current date and time settings",
                                    "/time_cfg", requires_model=requires_model)


def get_timezones(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the list of valid timezones
    """
    return isamAppliance.invoke_get("Retrieving the list of valid timezones",
                                    "/time_cfg/I18nTimezone", requires_model=requires_model)


def set(isamAppliance, ntpServers="", timeZone="America/New_York", enableNtp=False, dateTime=None, check_mode=False, force=False):
    """
    Update date/time settings (set NTP server and timezone)
    """

    if dateTime is None:
        dateTime = "0000-00-00 00:00:00"

    check_value, warnings = _check(isamAppliance=isamAppliance, timeZone=timeZone, ntpServers=ntpServers, enableNtp=enableNtp)
    if force is True or check_value is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_put(
                "Setting date/time settings (NTP)",
                "/time_cfg",
                {
                    "dateTime": dateTime,
                    "timeZone": timeZone,
                    "enableNtp": enableNtp,
                    "ntpServers": ntpServers
                },
            requires_model=requires_model
            )

    return isamAppliance.create_return_object(warnings=warnings)


def disable(isamAppliance, check_mode=False, force=False):
    """
    Disable NTP settings, leaves all other settings intact
    """

    ret_obj = get(isamAppliance)
    warnings = ret_obj['warnings']

    if warnings != []:
        if "Docker" in warnings[0]:
            return isamAppliance.create_return_object(warnings=warnings)

    if force is True or ret_obj['data']['ntpConfig']['enableNtp'] == True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_put(
                "Setting date/time settings (NTP)",
                "/time_cfg",
                {
                    'dateTime': ret_obj['data']['dateTime'],
                    'timeZone': ret_obj['data']['timeZone'],
                    'enableNtp': False,
                    'ntpServers': ','.join(ns['ntpServer'] for ns in ret_obj['data']['ntpConfig']['ntpServers'])
                },
                requires_model=requires_model
            )

    return isamAppliance.create_return_object(warnings=warnings)


def _check(isamAppliance, timeZone, ntpServers, enableNtp):
    """
    Check if NTP is already set for syncing date/time
    If timezone or ntpservers provided then also check if those values match what is currently set
    """
    ret_obj = get(isamAppliance)
    warnings=ret_obj['warnings']

    if warnings != []:
        if "Docker" in warnings[0]:
            return True, warnings

    if ret_obj['data']['ntpConfig']['enableNtp'] != enableNtp:
        return False, warnings

    if timeZone != ret_obj['data']['timeZone']:
        logger.info("Existing timeZone is different")
        return False, warnings

    if ntpServers != None:
        existing_ntpServers = list()
        for ntps in ret_obj['data']['ntpConfig']['ntpServers']:
            existing_ntpServers.append(ntps['ntpServer'])
        logger.debug(str(sorted(existing_ntpServers)))
        logger.debug(str(sorted(ntpServers.split(','))))
        if sorted(ntpServers.split(',')) != sorted(existing_ntpServers):
            logger.debug("Existing ntpServers are different")
            return False, warnings

    return True, warnings


def compare(isamAppliance1, isamAppliance2):
    """
    Compare date/time settings between two appliances
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    if ret_obj1['warnings'] != []:
        if 'Docker' in ret_obj1['warnings'][0]:
            return isamAppliance1.create_return_object(warnings=ret_obj1['warnings'])

    if ret_obj2['warnings'] != []:
        if 'Docker' in ret_obj2['warnings'][0]:
            return isamAppliance2.create_return_object(warnings=ret_obj2['warnings'])

    # Ignore actual date / time on servers - they should be same if synced correctly
    if 'dateTime' in ret_obj1['data']:
        del ret_obj1['data']['dateTime']

    if 'dateTime' in ret_obj2['data']:
        del ret_obj2['data']['dateTime']

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['datetime'])
