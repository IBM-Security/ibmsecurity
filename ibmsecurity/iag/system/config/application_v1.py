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

logger = logging.getLogger(__name__)

from ibmsecurity.iag.system.config.base import Base
from ibmsecurity.iag.system.config.base import Simple
from ibmsecurity.iag.system.config.base import SimpleList
from ibmsecurity.iag.system.config.base import AutoNumber
from ibmsecurity.iag.system.config.file import File

##############################################################################

class ApplicationV1(Base):
    """
    This class is used to represent the application configuration of an IAG
    container.
    """

    def __init__(self, 
                    path,
                    hosts,
                    is_transparent         = True,
                    max_cached_connections = 0,
                    policies               = None,
                    ssl                    = None,
                    rate_limiting          = None,
                    http_transformations   = None,
                    cors_policies          = None,
                    health                 = None,
                    content_injection      = None,
                    cookies                = None):
        """
        Initialise this class instance.  The parameters are as follows:

        @param path                   : The path at which the application is 
                                        located.  The path can either be a URI 
                                        path, or a virtual host name.
        @param hosts                  : An array of server names/ports which 
                                        hosts the application.
        @param is_transparent         : A boolean which indicates whether the 
                                        path is transparent to the proxy.
        @param max_cached_connections : The maximum number of cached persistent
                                        connections to the application.
        @param policies               : An array of Policy objects which define 
                                        the authorization policy for this 
                                        application.
        @param ssl                    : An SSL object which contains the SSL 
                                        configuration associated with 
                                        the servers for this application.
        @param rate_limiting          : An array of 
                                        ibmsecurity.iag.system.config.File 
                                        objects which contain the rate limiting 
                                        policies for the application.
        @param http_transformations   : An array of HttpTransformation objects
                                        which govern the HTTP transformations
                                        which will be applied to this 
                                        application.
        @param cors_policies          : An array of CorsPolicy objects which 
                                        govern the CORS policies applied to 
                                        this application.
        @param health                 : A HealthCheck object which is used to 
                                        define the health check for this
                                        application.
        @param content_injection      : An array of ContentInjection objects 
                                        which define the content which will be 
                                        injected into responses.
        @oaram cookies                : A CookieJar object which is used to 
                                        define the cookie jar which will be 
                                        used for this application.
        """

        super(ApplicationV1, self).__init__()

        self.path                   = Simple(str, path)
        self.hosts                  = SimpleList(str, hosts)
        self.is_transparent         = Simple(bool, is_transparent)
        self.max_cached_connections = Simple(int, max_cached_connections)
        self.policies               = self._checkList(PolicyV1, policies)
        self.ssl                    = self._check(SSLV1, ssl)
        self.rate_limiting          = self._checkList(File, rate_limiting)
        self.http_transformations   = self._checkList(HttpTransformationV1, http_transformations)
        self.cors                   = self._checkList(CorsPolicyV1, cors_policies)
        self.health                 = self._check(HealthCheckV1, health)
        self.content_injection      = self._checkList(ContentInjectionV1, content_injection)
        self.cookies                = self._check(CookieJarV1, cookies)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"

##############################################################################

class PolicyV1(Base):
    """
    This class is used to represent a single authorization policy definition.
    """

    def __init__(self,
                    path,
                    methods,
                    attributes):
        """
        Initialise this class instance.  The parameters are as follows:

        @param path       : The path which this policy applies to.
        @param method     : An array of methods which this policy applies to.
        @param attributes : A dictionary of attributes which must be
                            matched in the credential in order for the
                            authorization to be granted.
        """

        super(PolicyV1, self).__init__()

        self.path       = Simple(str, path)
        self.methods    = SimpleList(str, methods)
        self.attributes = Simple(dict, attributes)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"

##############################################################################

class SSLV1(Base):
    """
    This class is used to represent the SSL configuration to an application
    server.
    """

    def __init__(self,
                    tlsv1_0        = False,
                    tlsv1_1        = False,
                    tlsv1_2        = True,
                    tlsv1_3        = True,
                    nist_compliant = True):
        """
        Initialise this class instance.  The parameters are as follows:

        @param tlsv1_0        : A boolean which indicates whether TLS v1.0
                                support will be enabled.
        @param tlsv1_1        : A boolean which indicates whether TLS v1.1
                                support will be enabled.
        @param tlsv1_2        : A boolean which indicates whether TLS v1.2
                                support will be enabled.
        @param tlsv1_3        : A boolean which indicates whether TLS v1.3
                                support will be enabled.
        @param nist_compliant : A boolean which indicates whether only NIST
                                compliant ciphers will be used.
        """

        super(SSLV1, self).__init__()

        self.tlsv1_0        = Simple(bool, tlsv1_0)
        self.tlsv1_1        = Simple(bool, tlsv1_1)
        self.tlsv1_2        = Simple(bool, tlsv1_2)
        self.tlsv1_3        = Simple(bool, tlsv1_3)
        self.nist_compliant = Simple(bool, nist_compliant)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"

##############################################################################

class HttpTransformationV1(Base):
    """
    This class is used to represent a HTTP transformation rule for an
    application.
    """

    def __init__(self, request_match, rule):
        """
        Initialise this class instance.  The parameters are as follows:

        @param request_match : The HTTP request line to which this rule
                               will be matched.  The '*?' wildcard characters
                               may be used in the match.
        @param rule          : A ibmsecurity.iag.system.config.File object
                               which contains the XSLT transformation rule.
        """

        super(HttpTransformationV1, self).__init__()

        self.request_match = Simple(str, request_match)
        self.rule          = self._check(File, rule)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"

##############################################################################

class CorsPolicyV1(Base):
    """
    This class is used to represent a CORS policy for an application.
    """

    def __init__(self, 
                    name,
                    request_match,
                    handle_pre_flight = True,
                    allowed_origins   = None,
                    allow_credentials = True,
                    allowed_headers   = None,
                    allowed_methods   = None,
                    max_age           = 3600,
                    exposed_headers   = None):
        """
        Initialise this class instance.  The parameters are as follows:

        @param name              : The name of the CORS policy.
        @param request_match     : The HTTP request line to which this rule
                                   will be matched.  The '*?' wildcard 
                                   characters may be used in the match.
        @param handle_pre_flight : A boolean which indicates whether the proxy
                                   will handle pre-flight requests on behalf
                                   of the application.
        @param allowed_origins   : An array of origins which will be permitted
                                   to access the application.
        @param allow_credentials : A boolean which indicates whether
                                   authentication is required when accessing
                                   the application.
        @param allowed_headers   : An array of header names which will be
                                   allowed in cross-origin requests.
        @param allowed_methods   : An array of method names which will be 
                                   allowed in cross-origin requests.
        @param max_age           : The number of seconds a client should cache
                                   the results of a pre-flight request.
        @param exposed_headers   : An array of header names which the client
                                   may expose after making cross-origin
                                   requests.
        """

        super(CorsPolicyV1, self).__init__()

        self.name              = Simple(str, name)
        self.request_match     = Simple(str, request_match)
        self.handle_pre_flight = Simple(bool, handle_pre_flight)
        self.allowed_origins   = SimpleList(str, allowed_origins)
        self.allow_credentials = Simple(bool, allow_credentials)
        self.allowed_headers   = SimpleList(str, allowed_headers)
        self.allowed_methods   = SimpleList(str, allowed_methods)
        self.max_age           = Simple(int, max_age)
        self.exposed_headers   = SimpleList(str, exposed_headers)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"

##############################################################################

class HealthCheckV1(Base):
    """
    This class is used to define a health check for an application server.
    """

    def __init__(self, 
                    method,
                    uri,
                    ping_frequency          = 300,
                    ping_threshold          = 1,
                    recovery_ping_frequency = 300,
                    recovery_ping_threshold = 1,
                    timeout                 = None,
                    rules                   = None):
        """
        Initialise this class instance.  The parameters are as follows:

        @param method                  : The HTTP method which will be used
                                         when sending the health checks.
        @param uri                     : The URI to which the health check
                                         request will be sent.
        @param ping_frequency          : The frequency at which the health
                                         check requests will be sent to the
                                         server.
        @param ping_threshold          : The number of consecutive ping requests
                                         which must fail before the server
                                         is marked as unhealthy.
        @param recovery_ping_frequency : The frequency at which the health check
                                         requests will be sent to the server
                                         while it is unhealthy.
        @param recovery_ping_threshold : The number of consecutive ping requests
                                         which must succeed before an unhealthy
                                         server is marked as health.
        @param timeout                 : The timeout in seconds for sending
                                         ping requests to the server.
        @param rules                   : An array of HealthCheckRule objects
                                         which indicate the response code
                                         rules used to mark a server as 
                                         healthy or unhealthy.
        """

        super(HealthCheckV1, self).__init__()

        self.method                  = Simple(str, method)
        self.uri                     = Simple(str, uri)

        self.policy = {
            "ping_frequency"          : Simple(int, ping_frequency),
            "ping_threshold"          : Simple(int, ping_threshold),
            "recovery_ping_frequency" : Simple(int, recovery_ping_frequency),
            "recovery_ping_threshold" : Simple(int, recovery_ping_threshold),
            "timeout"                 : Simple(int, timeout),
            "rules"                   : self._checkList(HealthCheckRuleV1, rules)
        }

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"

##############################################################################

class HealthCheckRuleV1(Base):
    """
    This class is used to represent a single health check rule.  A rule 
    consists of a boolean value to indicate whether the specific response
    code is a healthy or unhealthy response.
    """

    def __init__(self,
                    is_healthy,
                    code):
        """
        Initialise this class instance.  The parameters are as follows"

        @param is_healthy : A boolean value which is used to indicate whether
                            the matching response code means that the server
                            is healthy or unhealthy.
        @param code       : The response code to match.  The '*?' wildcard
                            characters may be used.
        """

        super(HealthCheckRuleV1, self).__init__()

        self.is_healthy = self._check(bool, is_healthy)
        self.code       = self._check(str, code)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"

    def getData(self, version):
        """
        Return the data which is managed by this object.  
        """

        return "{0}{1}".format("+" if self.is_healthy else "-", self.code), \
                    version

##############################################################################

class ContentInjectionV1(Base):
    """
    This class is used to define the content which will be injected into
    application responses.
    """

    def __init__(self, path, location, data):
        """
        Initialise this class instance.  The parameters are as follows:

        @param path     : The URI path which will trigger the content injection.
        @param location : The pattern matched location within the response at 
                          which the content will be injection.
        @param data     : A ibmsecurity.iag.system.config.File object which 
                          contains the data which will be injected into the
                          response.
        """

        super(ContentInjectionV1, self).__init__()

        self.path     = Simple(str, path)
        self.location = Simple(str, location)
        self.data     = self._check(File, data)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"

##############################################################################

class CookieJarV1(Base):
    """
    This class is used to define the cookie jar for the application.  This
    will include a list of cookies to be stored in the cookie jar, as well
    as a list of cookies to be cleared from the client cookie jar when the
    session is terminated.
    """

    def __init__(self, 
                    managed = None,
                    reset   = None):
        """
        Initialise this class instance.  The parameters are as follows:

        @param managed : An array of cookie names which will be managed by the
                         cookie jar.  The '*?' wildcard characters may be used.
        @param reset   : An array of cookie names which will be cleared in the
                         client cookie jar when the session is terminated.  The
                         '*?' wildcard characters may be used.
        """

        super(CookieJarV1, self).__init__()

        self.managed = SimpleList(str, managed)
        self.reset   = SimpleList(str, reset)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"

##############################################################################

