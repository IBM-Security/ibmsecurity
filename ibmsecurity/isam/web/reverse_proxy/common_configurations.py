from _ldap import __author__
__author__ = "Don"

#Add for reverse proxy common_configuration retrieval
#Pending approval

import logging

uri = "/wga/common_configuration"

logger = logging.getLogger(__name__)

def get_all(isamAppliance, reverseproxy_id, check_mode=False, force=False):
    """
    Retrieving all common configuration for reverse proxy
    """
    return isamAppliance.invoke_get("Retrieving the all common configuration for reverse proxy",
                                    "{0}/{1}".format(uri,
                                                     reverseproxy_id))
    
def get(isamAppliance, reverseproxy_id, configuration_id, check_mode=False, force=False):
    """
    Retrieving value of specified configuration id from reverse proxy common configuration
    """
    ret_object = get_all(isamAppliance, reverseproxy_id)
    
    logger.debug("Looking for {0} value in reverse proxy {1}".format(configuration_id, reverseproxy_id))
    
    ret_value = ''
    
    try:
        ret_value = ret_object['data'][configuration_id]
    except:
        logger.error("Invalid configuration_id")
        return isamAppliance.create_return_object(data=ret_value)
    
    return isamAppliance.create_return_object(data=ret_value)
