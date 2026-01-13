import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/isam/user_count/user_count.json"
requires_modules = ["wga"]
requires_version = '11.0.2.0'


def get(isamAppliance, use_cache_result=False, search_timeout_sec=30, check_mode=False, force=False):
    """
    Get the user count
    """
    if use_cache_result:
        use_cache_result = 'true'
    else:
        use_cache_result = 'false'

    return isamAppliance.invoke_get("Retrieve the user count",
                                    f"{uri}?use_cache_result={use_cache_result}&search_timeout_sec={search_timeout_sec}",
                                        requires_modules=requires_modules,
                                        requires_version=requires_version
                                    )
