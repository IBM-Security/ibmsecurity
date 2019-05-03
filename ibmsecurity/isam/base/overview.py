def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieve an overview of updates and licensing information
    """
    return isamAppliance.invoke_get("Retrieve an overview of updates and licensing information",
                                    "/updates/overview")


def get_licensing_info(isamAppliance, check_mode=False, force=False):
    """
    Retrieve the licensing information
    """
    return isamAppliance.invoke_get("Retrieve the licensing information",
                                    "/lum/is_licensed")
