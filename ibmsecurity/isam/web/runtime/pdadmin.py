import logging

try:
    basestring
except NameError:
    basestring = (str, bytes)

logger = logging.getLogger(__name__)


def execute(isamAppliance, isamUser, commands, admin_domain='Default'):
    """
    Execute a pdadmin command
    """
    logger.debug('user is: ' + isamUser.username)
    if (isinstance(commands, basestring)):
        import ast
        commands = ast.literal_eval(commands)
    return isamAppliance.invoke_post("Execute pdadmin commands", "/isam/pdadmin/",
                                     {
                                         "admin_id": isamUser.username,
                                         "admin_pwd": isamUser.password,
                                         "commands": commands,
                                         "admin_domain": admin_domain
                                     })
