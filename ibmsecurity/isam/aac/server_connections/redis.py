import logging

import json
from ibmsecurity.utilities.tools import version_compare
from ibmsecurity.utilities.tools import json_compare

logger = logging.getLogger(__name__)

# URI for this module
uri = "/mga/server_connections/redis"
requires_modules = ["mga", "federation"]
requires_version = "10.0.3.0"  # Will change if introduced in an earlier version.

def get_all(isamAppliance, check_mode=False, force=False):
   """
   Retrieving a list of all Redis connections
   """
   return isamAppliance.invoke_get("Retrieving a list of all Redis connections",
                                   f"{uri}/v1", requires_modules=requires_modules,
                                   requires_version=requires_version)


def get(isamAppliance, name=None, check_mode=False, force=False):
   """
   Retrieving a Redis connection
   """
   ret_obj = search(isamAppliance, name=name, force=force)
   id = ret_obj["data"]

   if id == {}:
       logger.info(f"Redis Service connection {name} had no match, skipping retrieval.")
       return isamAppliance.create_return_object()
   else:
       return isamAppliance.invoke_get("Retrieving a Redis Service connection",
                                       f"{uri}/{id}/v1",
                                       requires_modules=requires_modules,
                                       requires_version=requires_version)


def search(isamAppliance, name, check_mode=False, force=False):
   """
   Search UUID for named Redis Service connection
   """
   ret_obj = get_all(isamAppliance)
   return_obj = isamAppliance.create_return_object()
   return_obj["warnings"] = ret_obj["warnings"]

   for obj in ret_obj['data']:
       if obj['name'] == name:
           logger.info(f"Found Redis Service connection {name} id: {obj['uuid']}")
           return_obj['data'] = obj['uuid']
           return_obj['rc'] = 0

   return return_obj


def add(isamAppliance, name, connection, description='', connectionManager=None, servers=None, locked=False, check_mode=False, force=False):
   """
   Creating a Redis Service connection
   """
   if (search(isamAppliance, name=name))['data'] == {}:
       if check_mode is True:
           return isamAppliance.create_return_object(changed=True)
       else:
           return isamAppliance.invoke_post(
               "Creating a Redis Service connection",
               f"{uri}/v1",
               _create_json(name=name,
                            description=description,
                            locked=locked,
                            connection=connection,
                            connectionManager=connectionManager,
                            servers=servers),
               requires_modules=requires_modules, requires_version=requires_version)

   return isamAppliance.create_return_object()


def delete(isamAppliance, name, check_mode=False, force=False):
   """
   Deleting a Redis connection
   """
   ret_obj = search(isamAppliance, name, check_mode=check_mode, force=force)
   id = ret_obj["data"]

   if force is True or _check_exists(isamAppliance, name=name) is True:
       if check_mode is True:
           return isamAppliance.create_return_object(changed=True)
       else:
           return isamAppliance.invoke_delete(
               "Deleting a Redis connection",
               f"{uri}/{id}/v1", requires_modules=requires_modules,
               requires_version=requires_version)

   return isamAppliance.create_return_object()


def update(isamAppliance, name, connection, description='', locked=False, connectionManager=None, servers=None, new_name=None, ignore_password_for_idempotency=False,
          check_mode=False, force=False):
   """
   Modifying a Redis connection

   Use new_name to rename the connection
   """
   ret_obj = get(isamAppliance, name)
   warnings = ret_obj["warnings"]

   if ret_obj["data"] == {}:
       warnings.append(f"Redis connection {name} not found, skipping update.")
       return isamAppliance.create_return_object(warnings=warnings)
   else:
       id = ret_obj["data"]["uuid"]

   needs_update = False

   json_data = _create_json(name=name,
                            description=description,
                            locked=locked,
                            connection=connection,
                            connectionManager=connectionManager,
                            servers=servers)
   if new_name is not None:  # Rename condition
       json_data['name'] = new_name

   if force is not True:
       if 'uuid' in ret_obj['data']:
           del ret_obj['data']['uuid']
       if ignore_password_for_idempotency:
           if 'password' in connection:
               warnings.append("Request made to ignore password for idempotency check.")
               connection.pop('password', None)

       #remove uuid from servers
       if 'servers' in ret_obj['data']:
         for x in ret_obj['data']['servers']:
             if 'uuid' in x:
                 logger.debug(f"Deleting uuid from returned object:\n{x['uuid']}")
                 del x['uuid']

       sorted_ret_obj = json.dumps(ret_obj['data'], skipkeys=True, sort_keys=True)
       sorted_json_data = json.dumps(json_data, skipkeys=True, sort_keys=True)

       logger.debug(f"Sorted Existing Data:\n{sorted_ret_obj}")
       logger.debug(f"Sorted Desired  Data:\n{sorted_json_data}")

       if sorted_ret_obj != sorted_json_data:
           needs_update = True

       if 'password' in connection:
           warnings.append("Since existing password cannot be read - this call will not be idempotent.")
           needs_update = True

   if force is True or needs_update:
       if check_mode:
           return isamAppliance.create_return_object(changed=True, warnings=warnings)
       else:
           return isamAppliance.invoke_put(
               "Modifying a Redis connection",
               f"{uri}/{id}/v1", json_data, requires_modules=requires_modules,
               requires_version=requires_version, warnings=warnings)

   return isamAppliance.create_return_object(warnings=warnings)

def set(isamAppliance, name, connection, description='', locked=False, new_name=None, connectionManager=None, servers=None, ignore_password_for_idempotency=False, check_mode=False, force=False):
   """
   Creating or Modifying a Redis connection
   """
   if (search(isamAppliance, name=name))['data'] == {}:
       # Force the add - we already know connection does not exist
       return add(isamAppliance=isamAppliance, name=name, connection=connection, description=description,
                  locked=locked, connectionManager=connectionManager, servers=servers, check_mode=check_mode, force=True)
   else:
       # Update request
       return update(isamAppliance=isamAppliance, name=name, connection=connection, description=description,
                     locked=locked, connectionManager=connectionManager, servers=servers,
                     new_name=new_name, ignore_password_for_idempotency=ignore_password_for_idempotency,
                     check_mode=check_mode, force=force)

def _create_json(name, description, locked, connection, connectionManager=None, servers=None):
   """
   Create a JSON to be used for the REST API call
   """
   _json = {
       "connection": connection,
       "type": "redis",
       "name": name,
       "description": description,
       "locked": locked
   }
   if connectionManager is not None:
       _json['connectionManager'] = connectionManager
   if servers is not None:
       _json['servers'] = servers
   return _json


def compare(isamAppliance1, isamAppliance2):
   """
   Compare Redis connections between two appliances
   """
   ret_obj1 = get_all(isamAppliance1)
   ret_obj2 = get_all(isamAppliance2)

   for obj in ret_obj1['data']:
       del obj['uuid']
   for obj in ret_obj2['data']:
       del obj['uuid']

   return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['uuid'])


def _check_exists(isamAppliance, name=None, id=None):
   """
   Check if Redis Connection already exists
   """
   ret_obj = get_all(isamAppliance)

   for obj in ret_obj['data']:
       if (name is not None and obj['name'] == name) or (id is not None and obj['uuid'] == id):
           return True

   return False

#test connection for redis is different from the other ones (those are in connection.py)
def test(isamAppliance, name, check_mode=False, force=False):
   """
   Test Redis Connection
   Note that to be able to test the connection, the LMI needs to be restarted!
   Otherwise, you'll run into : FBTSPS137E The Redis configuration is invalid and cannot be processed
   param: name:    the name of the server_connection
   """
   if check_mode is True:
       return isamAppliance.create_return_object()

   return isamAppliance.invoke_get("Test Redis Connection", f"/iam/access/v8/testconnection/redis/{name}")
