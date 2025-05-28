import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/isam/tracing"
requires_modules = None
requires_version = "10.0.8.0"
warnings=[]

def get(isamAppliance, full_list=False, deployed_policy=False, check_mode=False, force=False):
    """
    Get tracing settings
    """
    full_uri = uri + ibmsecurity.utilities.tools.create_query_string(full_list=str(full_list).lower(), deployed_policy=str(deployed_policy).lower())
    logger.debug(f"{full_uri}")
    return isamAppliance.invoke_get("Get tracing",
                                    full_uri,
                                    requires_modules=requires_modules,
                                    requires_version=requires_version,
                                    warnings=warnings)
