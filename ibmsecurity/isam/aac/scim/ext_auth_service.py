import logging
import ibmsecurity.isam.aac.server_connections.ws
from ibmsecurity.utilities.tools import json_sort

logger = logging.getLogger(__name__)

uri = "/mga/scim/configuration"
requires_modules = ["mga", "federation"]
requires_version = "9.0.2"



def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the current external authentication service SCIM configuration
    """
    return isamAppliance.invoke_get("Retrieving the current external authentication service SCIM configuration ",
                                    "{0}/urn:ietf:params:scim:schemas:extension:isam:1.0:MMFA:EAS".format(uri),
                                    requires_modules=requires_modules,
                                    requires_version=requires_version
                                    )


def set(isamAppliance, connection, schemas, check_mode=False, force=False):
    """
    Updating the external authentication service SCIM configuration settings
    """
    current_objs = get(isamAppliance)
    current_configs = current_objs['data']['urn:ietf:params:scim:schemas:extension:isam:1.0:MMFA:EAS']
    ws_connections = ibmsecurity.isam.aac.server_connections.ws.get_all(isamAppliance)
    ws_connections = ws_connections['data']
    update_required = False
    uuid = None
    found = False

    for ws in ws_connections:
        if connection == ws['name']:
            uuid = ws['uuid']


    if uuid is None:
        warnings = "Did not find connection {0} in the configured server list.".format(connection)
        return isamAppliance.create_return_object(changed=False, warnings=warnings)

    for config in current_configs:
        if config['connection'] == uuid:
            found = True
            new_schemas = schemas
            old_schemas = config['schemas']
            sorted_new = json_sort(new_schemas)
            sorted_old = json_sort(old_schemas)
            if sorted_new != sorted_old:
                update_required = True

    if found is False:
        update_required = True


    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            data = []
            obj1 = {}
            obj1['connection'] = uuid
            obj1['schemas'] = schemas
            data.append(obj1)
            return isamAppliance.invoke_put("Updating the external authentication service SCIM configuration settings",
                                            "{0}/urn:ietf:params:scim:schemas:extension:isam:1.0:MMFA:EAS".format(uri),
                                            data,
                                            requires_modules=requires_modules,
                                            requires_version=requires_version
                                            )

    return isamAppliance.create_return_object(changed=False)
