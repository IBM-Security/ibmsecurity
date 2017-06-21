import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get(isamAppliance, check_mode=False, force=False):
    """
    Get the status of the geolocation database load
    """
    return isamAppliance.invoke_get("Retrieving geolocation DB settings...",
                                    "/iam/access/v8/geolocation-db/status")



def load(isamAppliance, file=None, check_mode=False, force=False):
    """
    Load new geolocation database
    """
    if force is True :
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
    
    return isamAppliance.invoke_put("Load new GEO Database",
                                            "/iam/access/v8/geolocation-db",
                                            {'file': file})

    #return isamAppliance.create_return_object()



