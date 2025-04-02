import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/db_object"


def get(isvgAppliance, check_mode=False, force=False):
    """
    Retrieve identity data store configuration
    """
    return isvgAppliance.invoke_get("Retrieve identity data store configuration entries", "{0}".format(uri))


def search(isvgAppliance, name, check_mode=False, force=False):
    """
    Search for existing identity data store configuration.
    """
    ret_obj = get(isvgAppliance)
    return_obj = isvgAppliance.create_return_object()

    for obj in ret_obj['data']:
        if 'name' in obj and obj['name'] == name:
            logger.info("Found db entry: {0}".format(obj['name']))
            return_obj['data'] = obj
            return_obj['rc'] = 0

    return return_obj


def add(isvgAppliance, name, hostName, port, dbName, adminName, adminPwd, userName, userPwd, configuredAs, retryInterval, maximumRetries, existingDB, oracleSvce, oracleLocationName, dropTables, useSSL, altServerNames, altPortNumbers, connTimeOut, maxConn, minConn, reapTime, agedTimeout, unusedTimeout, check_mode=False, force=False):
    """
    Updating identity data store configuration
    """
    if force is True:
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True)
        else:
            if existingDB == ['true']:
                # Reconfiguration does not update the database schema. It configures only the Identity Manager database details.
                action = "reconfigure"
            else:
                # Configuration updates the database schema, in addition it configures the Identity Manager database details.
                action = "configure"

            return isvgAppliance.invoke_post(
                "Configure identity data store", "{0}".format(uri),
                    {
                      "name": name,
                      "hostName": hostName,
                      "port": port,
                      "dbName": dbName,
                      "oracleLocationName": oracleLocationName,
                      "adminName": adminName,
                      "adminPwd": adminPwd,
                      "userName": userName,
                      "userPwd": userPwd,
                      "configuredAs": configuredAs,
                      "dropTables": dropTables,
                      "action": action,
                      "useSSL": useSSL,
                      "altServerNames": altServerNames,
                      "altPortNumbers": altPortNumbers,
                      "retryInterval": retryInterval,
                      "maximumRetries": maximumRetries,
                      "connTimeOut": connTimeOut,
                      "maxConn": maxConn,
                      "minConn": minConn,
                      "reapTime": reapTime,
                      "unusedTimeout": unusedTimeout,
                      "agedTimeout": agedTimeout,
                      "_isNew": True,
                      "existingDB": existingDB,
                      "oracleSvce": oracleSvce
                    })

    return isvgAppliance.create_return_object(changed=False)


def delete(isvgAppliance, name, check_mode=False, force=False):
    """
    Un-configure identity data store
    """
    ret_obj = search(isvgAppliance, name)
    warnings = ret_obj['warnings']

    if force is True or ret_obj['data'] != {}:
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            ret_obj['data'] = ret_obj['data']
            uuid = ret_obj['data']['uuid']
            return isvgAppliance.invoke_delete(
                "Un-configure identity data store", "{0}/{1}".format(uri, uuid), warnings=warnings)

    return isvgAppliance.create_return_object(warnings=warnings)


def update(isvgAppliance, name, hostName, port, dbName, adminName, adminPwd, userName, userPwd, configuredAs, retryInterval, maximumRetries, existingDB, oracleSvce, oracleLocationName, dropTables, useSSL, altServerNames, altPortNumbers, connTimeOut, maxConn, minConn, reapTime, agedTimeout, unusedTimeout, check_mode=False, force=False):
    """
    Updating identity data store
    """
    ret_obj = get(isvgAppliance)
    warnings = ret_obj['warnings']

    # JSON payload of interest is at first (and only) position of array
    ret_obj['data'] = ret_obj['data'][0]

    uuid = ret_obj['data']['uuid']

    needs_update = False

    # Create a simple json with just the attributes
    json_data = {
        "name": name,
        "uuid": uuid
    }

    if 'action' in ret_obj['data']:
        del ret_obj['data']['action']
    if 'lastmodified' in ret_obj['data']:
        del ret_obj['data']['lastmodified']
    if 'certCheckSum' in ret_obj['data']:
        del ret_obj['data']['certCheckSum']

    # mandatory attributes
    if hostName is not None:
        json_data['hostName'] = hostName
    elif 'hostName' in ret_obj['data']:
        if ret_obj['data']['hostName'] is not None:
            json_data['hostName'] = ret_obj['data']['hostName']
        else:
            del ret_obj['data']['hostName']
    if port is not None:
        json_data['port'] = port
    elif 'port' in ret_obj['data']:
        if ret_obj['data']['port'] is not None:
            json_data['port'] = ret_obj['data']['port']
        else:
            del ret_obj['data']['port']
    if dbName is not None:
        json_data['dbName'] = dbName
    elif 'dbName' in ret_obj['data']:
        if ret_obj['data']['dbName'] is not None:
            json_data['dbName'] = ret_obj['data']['dbName']
        else:
            del ret_obj['data']['dbName']
    if adminName is not None:
        json_data['adminName'] = adminName
    elif 'adminName' in ret_obj['data']:
        if ret_obj['data']['adminName'] is not None:
            json_data['adminName'] = ret_obj['data']['adminName']
        else:
            del ret_obj['data']['adminName']
    if adminPwd is not None:
        json_data['adminPwd'] = adminPwd
    elif 'adminPwd' in ret_obj['data']:
        if ret_obj['data']['adminPwd'] is not None:
            json_data['adminPwd'] = ret_obj['data']['adminPwd']
        else:
            del ret_obj['data']['adminPwd']
    if userName is not None:
        json_data['userName'] = userName
    elif 'userName' in ret_obj['data']:
        if ret_obj['data']['userName'] is not None:
            json_data['userName'] = ret_obj['data']['userName']
        else:
            del ret_obj['data']['userName']
    if userPwd is not None:
        json_data['userPwd'] = userPwd
    elif 'userPwd' in ret_obj['data']:
        if ret_obj['data']['userPwd'] is not None:
            json_data['userPwd'] = ret_obj['data']['userPwd']
        else:
            del ret_obj['data']['userPwd']
    if configuredAs is not None:
        json_data['configuredAs'] = configuredAs
    elif 'configuredAs' in ret_obj['data']:
        if ret_obj['data']['configuredAs'] is not None:
            json_data['configuredAs'] = ret_obj['data']['configuredAs']
        else:
            del ret_obj['data']['configuredAs']
    if retryInterval is not None:
        json_data['retryInterval'] = retryInterval
    elif 'retryInterval' in ret_obj['data']:
        if ret_obj['data']['retryInterval'] is not None:
            json_data['retryInterval'] = ret_obj['data']['retryInterval']
        else:
            del ret_obj['data']['retryInterval']
    if maximumRetries is not None:
        json_data['maximumRetries'] = maximumRetries
    elif 'maximumRetries' in ret_obj['data']:
        if ret_obj['data']['maximumRetries'] is not None:
            json_data['maximumRetries'] = ret_obj['data']['maximumRetries']
        else:
            del ret_obj['data']['maximumRetries']
    if oracleLocationName is not None:
        json_data['oracleLocationName'] = oracleLocationName
    elif 'oracleLocationName' in ret_obj['data']:
        if ret_obj['data']['oracleLocationName'] is not None:
            json_data['oracleLocationName'] = ret_obj['data']['oracleLocationName']
        else:
            del ret_obj['data']['oracleLocationName']
    # optional attributes
    if dropTables is not None:
        json_data['dropTables'] = dropTables
    elif 'dropTables' in ret_obj['data']:
        if ret_obj['data']['dropTables'] is not None:
            json_data['dropTables'] = ret_obj['data']['dropTables']
        else:
            del ret_obj['data']['dropTables']
    if useSSL is not None:
        json_data['useSSL'] = useSSL
    elif 'useSSL' in ret_obj['data']:
        if ret_obj['data']['useSSL'] is not None:
            json_data['useSSL'] = ret_obj['data']['useSSL']
        else:
            del ret_obj['data']['useSSL']
    if altServerNames is not None:
        json_data['altServerNames'] = altServerNames
    elif 'altServerNames' in ret_obj['data']:
        if ret_obj['data']['altServerNames'] is not None:
            json_data['altServerNames'] = ret_obj['data']['altServerNames']
        else:
            del ret_obj['data']['altServerNames']
    if altPortNumbers is not None:
        json_data['altPortNumbers'] = altPortNumbers
    elif 'altPortNumbers' in ret_obj['data']:
        if ret_obj['data']['altPortNumbers'] is not None:
            json_data['altPortNumbers'] = ret_obj['data']['altPortNumbers']
        else:
            del ret_obj['data']['altPortNumbers']
    if connTimeOut is not None:
        json_data['connTimeOut'] = connTimeOut
    elif 'connTimeOut' in ret_obj['data']:
        if ret_obj['data']['connTimeOut'] is not None:
            json_data['connTimeOut'] = ret_obj['data']['connTimeOut']
        else:
            del ret_obj['data']['connTimeOut']
    if maxConn is not None:
        json_data['maxConn'] = maxConn
    elif 'maxConn' in ret_obj['data']:
        if ret_obj['data']['maxConn'] is not None:
            json_data['maxConn'] = ret_obj['data']['maxConn']
        else:
            del ret_obj['data']['maxConn']
    if minConn is not None:
        json_data['minConn'] = minConn
    elif 'minConn' in ret_obj['data']:
        if ret_obj['data']['minConn'] is not None:
            json_data['minConn'] = ret_obj['data']['minConn']
        else:
            del ret_obj['data']['minConn']
    if reapTime is not None:
        json_data['reapTime'] = reapTime
    elif 'reapTime' in ret_obj['data']:
        if ret_obj['data']['reapTime'] is not None:
            json_data['reapTime'] = ret_obj['data']['reapTime']
        else:
            del ret_obj['data']['reapTime']
    if agedTimeout is not None:
        json_data['agedTimeout'] = agedTimeout
    elif 'agedTimeout' in ret_obj['data']:
        if ret_obj['data']['agedTimeout'] is not None:
            json_data['agedTimeout'] = ret_obj['data']['agedTimeout']
        else:
            del ret_obj['data']['agedTimeout']
    if unusedTimeout is not None:
        json_data['unusedTimeout'] = unusedTimeout
    elif 'unusedTimeout' in ret_obj['data']:
        if ret_obj['data']['unusedTimeout'] is not None:
            json_data['unusedTimeout'] = ret_obj['data']['unusedTimeout']
        else:
            del ret_obj['data']['unusedTimeout']

    sorted_ret_obj = tools.json_sort(ret_obj['data'])
    sorted_json_data = tools.json_sort(json_data)
    logger.debug("Sorted Existing Data:{0}".format(sorted_ret_obj))
    logger.debug("Sorted Desired  Data:{0}".format(sorted_json_data))
    if sorted_ret_obj != sorted_json_data:
        json_data['_isNew'] = False
        json_data['action'] = "reconfigure"
        if oracleSvce is not None:
            json_data['oracleSvce'] = oracleSvce
        if existingDB is not None:
            json_data['existingDB'] = existingDB
        needs_update = True

    if force is True or needs_update is True:
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True)
        else:
            return isvgAppliance.invoke_put(
                "Update identity data store", "{0}/{1}".format(uri, uuid),
                json_data, warnings=warnings)

    return isvgAppliance.create_return_object(changed=False)


def set(isvgAppliance, name, hostName, port, dbName, adminName, adminPwd, userName, userPwd, configuredAs, retryInterval, maximumRetries, existingDB, oracleSvce, oracleLocationName, dropTables="false", useSSL=False, altServerNames="", altPortNumbers="", connTimeOut=180, maxConn=30, minConn=5, reapTime=180, agedTimeout=0, unusedTimeout=1800, check_mode=False, force=False):
    """
    Creating or Modifying a identity data store configuration
    """
    if (search(isvgAppliance, name))['data'] == {}:
        # Force the add - we already know object does not exist
        logger.info("Identity data store {0} had no match, requesting to configure.".format(name))
        return add(isvgAppliance, name, hostName, port, dbName, adminName, adminPwd, userName, userPwd, configuredAs, retryInterval, maximumRetries, existingDB, oracleSvce, oracleLocationName, dropTables, useSSL, altServerNames, altPortNumbers, connTimeOut, maxConn, minConn, reapTime, agedTimeout, unusedTimeout, check_mode=check_mode, force=True)
    else:
        # Update request
        logger.info("Identity data store {0} exists, requesting to reconfigure.".format(name))
        return update(isvgAppliance, name, hostName, port, dbName, adminName, adminPwd, userName, userPwd, configuredAs, retryInterval, maximumRetries, existingDB, oracleSvce, oracleLocationName, dropTables, useSSL, altServerNames, altPortNumbers, connTimeOut, maxConn, minConn, reapTime, agedTimeout, unusedTimeout, check_mode=check_mode, force=force)
