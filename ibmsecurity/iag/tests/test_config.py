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

from ibmsecurity.iag.system.config.server_v1 import *

from ibmsecurity.iag.system.config.logging_v1  import LoggingV1
from ibmsecurity.iag.system.config.logging_v1  import LoggingComponentV1
from ibmsecurity.iag.system.config.logging_v1  import LoggingStatisticV1
from ibmsecurity.iag.system.config.logging_v1  import TracingV1
from ibmsecurity.iag.system.config.logging_v1  import TransactionV1
from ibmsecurity.iag.system.config.logging_v1  import RequestLogV1

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

from ibmsecurity.iag.system.config.applications_v1 import *

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
    session    = SessionV1()
    ssl        = SSLV1(
        front_end = SSLFrontEndV1(
            certificate=cert,
            #ciphers=ciphers
        ),
        applications = SSLApplicationsV1(

        )
    )

    apps       = AppsV1(
                       cred_viewer=CredViewerAppV1(
                                                path="cred-viewer-app"),
                       azn_decision=AznDecisionAppV1(
                                                path="azn-decision-app",
                                                max_cache_lifetime=300,
                                                max_cache_size=3600
                       )
    )
    server     = ServerV1(
                        worker_threads = 200, 
                        ssl            = ssl, 
                        websocket      = web_socket, 
                        session        = session, 
                        apps           = apps,
                        failover       = FailoverV1(key = cert))

    #
    # Set up the logging configuration.
    #

    logging = LoggingV1(
                    components =  [ LoggingComponentV1.audit_azn, 
                                            LoggingComponentV1.audit_authn ],
                    request_log = RequestLogV1(
                                    format    = "%h %l %u %t \"%r\" %s %b",
                                    file_name = "/var/tmp/request.log"),
                    statistics =  [ LoggingStatisticV1(
                                    component = "pdweb.https",
                                    file_name = "/var/tmp/statistics.log") ],
                    tracing    =  [ TracingV1(
                                    component = "pdweb.snoop", 
                                    file_name = "/var/tmp/tracing.log",
                                    level     = 9) ],
                    transaction = TransactionV1(
                                    file_name = "/var/tmp/transaction.log"),
                    json_logging = False
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
#                        tenant             = "xxx",
#                        client_id          = "xxx",
#                        client_secret      = "xxx",
#                        redirect_uri_host  = "iag"
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
        ApplicationsV1(
            path                 = "/static",
            servers                = [
                ServerV1(
                    server           = "10.10.10.200",
                    port             = 1337,
                    ssl              = ServerSSLV1(
                                         server_dn = "cn=ibm,dc=com",
                                         sni       = "test.ibm.com"
                    ),
                    url_style        = ServerURLStyleV1(
                                         case_insensitive = False,
                                         windows          = False
                    )
                )
            ],
            connection_type      = ConnectionTypeV1.tcp,
            transparent_path     = False,
            stateful             = True,
            http2                = None,
            identity_headers     = IdentityHeadersV1(
                ip_address           = True,
                encoding             = IdentityHeadersEncodingTypeV1.utf8_bin,
                basic_auth           = IdentityHeadersBasicAuthTypeV1.supply,
                session_cookie       = True
                #cred="iv_creds"
            ),
            cookies              = CookiesV1(
                #junction_cookies    = JunctionCookieV1(
                #    position            = "inhead",
                #    version             = "xhtml10",
                #    ensure_unique       = True,
                #    preserve_name       = True
                #),
            ),
            mutual_auth          = MutualAuthV1(
                basic_auth           = BasicAuthV1(
                    username             = "test",
                    password             = "passsword"
                )
            ),
            http_transformations = HttpTransformationV1(
                request              = [
                    HTTPTransformationRuleV1(
                        name             = "RequestHeaderInjector",
                        method           = "*",
                        url              = "*",
                        rule             = File("httptrans_req.xsl")
                    )
                ]
            ),
            cors                 = [CorsV1(
                name                 = "apiPolicy",
                method               = "*",
                url                  = "*",
                policy               = CorsPolicyV1(
                    allow_origins        = ["*"],
                    handle_pre_flight    = True,
                    allow_headers        = ["X-IBM"],
                    max_age              = 3600,
                    allow_methods        = ["IBMGET"],
                    allow_credentials    = True,
                    expose_headers       = ["IBMHDR"]
                )
            )],
            health               = None,
            rate_limiting        = [
                RateLimitingV1(
                    name             = "rl1",
                    methods          = ["*"],
                    url              = "rl1",
                    rule             = File("ratelimit.yaml")
                ),
                RateLimitingV1(
                    name             = "rl2",
                    methods          = ["*"],
                    url              = "rl2",
                    rule             = File("ratelimit.yaml")
                )
            ],
            content_injection    = [
                ContentInjectionV1(
                    name             = "test",
                    url              = "inject",
                    location         = "<h3>*",
                    content          = File("snippet.html")
                )
            ],
            worker_threads       = None,
            policies             = [
                PolicyV1(
                    name             = "test",
                    methods          = ["GET","PUT"],
                    url              = "*",
                    rule             = "(any groupIds = \"application owners\")",
                    action           = PolicyActionV1.deny
                ),
                PolicyV1(
                    name             = "administrators",
                    methods          = ["GET", "PUT"],
                    url              = "*",
                    action           = PolicyActionV1.deny
                )
            ]
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
                    applications  = applications,
                    authorization = authorization,
                    identity      = identity)

    config.write(outFile)

except Exception as exc:
    logger.critical(traceback.format_exc())
    sys.exit(1)

