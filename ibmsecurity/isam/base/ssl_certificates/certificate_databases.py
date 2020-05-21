import logging

logger = logging.getLogger(__name__)
requires_model = "Appliance"


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Get list of all certificate databases
    """
    return isamAppliance.invoke_get("Retrieving all current certificate database names",
                                    "/isam/ssl_certificates")


def get(isamAppliance, cert_dbase_id, check_mode=False, force=False):
    """
    Retrieving the SSL certificate database details
    """
    return isamAppliance.invoke_get("Retrieving the SSL certificate database details",
                                    "/isam/ssl_certificates/{0}/details".format(cert_dbase_id),
                                    requires_model=requires_model)


def create(isamAppliance, kdb_name, type='kdb', token_label=None, passcode=None, hsm_type=None, ip=None, port=None,
           kneti_hash=None, esn=None, rfs=None, rfs_port=None, rfs_auth=None, safenet_pw=None, check_mode=False,
           force=False):
    """
    Create a certificate database
    """
    if force is True or _check(isamAppliance, kdb_name) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post(
                "Creating certificate database '{0}'".format(kdb_name),
                "/isam/ssl_certificates",
                {
                    "kdb_name": kdb_name,
                    "type": type,
                    "token_label": token_label,
                    "passcode": passcode,
                    "hsm_type": hsm_type,
                    "ip": ip,
                    "port": port,
                    "kneti_hash": kneti_hash,
                    "esn": esn,
                    "rfs": rfs,
                    "rfs_port": rfs_port,
                    "rfs_auth": rfs_auth,
                    "safenet_pw": safenet_pw
                })

    return isamAppliance.create_return_object()


def delete(isamAppliance, cert_dbase_id, check_mode=False, force=False):
    """
    Delete a certificate database
    """
    if force is True or _check(isamAppliance, cert_dbase_id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Deleting a certificate database",
                "/isam/ssl_certificates/{0}".format(cert_dbase_id))

    return isamAppliance.create_return_object()


def export_db(isamAppliance, cert_id, filename, check_mode=False, force=False):
    """
    Export a certificate database
    """
    import os.path

    if force is True or (_check(isamAppliance, cert_id) is True and os.path.exists(filename) is False):
        if check_mode is False:  # No point downloading a file if in check_mode
            return isamAppliance.invoke_get_file(
                "Export a certificate database",
                "/isam/ssl_certificates/{0}?export".format(cert_id),
                filename)

    return isamAppliance.create_return_object()


def import_db(isamAppliance, kdb, stash, check_mode=False, force=False):
    """
    Import certificate database
    """
    # Grab the filename to use as identifier (strip path and extension)
    import os.path
    kdb_id = os.path.basename(kdb)
    kdb_id = os.path.splitext(kdb_id)[0]

    if force is True or _check(isamAppliance, kdb_id) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post_files(
                "Import certificate database",
                "/isam/ssl_certificates",
                [
                    {
                        'file_formfield': 'kdb',
                        'filename': kdb,
                        'mimetype': 'application/octet-stream'
                    },
                    {
                        'file_formfield': 'stash',
                        'filename': stash,
                        'mimetype': 'application/octet-stream'
                    }
                ],
                {})

    return isamAppliance.create_return_object()


def rename(isamAppliance, cert_id, new_name, check_mode=False, force=False):
    """
    Rename a certificate database
    """
    if force is True or _check(isamAppliance, cert_id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Renaming a certificate database",
                "/isam/ssl_certificates/{0}".format(cert_id),
                {
                    "new_name": new_name
                })

    return isamAppliance.create_return_object()


def set(isamAppliance, cert_id, description, check_mode=False, force=False):
    """
    Set description for a certificate database
    """
    desc_match = True  # This will remain True even when cert db is not found!
    if force is False:
        ret_obj = get_all(isamAppliance)
        for certdb in ret_obj['data']:
            if certdb['id'] == cert_id:
                if certdb['description'] != description:
                    desc_match = False
                break

    if force is True or desc_match is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Set description for a certificate database",
                "/isam/ssl_certificates/{0}".format(cert_id),
                {
                    "description": description
                })

    return isamAppliance.create_return_object()


def _check(isamAppliance, id):
    """
    Check if certificate database already exists
    """
    ret_obj = get_all(isamAppliance)

    for certdb in ret_obj['data']:
        if certdb['id'] == id:
            return True

    return False


def compare(isamAppliance1, isamAppliance2):
    """
    Compare certificate databases between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    # Version is last modified time of file - not worth comparing
    for cert_db in ret_obj1['data']:
        del cert_db['version']
    for cert_db in ret_obj2['data']:
        del cert_db['version']

    import ibmsecurity.utilities.tools
    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['version'])
