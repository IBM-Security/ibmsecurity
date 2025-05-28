import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/iam/access/v8/dynamic_client_migration"
requires_modules = ["mga"]
requires_version = "10.0.0"


def bulk_migration(isamAppliance, definitionName, definitionId, check_mode=False, force=False):
    """
    Dynamic client bulk migration
    :param isamAppliance:
    :param definitionName:
    :param definitionId:
    :param check_mode:
    :param force:
    :return:
    """

    return isamAppliance.invoke_post(
        "Dynamic client bulk migration",
        f"{uri}",
        {
            'definitionName': definitionName,
            'definitionId': definitionId
        },
        requires_modules=requires_modules, requires_version=requires_version)


def client_migration(isamAppliance, definitionName, client_id, check_mode=False, force=False):
    """
    Dynamic client bulk migration
    :param isamAppliance:
    :param definitionName:
    :param definitionId:
    :param check_mode:
    :param force:
    :return:
    """

    return isamAppliance.invoke_post(
        "Dynamic client bulk migration",
        f"{uri}/{client_id}",
        {
            'definitionName': definitionName
        },
        requires_modules=requires_modules, requires_version=requires_version)
