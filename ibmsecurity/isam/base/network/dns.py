import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)

try:
    basestring
except NameError:
    basestring = (str, bytes)


def get(isamAppliance, check_mode=False, force=False):
    """
    Get current dns settings
    """
    return isamAppliance.invoke_get("Retrieving current dns settings",
                                    "/net/dns")


def set(isamAppliance, primaryServer=None, secondaryServer=None, tertiaryServer=None, searchDomains=None, auto=True,
        autoFromInterface=None, check_mode=False, force=False):
    """
    Update date/time settings (set NTP server and timezone)
    """
    if isinstance(auto, basestring):
        if auto.lower() == 'true':
            auto = True
        else:
            auto = False
    if force is True or _check(isamAppliance, primaryServer, secondaryServer, tertiaryServer, searchDomains, auto,
                               autoFromInterface) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Setting dns settings",
                "/net/dns",
                {
                    'auto': auto,
                    'autoFromInterface': autoFromInterface,
                    'primaryServer': primaryServer,
                    'secondaryServer': secondaryServer,
                    'tertiaryServer': tertiaryServer,
                    'searchDomains': searchDomains
                })

    return isamAppliance.create_return_object()


def test(isamAppliance, host, server=None, force=False, check_mode=False):
    """
    Run DNS Lookup Test
    """
    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)

    ret_obj = isamAppliance.invoke_post("Run DNS Lookup Test",
                                        "/isam/net/lookup",
                                        {
                                            'host': host,
                                            'server': server
                                        })
    # HTTP POST calls get flagged as changes - but DNS lookup changes nothing so override
    if ret_obj['changed'] is True:
        ret_obj['changed'] = False

    return ret_obj


def _check(isamAppliance, primaryServer, secondaryServer, tertiaryServer, searchDomains, auto=False,
           autoFromInterface=None):
    """
    Check if DNS is already set
    """
    ret_obj = get(isamAppliance)

    check_json_data = {
        'auto': auto,
        'autoFromInterface': autoFromInterface,
        'primaryServer': primaryServer,
        'secondaryServer': secondaryServer,
        'tertiaryServer': tertiaryServer,
        'searchDomains': searchDomains
    }

    if ibmsecurity.utilities.tools.json_sort(ret_obj['data']) == ibmsecurity.utilities.tools.json_sort(check_json_data):
        return True
    else:
        return False


def compare(isamAppliance1, isamAppliance2):
    """
    Compare dns settings between two appliances
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
