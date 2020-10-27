import logging
import ibmsecurity.utilities.tools
import ibmsecurity.isam.base.network.interfaces

logger = logging.getLogger(__name__)
requires_model="Appliance"

try:
    basestring
except NameError:
    basestring = (str, bytes)


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the DNS configuration
    """
    return isamAppliance.invoke_get("Retrieving the DNS configuration",
                                    "/net/dns", requires_model=requires_model)


def set(isamAppliance, primaryServer=None, secondaryServer=None, tertiaryServer=None, searchDomains=None, auto=True,
        autoFromInterface=None, check_mode=False, force=False):
    """
    Updating the DNS configuration
    """

    if isinstance(auto, basestring):
        if auto.lower() == 'true':
            auto = True
        else:
            auto = False

    # check autoFromInterface. If it is a label replace it with corresponding interface UUID, else leave it untouched (treat as UUID)
    if autoFromInterface is not None:
      ret_obj = ibmsecurity.isam.base.network.interfaces.get_all(isamAppliance)
      for intfc in ret_obj['data']['interfaces']:
        if intfc['label'] == autoFromInterface:
          autoFromInterface = intfc['uuid']

    check_value,warnings = _check(isamAppliance, primaryServer, secondaryServer, tertiaryServer, searchDomains, auto,
                               autoFromInterface)
    if force is True or check_value is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_put(
                "Updating the DNS configuration",
                "/net/dns",
                {
                    'auto': auto,
                    'autoFromInterface': autoFromInterface,
                    'primaryServer': primaryServer,
                    'secondaryServer': secondaryServer,
                    'tertiaryServer': tertiaryServer,
                    'searchDomains': searchDomains
                }, requires_model=requires_model)

    return isamAppliance.create_return_object(warnings=warnings)


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
                                        }, requires_model=requires_model)
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
    check_value,warnings=True,ret_obj['warnings']

    check_json_data = {
        'auto': auto,
        'autoFromInterface': autoFromInterface,
        'primaryServer': primaryServer,
        'secondaryServer': secondaryServer,
        'tertiaryServer': tertiaryServer,
        'searchDomains': searchDomains
    }

    if ibmsecurity.utilities.tools.json_sort(ret_obj['data']) == ibmsecurity.utilities.tools.json_sort(check_json_data):
        check_value=True
        return check_value,warnings
    else:
        check_value = False
        return check_value,warnings


def compare(isamAppliance1, isamAppliance2):
    """
    Compare dns settings between two appliances
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
