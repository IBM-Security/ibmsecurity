import logging

import ibmsecurity.isam.web.kerberos_configuration.keyfiles
import ibmsecurity.isam.appliance


def test_export_keyfile(iviaServer, caplog) -> None:
    """Get all admincfg options."""
    caplog.set_level(logging.DEBUG)

    returnValue = ibmsecurity.isam.web.kerberos_configuration.keyfiles.export_keytab(isamAppliance=iviaServer,
                                                                    id="env.keytab",
                                                                    file="/tmp/env.keytab")
    logging.log(logging.INFO, returnValue)

    assert not returnValue.failed()
