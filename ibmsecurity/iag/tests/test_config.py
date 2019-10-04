#!/usr/local/bin/python3

"""
IBM Confidential
Object Code Only Source Materials
5725-V90
(c) Copyright International Business Machines Corp. 2020
The source code for this program is not published or otherwise divested
of its trade secrets, irrespective of what has been deposited with the
U.S. Copyright Office.
"""

import logging
import sys
import os
import traceback

from ibmsecurity.iag.system.configurator import Configurator

from ibmsecurity.iag.system.config.file        import File

from ibmsecurity.iag.system.config.server_v1 import ServerV1
from ibmsecurity.iag.system.config.server_v1 import SSLV1
from ibmsecurity.iag.system.config.server_v1 import SSLCipherV1
from ibmsecurity.iag.system.config.server_v1 import SessionV1
from ibmsecurity.iag.system.config.server_v1 import SharedSessionV1
from ibmsecurity.iag.system.config.server_v1 import WebSocketV1
from ibmsecurity.iag.system.config.server_v1 import AppV1
from ibmsecurity.iag.system.config.server_v1 import AppNames

from ibmsecurity.iag.system.config.logging_v1  import LoggingV1
from ibmsecurity.iag.system.config.logging_v1  import LoggingComponentV1
from ibmsecurity.iag.system.config.logging_v1  import LoggingStatisticV1
from ibmsecurity.iag.system.config.logging_v1  import TracingV1
from ibmsecurity.iag.system.config.logging_v1  import TransactionV1

from ibmsecurity.iag.system.config.advanced_v1 import AdvancedV1
from ibmsecurity.iag.system.config.advanced_v1 import StanzaV1

from ibmsecurity.iag.system.config.identity_v1 import IdentityV1
from ibmsecurity.iag.system.config.identity_v1 import OidcCiIdentityV1
from ibmsecurity.iag.system.config.identity_v1 import OidcIdentityV1
from ibmsecurity.iag.system.config.identity_v1 import OidcRspTypesV1
from ibmsecurity.iag.system.config.identity_v1 import OidcRspModesV1
from ibmsecurity.iag.system.config.identity_v1 import IdentityRuleV1
from ibmsecurity.iag.system.config.identity_v1 import OAuthMethodTypeV1
from ibmsecurity.iag.system.config.identity_v1 import OAuthIdentityV1

from ibmsecurity.iag.system.config.application_v1 import ApplicationV1
from ibmsecurity.iag.system.config.application_v1 import PolicyV1 
from ibmsecurity.iag.system.config.application_v1 import SSLV1 as AppSSLV1
from ibmsecurity.iag.system.config.application_v1 import HttpTransformationV1
from ibmsecurity.iag.system.config.application_v1 import CorsPolicyV1
from ibmsecurity.iag.system.config.application_v1 import HealthCheckV1
from ibmsecurity.iag.system.config.application_v1 import HealthCheckRuleV1
from ibmsecurity.iag.system.config.application_v1 import ContentInjectionV1
from ibmsecurity.iag.system.config.application_v1 import CookieJarV1

from ibmsecurity.iag.system.config.authorization_v1 import AuthorizationV1
from ibmsecurity.iag.system.config.authorization_v1 import AuthorizationRuleV1

##############################################################################
# This file is used to excercise the IAG configurator python class.

# Check the command line options.
if len(sys.argv) != 2 and len(sys.argv) != 3:
    print("Usage: {0} [out-file] {{pem-file}}".format(__file__))
    sys.exit(1)

outFile = sys.argv[1]
pemFile = sys.argv[2] if len(sys.argv) == 3 else None

logger = logging.getLogger(__file__)

try:
    #
    # Set up the front-end configuration.
    #

    ciphers   = [ 
            SSLCipherV1.SSL_RSA_FIPS_WITH_3DES_EDE_CBC_SHA, 
            SSLCipherV1.SSL_RSA_FIPS_WITH_DES_CBC_SHA 
    ]

    # 
    # Create an entry for the certificate file.  If a certificate file was
    # not provided we just use the current file.
    #
    cert = File(pemFile if pemFile is not None else __file__)

    web_socket = WebSocketV1()
    session    = SessionV1(shared_session = SharedSessionV1(secret = cert))
    ssl        = SSLV1(certificate = cert, ciphers = ciphers)
    apps       = [ AppV1(app_name = AppNames.cred_viewer, app_path = "/creds") ]
    server     = ServerV1(
                        worker_threads = 200, 
                        ssl            = ssl, 
                        websocket      = web_socket, 
                        session        = session, 
                        apps           = apps)

    #
    # Set up the logging configuration.
    #

    logging = LoggingV1(
                    components =  [ LoggingComponentV1.audit_azn, 
                                            LoggingComponentV1.audit_authn ],
                    req_log_format = "%h %l %u %t \"%r\" %s %b",
                    statistics =  [ LoggingStatisticV1(
                                    component = "pdweb.https",
                                    file_name = "/var/tmp/statistics.log") ],
                    tracing    =  [ TracingV1(
                                    component = "pdweb.snoop", 
                                    file_name = "/var/tmp/tracing.log",
                                    level     = 9) ],
                    transaction = TransactionV1(
                                    file_name = "/var/tmp/transaction.log") 
                )

    #
    # Advanced configuration.
    #

    advanced = AdvancedV1(
                    [ StanzaV1("test_stanza", 
                            { 
                                "name" : "value" ,
                                "name2" : "value2",
                                "name3" : [ "value3a", "value3b" ]
                            }) ] )

    #
    # Identity configuration.
    #

#    identity = IdentityV1(config = OidcCiIdentityV1(
#                        tenant             = "tenant",
#                        client_id          = "dummy_client_id",
#                        client_secret      = "dummy_client_secret",
#                        redirect_uri_host  = "a.ibm.com",
#                        response_type      = OidcRspTypesV1.id_token__token,
#                        response_mode      = OidcRspModesV1.form_post,
#                        proxy              = "https://proxy:3128",
#                        scopes             = [ "profile", "email2" ],
#                        allowed_query_args = [ "arg1", "arg2" ],
#                        bearer_token_attrs = [
#                                  IdentityRuleV1(False, "attr_1"), 
#                                  IdentityRuleV1(True, "*") 
#                                ],
#                        id_token_attrs = [
#                                  IdentityRuleV1(False, "id_attr_1"), 
#                                  IdentityRuleV1(True, "*") 
#                                ],
#                        mapped_identity = "identity"
#                    ))

    identity = IdentityV1(config = OAuthIdentityV1(
                        certificate            = cert,
                        introspection_endpoint = "https://introspection",
                        proxy                  = "https://proxy:3128",
                        client_id              = "dummy_client_id",
                        client_id_hdr          = "dummy_client_id_hdr",
                        client_secret          = "dummy_client_secret",
                        token_type_hint        = "hint",
                        mapped_identity        = "identity",
                        response_attrs         = [
                                  IdentityRuleV1(False, "attr_1"), 
                                  IdentityRuleV1(True, "*") 
                                ],
                        method                 = OAuthMethodTypeV1.client_secret_post,
                        multivalue_scope       = False
                    ))

#    identity = IdentityV1(config = OidcIdentityV1(
#                        certificate        = cert,
#                        discovery_endpoint = "https://discovery",
#                        client_id          = "dummy_client_id",
#                        client_secret      = "dummy_client_secret",
#                        redirect_uri_host  = "a.ibm.com",
#                        response_type      = OidcRspTypesV1.id_token__token,
#                        response_mode      = OidcRspModesV1.form_post,
#                        proxy              = "https://proxy:3128",
#                        scopes             = [ "profile", "email2" ],
#                        allowed_query_args = [ "arg1", "arg2" ],
#                        bearer_token_attrs = [
#                                  IdentityRuleV1(False, "attr_1"), 
#                                  IdentityRuleV1(True, "*") 
#                                ],
#                        id_token_attrs = [
#                                  IdentityRuleV1(False, "id_attr_1"), 
#                                  IdentityRuleV1(True, "*") 
#                                ],
#                        mapped_identity = "identity"
#                    ))

    #
    # Identity configuration.
    #

    applications = [
            ApplicationV1(
                path                   = "/path_a",
                hosts                  = [ "127.0.0.1" ],
                is_transparent         = False,
                max_cached_connections = 10,
                rate_limiting          = [ cert ],
                policies               = [ PolicyV1(
                                            "/path",
                                            [ "GET", "POST" ],
                                            { "attr_name": "attr_value" }
                                        )],
                ssl                    = AppSSLV1(
                                            tlsv1_0        = True,
                                            tlsv1_1        = True,
                                            tlsv1_2        = True,
                                            tlsv1_3        = True,
                                            nist_compliant = True),
                http_transformations   = [ HttpTransformationV1(
                                            request_match = "GET /abc *",
                                            rule          = cert
                                        )],
                cors_policies          = [ CorsPolicyV1(
                                            name              = "Cors",
                                            request_match     = "GET /abc *",
                                            handle_pre_flight = False,
                                            allowed_origins   = [ "ibm.com" ],
                                            allow_credentials = False,
                                            allowed_headers   = [ "Host" ],
                                            allowed_methods   = [ "GET" ],
                                            max_age           = 20,
                                            exposed_headers   = [ "Exposed" ]
                                        )],
                health                  = HealthCheckV1(
                                            method = "GET",
                                            uri    = "/health_check.jsp",
                                            ping_frequency          = 20,
                                            ping_threshold          = 2,
                                            recovery_ping_frequency = 20,
                                            recovery_ping_threshold = 2,
                                            timeout                 = 10,
                                            rules                   = [
                                                HealthCheckRuleV1(False, "5??"),
                                                HealthCheckRuleV1(True, "*")
                                            ]
                                        ),
                content_injection       = [ ContentInjectionV1(
                                                path     = "*",
                                                location = "<div id=\"login\"*",
                                                data     = cert
                                        )],
                cookies                 = CookieJarV1(
                                                managed = [ "Managed", "L*" ],
                                                reset = [ "RESET" ]
                                        )

            ),
            ApplicationV1(
                path  = "www.ibm.com",
                hosts = [ "a.ibm.com", "b.ibm.com" ]
            )
    ]

    authorization = AuthorizationV1(rules=[
        AuthorizationRuleV1("administrators", "(any groupIds = \"administrator\")"),
        AuthorizationRuleV1("users", "(all authenticationLevels > \"0\")"),
    ])

    #
    # Write the configuration file.
    #

    if os.path.isfile(outFile):
        os.remove(outFile)

    config = Configurator(
                    server        = server,
                    logging       = logging,
                    advanced      = advanced,
                    application   = applications,
                    authorization = authorization,
                    identity      = identity)

    config.write(outFile)

except Exception as exc:
    logger.critical(traceback.format_exc())
    sys.exit(1)

