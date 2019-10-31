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
from ibmsecurity.iag.system.config.file import File
from ibmsecurity.iag.system.config.base import AutoNumber


##############################################################################

class ApplicationV1(Base):
    """
    This class is used to represent the application configuration of an IAG
    container.
    """

    def __init__(self,
                    path                 = None,
                    virtual_host         = None,
                    virtual_host_port    = None,
                    hosts                = None,
                    app_type             = None,
                    transparent_path     = True,
                    stateful             = False,
                    http2                = None,
                    identity_headers     = None,
                    cookies              = None,
                    mutual_auth          = None,
                    http_transformations = None,
                    cors                 = None,
                    health               = None,
                    rate_limiting        = None,
                    content_injection    = None,
                    worker_threads       = None,
                    policies             = None):
        """
        Initialise this class instance.  The parameters are as follows:

        @param path                 : The path this application will be created 
                                      at. Use either this parameter or 
                                      virtual_host and virtual_host_port.
        @param virtual_host         : For a virtual host application, this is the 
                                      hostname where the application will be made 
                                      available.
        @param virtual_host_port    : For a virtual host application, this is the 
                                      port where the application will be made 
                                      available.
        @param hosts                : An array of elements describing where the 
                                      application to be protected resides. This
                                      value is an array of 
                                      ibmsecurity.iag.system.config.Host
        @param app_type             : The connection type to the reverse proxy 
                                      will make to this application. This value
                                      is an ibmsecurity.iag.system.config.AppType
        @param transparent_path     : For path type applications, this will pass 
                                      the entire URL as observed by the reverse 
                                      proxy to the application including the value 
                                      given in "path".
        @param stateful             : When enabled, this will ensure that user 
                                      requests during the lifetime of a session 
                                      are always processed by the same application 
                                      server. 
        @param http2                : Settings specific to HTTP/2. This value is
                                      an ibmsecurity.iag.system.config.HTTP2
        @param identity_headers     : Settings specific to headers containing 
                                      identity data which can be injected by the
                                      reverse proxy. This value is an
                                      ibmsecurity.iag.system.config.IdentityHeaders
        @param cookies              : Settings specific to the handling of cookies.
                                      This value is an ibmsecurity.iag.system.config.Cookies
        @param mutual_auth          : Settings specific to having the reverse
                                      proxy authenticate with the application
                                      servers. This value is an 
                                      ibmsecurity.iag.system.config.MutualAuth
        @param http_transformations : Settings for defining HTTP Transformation
                                      Rules. This value is an 
                                      ibmsecurity.iag.system.config.HttpTransformation
        @param cors                 : Settings specific to Cross Origin Resource
                                      Processing. This value is an array of
                                      ibmsecurity.iag.system.config.CORS
        @param health               : Settings specific to application server
                                      health monitoring. This value is an
                                      ibmsecurity.iag.system.config.Health
        @param rate_limiting        : Settings for defining rate limiting policies.
                                      This value is an array of 
                                      ibmsecurity.iag.system.config.RateLimting
        @param content_injection    : Settings for configuring content injection.
                                      This value is an array of
                                      ibmsecurity.iag.system.config.ContentInjection
        @param worker_threads       : Limits can be set on the percentage of 
                                      worker threads that may be consumed
                                      by this application. This value is an
                                      ibmsecurity.iag.system.config.WorkerThreads
        @param policy               : Authorization policies for this application.
                                      This value is an array of
                                      ibmsecurity.iag.system.config.Policy
        """

        super(ApplicationV1, self).__init__()

        self.path                 = Simple(str, path)
        self.virtual_host         = Simple(str, virtual_host)
        self.virtual_host_port    = Simple(str, virtual_host_port)
        self.hosts                = self._checkList(HostV1, hosts)
        self.app_type             = self._check(AppTypeV1, app_type)
        self.transparent_path     = Simple(bool, transparent_path)
        self.stateful             = Simple(bool, stateful)
        self.http2                = self._check(HTTP2V1, http2)
        self.identity_headers     = self._check(IdentityHeadersV1, identity_headers)
        self.cookies              = self._check(CookiesV1, cookies)
        self.mutual_auth          = self._check(MutualAuthV1, mutual_auth)
        self.http_transformations = self._check(HttpTransformationV1, http_transformations)
        self.cors                 = self._checkList(CorsV1, cors)
        self.health               = self._check(HealthV1, health)
        self.rate_limiting        = self._checkList(RateLimitingV1, rate_limiting)
        self.content_injection    = self._checkList(ContentInjectionV1, content_injection)
        self.worker_threads       = self._check(WorkerThreadsV1, worker_threads)
        self.policy               = self._checkList(PolicyV1, policies)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"


##############################################################################

class AppTypeV1(AutoNumber):
    """
    This class is used to represent an application type. This is the type of
    connection the reverse proxy will make to the application server.
    """

    """
    TCP
    """
    tcp = ()
    """
    SSL (TLS)
    """
    ssl = ()
    """
    TCP Proxy (requires the proxy_host and proxy_port to be defined in each
    host)
    """
    tcp_proxy = ()
    """
    SSL (TLS) Proxy (requires the proxy_host and proxy_port to be defined in 
    each host)
    """
    ssl_proxy = ()

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"

    def getData(self, version):
        """
        Return the data which is managed by this object.
        """

        if (self.version() > version):
            version = self.version()

        return self.name.replace("_", "."), version


##############################################################################

class HostV1(Base):
    """
    This class is used to represent a single application host. A host
    defines where the application being protected resides.
    """

    def __init__(self,
                    host,
                    port,
                    virtual_host                = None,
                    virtual_host_port           = None,
                    proxy_host                  = None,
                    proxy_port                  = None,
                    mutual_ssl_virtual_hostname = None,
                    mutual_ssl_port             = None,
                    ssl                         = None,
                    url_style                   = None):
        """
        Initialise this class instance.  The parameters are as follows:

        @param host                        : The host name or IP address where
                                             the application resides.
        @param port                        : The port which the application 
                                             server is listening on.
        @param virtual_host                : If the application resides on a 
                                             virtual host, this parameter can 
                                             be used to specify the hostname 
                                             which the reverse proxy should 
                                             present in the host header for 
                                             requests to this application.
        @param virtual_host_port           : Port used in conjunction with
                                             virtual_host.
        @param proxy_host                  : For applications with the app_type
                                             tcp_proxy or ssl_proxy, this
                                             entry can be used to specify the
                                             proxy server.
        @param proxy_port                  : Port used in conjunction with
                                             proxy_host.
        @param ssl                         : SSL settings for this application.
                                             This value is an
                                             ibmsecurity.iag.system.config.HostSSL
        @param url_style                   : URL style for this application.
                                             This value is an
                                             ibmsecurity.iag.system.config.HostURLStyle
        """

        super(HostV1, self).__init__()

        self.host                        = Simple(str, host)
        self.port                        = Simple(int, port)
        self.virtual_host                = Simple(str, virtual_host)
        self.virtual_host_port           = Simple(int, virtual_host_port)
        self.proxy_host                  = Simple(str, proxy_host)
        self.proxy_port                  = Simple(int, proxy_port)
        self.mutual_ssl_virtual_hostname = Simple(str, mutual_ssl_virtual_hostname)
        self.mutual_ssl_port             = Simple(int, mutual_ssl_port)
        self.ssl                         = self._check(HostSSLV1, ssl)
        self.url_style                   = self._check(HostURLStyleV1, url_style)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"


##############################################################################

class HostSSLV1(Base):
    """
    This class is used to represent SSL settings for a single application 
    server.
    """

    def __init__(self,
                    certificate = None,
                    server_dn   = None,
                    sni         = None):
        """
        Initialise this class instance.  The parameters are as follows:

        @param certificate : If required, a signer certificate required for 
                             the reverse proxy to trust the application server 
                             can be specified here in PEM format.
        @param server_dn   : This option can be used to ensure that the 
                             application server presents a  specific 
                             certificate.
        @param sni         : If this is a HTTP/2 application, the expected 
                             SNI of the application server can be indicated 
                             here.
        """

        super(HostSSLV1, self).__init__()

        self.certificate = self._check(File, certificate)
        self.server_dn   = Simple(str, server_dn)
        self.sni         = Simple(str, sni)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"


##############################################################################

class HostURLStyleV1(Base):
    """
    This class is used to represent the URL style for a application host.
    """

    def __init__(self,
                    case_insensitive = False,
                    windows          = False):
        """
        Initialise this class instance.  The parameters are as follows:

        @param case_insensitive : Handle URLs as case insensitive
        @param windows          : Handle URLs as case insensitive and forbid 
                                  requests to URLs that appear to be Windows 
                                  style file name aliases.
        """

        super(HostURLStyleV1, self).__init__()

        self.case_insensitive = Simple(bool, case_insensitive)
        self.windows          = Simple(bool, windows)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"


##############################################################################

class HTTP2V1(Base):
    """
    This class is used to represent HTTP/2 settings for an application.
    """

    def __init__(self,
                    enabled = False,
                    sni     = None):
        """
        Initialise this class instance.  The parameters are as follows:

        @param enabled : When enabled, requests will be made by the reverse 
                         proxy to the application server using HTTP/2.
        @param sni     : The Server Name Indicator the reverse proxy will 
                         indicate to the application when communicating using
                         HTTP/2.
        """

        super(HTTP2V1, self).__init__()

        self.enabled = Simple(bool, enabled)
        self.sni     = Simple(str, sni)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"


##############################################################################

class IdentityHeadersV1(Base):
    """
    This class is used to represent the identity headers configuration for
    an application.
    """

    def __init__(self,
                    encoding   = None,
                    basic_auth = None,
                    ip_address = False,
                    cred       = None):
        """
        Initialise this class instance.  The parameters are as follows:

        @param encoding   : The encoding type to use for any identity headers 
                            passed to the application. This value is an
                            ibmsecurity.iag.system.config.IdentityHeadersEncodingType
        @param basic_auth : Controls whether or not basic authentication 
                            headers presented by clients are forwarded to 
                            applications or not. This value is an
                            ibmsecurity.iag.system.config.IdentityHeadersBasicAuthType
        @param ip_address : Provides the client IP address as a HTTP header in 
                            requests forwarded to the application.
        @param cred       : Provides credential data in HTTP headers in 
                            requests forwarded to the application. This value
                            is an ibmsecurity.iag.system.config.IdentityHeadersCredTypeV1
        """

        super(IdentityHeadersV1, self).__init__()

        self.encoding   = self._check(IdentityHeadersEncodingTypeV1, encoding)
        self.basic_auth = self._check(IdentityHeadersBasicAuthTypeV1, basic_auth)
        self.ip_address = Simple(bool, ip_address)
        self.cred       = self._check(IdentityHeadersCredTypeV1, cred)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"


##############################################################################

class IdentityHeadersEncodingTypeV1(AutoNumber):
    """
    This class is used to represent an encoding type for identity headers.
    """

    """
    UTF8 URI (default)
    """
    utf8_uri = ()
    """
    UTF8 Binary
    """
    utf8_bin = ()
    """
    LCP URI
    """
    lcp_uri = ()
    """
    LCP Binary
    """
    lcp_bin = ()

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"

    def getData(self, version):
        """
        Return the data which is managed by this object.
        """

        if (self.version() > version):
            version = self.version()

        return self.name.replace("_", "."), version


##############################################################################

class IdentityHeadersCredTypeV1(AutoNumber):
    """
    This class is used to represent aliases for the available identity 
    headers. This is credential data which the reverse proxy can include
    in request headers to requests forwarded to the application.
    """

    """
    "iv_user"   - The user name of the client (login ID). Defaults to 
                  "Unauthenticated" if client is unauthenticated (unknown).
    """
    iv_user = ()
    """
    "iv_user_l" - The distinguished name (DN) of the client.
    """
    iv_user_l = ()
    """
    "iv_groups" - A list of groups to which the client belongs. Consists of 
                  comma separated quoted entries.
    """
    iv_groups = ()
    """
    "iv_creds"  - Encoded opaque data structure that represents a Security 
                  Access Manager credential. 
    """
    iv_creds = ()
    """
    "all".      - Alias for "iv-user", "iv_groups" and "iv_creds"
    """
    all = ()

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"

    def getData(self, version):
        """
        Return the data which is managed by this object.
        """

        if (self.version() > version):
            version = self.version()

        return self.name.replace("_", "."), version


##############################################################################

class IdentityHeadersBasicAuthTypeV1(AutoNumber):
    """
    This class is used to represent how the application should handle basic
    authentication headers.
    """

    """
    "filter" - The reverse proxy will removes any basic authentication
               information from client requests before sending them to
               the application server.
    """
    filter = ()
    """
    "supply" - The reverse proxy will provide the username and the a dummy
               password to the application server. Use the entry 
               advanced/config/junction/basicauth-dummy-passwd to set the
               dummy password.
    """
    supply = ()
    """
    "ignore" - The reverse proxy will pass any basic authentication headers
               to the application.
    """
    ignore = ()

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"

    def getData(self, version):
        """
        Return the data which is managed by this object.
        """

        if (self.version() > version):
            version = self.version()

        return self.name.replace("_", "."), version


##############################################################################

class CookiesV1(Base):
    """
    This class is used to represent cookie related settings for an application..
    """

    def __init__(self,
                    junction_cookies      = None,
                    forward_client_cookie = False,
                    managed               = None,
                    reset                 = None):
        """
        Initialise this class instance.  The parameters are as follows:

        @param junction_cookie       : The reverse proxy can set a 
                                       "junction cookie" in returned HTML 
                                       pages indicating which junction the 
                                       page was served from. This is useful 
                                       for applications which dynamically 
                                       generate URLs that may not be aware 
                                       or capable of generating URLs 
                                       containing the path which the reverse
                                       proxy served them from. This value is 
                                       an ibmsecurity.iag.system.config.JunctionCookie
        @param forward_client_cookie : This entry will forward the reverse 
                                       proxy cookie (the one named by 
                                       server/session/cookie_name) to the 
                                       application server.
        @param managed               : The reverse proxy can manage cookies 
                                       returned from the application. The 
                                       reverse proxy will store these cookies 
                                       and not return them to the client, but 
                                       will insert them into client requests 
                                       which are forwarded to the application. 
                                       This entry is a list of patterns, 
                                       cookies with names which match any of 
                                       these patterns will be managed by the 
                                       reverse proxy.
        @param reset                 : The reverse proxy can send "clear" 
                                       (empty and expired) cookies to clients 
                                       when their session ends. This can 
                                       effectively remove the cookies from 
                                       some clients. This entry is a list of 
                                       patterns, cookies in a client request 
                                       with names which match any of these 
                                       patterns will be returned as clear 
                                       cookies during a logout.
        """

        super(CookiesV1, self).__init__()

        self.junction_cookie       = self._check(JunctionCookieV1, junction_cookies)
        self.forward_client_cookie = Simple(bool, forward_client_cookie)
        self.managed               = SimpleList(str, managed)
        self.reset                 = SimpleList(str, reset)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"


##############################################################################

class JunctionCookieV1(Base):
    """
    This class is used to represent the junction cookie settings.
    """

    def __init__(self,
                    position      = None,
                    version       = False,
                    ensure_unique = False,
                    preserve_name = False):
        """
        Initialise this class instance.  The parameters are as follows:

        @param position      : Position where the script will be injected.
                               This value is an 
                               ibmsecurity.iag.system.config.JunctionCookiePositionType
        @param version       : Version of the cookie injection script. This 
                               value is an
                               ibmsecurity.iag.system.config.JunctionCookieVersionType
        @param ensure_unique : Inserts the application path or host to ensure 
                               that the cookie is unique.
        @param preserve_name : When the junction cookie is enabled, non-domain 
                               cookies are renamed AMWEBJCT!<path>. Set this 
                               option to true to preserve the original name.
        """

        super(JunctionCookieV1, self).__init__()

        self.position      = self._check(JunctionCookiePositionTypeV1, position)
        self.version       = self._check(JunctionCookieVersionTypeV1, version)
        self.ensure_unique = Simple(bool, ensure_unique)
        self.preserve_name = Simple(bool, preserve_name)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"


##############################################################################

class JunctionCookiePositionTypeV1(AutoNumber):
    """
    This class is used to represent the position of the cookie injection script
    used by junction cookies.
    """

    """
    "inhead"  - injects a <script> block within the document <head>
    """
    inhead = ()
    """
    "trailer" - injects a <script> block of JavaScript at the end of the 
                document
    """
    trailer = ()
    """
    "default" - injects a <script> block before the document
    """
    default = ()

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"

    def getData(self, version):
        """
        Return the data which is managed by this object.
        """

        if (self.version() > version):
            version = self.version()

        return self.name.replace("_", "."), version


##############################################################################

class JunctionCookieVersionTypeV1(AutoNumber):
    """
    This class is used to represent the version of the cookie injection script
    used by junction cookies.
    """

    """
    "onfocus" - injects JavaScript with an onfocus handler.
    """
    onfocus = ()
    """
    "xhtml10" - sets a XHTML1.0 compliant block. (Not compatible with onfocus)
    version: xhtml10
    """
    xhtml = ()

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"

    def getData(self, version):
        """
        Return the data which is managed by this object.
        """

        if (self.version() > version):
            version = self.version()

        return self.name.replace("_", "."), version


##############################################################################

class MutualAuthV1(Base):
    """
    This class is used to represent a mutual authentication used in an
    application definition.
    """

    def __init__(self,
                    basic_auth       = None,
                    certificate_auth = None):
        """
        Initialise this class instance.  The parameters are as follows:

        @param basic_auth       : The reverse proxy can authenticate to the 
                                  application using basic authentication.
                                  This value is an
                                  ibmsecurity.iag.system.config.BasicAuth
        @param certificate_auth : The reverse proxy can authenticate to the 
                                  application using a certificate.
                                  This value is an
                                  ibmsecurity.iag.system.config.CertificateAuth
        """

        super(MutualAuthV1, self).__init__()

        self.basic_auth       = self._check(BasicAuthV1, basic_auth)
        self.certificate_auth = self._check(CertificateAuthV1, certificate_auth)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"


##############################################################################

class BasicAuthV1(Base):
    """
    This class is used to represent basic authentication configuration, used
    in an applications mutual authentication configuration.
    """

    def __init__(self,
                    username,
                    password):
        """
        Initialise this class instance.  The parameters are as follows:

        @param username : The username to use for authentication.
        @param password : The password to use for authentication.
        """

        super(BasicAuthV1, self).__init__()

        self.username = Simple(str, username)
        self.password = Simple(str, password)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"


##############################################################################

class CertificateAuthV1(Base):
    """
    This class is used to represent certificate authentication configuration, 
    used in an applications mutual authentication configuration.    
    """

    def __init__(self,
                    certificate = ""):
        """
        Initialise this class instance.  The parameters are as follows:

        @param certificate : The certificate to present to the application
                             servers for authentication.
        """

        super(CertificateAuthV1, self).__init__()

        self.certificate = self._check(File, certificate)

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
                    name,
                    method,
                    url,
                    rule   = None,
                    action = None):
        """
        Initialise this class instance.  The parameters are as follows:

        @param name   : A name for this policy, which is used to refer to 
                        this policy in audit events.
        @param method : The method(s) which this policy applies to. If this is 
                        not defined, the policy will apply to all methods.
        @param url    : The URL pattern which this policy applies to.
        @param rule   : If a rule string is not defined here, the reverse 
                        proxy will look for a named rule (with the same name 
                        as this policy) in the authorization section of the 
                        configuration YAML.
                        Refer to the authorization section for an explanation 
                        of rule syntax.
        @param action : If the rule matches, should this request be permitted?
                        This value is an 
                        ibmsecurity.iag.system.config.PolicyAction
        """

        super(PolicyV1, self).__init__()

        self.name   = Simple(str, name)
        self.method = SimpleList(str, method)
        self.url    = Simple(str, url)
        self.rule   = Simple(str, rule)
        self.action = self._check(PolicyActionV1, action)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"


##############################################################################

class PolicyActionV1(AutoNumber):
    """
    This class is used to represent an action to be performed by an 
    authorization policy when the policy rule evaluates to true.
    """

    """
    Allow access
    """
    permit = ()
    """
    Deny access
    """
    deny = ()

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"

    def getData(self, version):
        """
        Return the data which is managed by this object.
        """

        if (self.version() > version):
            version = self.version()

        return self.name.replace("_", "."), version


##############################################################################

class HttpTransformationV1(Base):
    """
    This class is used to represent a HTTP transformation rule for an
    application.
    """

    def __init__(self, 
                 request  = None, 
                 response = None):
        """
        Initialise this class instance.  The parameters are as follows:

        @param request  : A list of transformation rules for requests. This
                          value is an array of 
                          ibmsecurity.iag.system.config.HTTPTransformationRule
        @param response : A list of transformation rules for responses. This
                          value is an array of 
                          ibmsecurity.iag.system.config.HTTPTransformationRule
        """

        super(HttpTransformationV1, self).__init__()

        self.request  = self._checkList(HTTPTransformationRuleV1, request)
        self.response = self._checkList(HTTPTransformationRuleV1, response)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"


##############################################################################

class HTTPTransformationRuleV1(Base):
    """
    This class is used to represent a single HTTPTransformationRule definition.
    """

    def __init__(self,
                    name,
                    method,
                    url,
                    rule   = None):
        """
        Initialise this class instance.  The parameters are as follows:

        @param name   : The name of this rule.
        @param method : The HTTP methods which this rule will match.
        @patam url    : The URL pattern which this rule will match.
        @param rule   : The HTTP Transformation Rule XSL document.
        """

        super(HTTPTransformationRuleV1, self).__init__()

        self.name   = Simple(str, name)
        self.method = Simple(str, method)
        self.url    = Simple(str, url)
        self.rule   = self._check(File, rule)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"


##############################################################################

class CorsV1(Base):
    """
    This class is used to represent a CORS policy for an application.
    """

    def __init__(self,
                    name,
                    method,
                    url,
                    policy = None):
        """
        Initialise this class instance.  The parameters are as follows:

        @param name   : The name of this policy.
        @param method : The HTTP methods which this policy will match.
        @patam url    : The URL pattern which this rule will match.
        @param policy : The CORS policy data. This value is an
                        ibmsecurity.iag.system.config.CorsPolicy
        """

        super(CorsV1, self).__init__()

        self.name   = Simple(str, name)
        self.method = Simple(str, method)
        self.url    = Simple(str, url)
        self.policy = self._check(CorsPolicyV1, policy)

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
                    allow_origin      = None,
                    handle_pre_flight = False,
                    allow_header      = None,
                    max_age           = None,
                    allow_method      = None,
                    allow_credentials = False,
                    expose_header     = None):
        """
        Initialise this class instance.  The parameters are as follows:

        @param allow_origins     : An array of origins which will be permitted
                                   to access the application.
        @param handle_pre_flight : A boolean which indicates whether the proxy
                                   will handle pre-flight requests on behalf
                                   of the application.
        @param allow_header      : An array of header names which will be
                                   allowed in cross-origin requests.
        @param max_age           : The number of seconds a client should cache
                                   the results of a pre-flight request.
        @param allow_method      : An array of method names which will be 
                                   allowed in cross-origin requests.
        @param allow_credentials : A boolean which indicates whether
                                   authentication is required when accessing
                                   the application.
        @param expose_header     : An array of header names which the client
                                   may expose after making cross-origin
                                   requests.
        """

        super(CorsPolicyV1, self).__init__()

        self.allow_origin      = SimpleList(str, allow_origin)
        self.handle_pre_flight = Simple(bool, handle_pre_flight)
        self.allow_header      = SimpleList(str, allow_header)
        self.max_age           = Simple(int, max_age)
        self.allow_method      = SimpleList(str, allow_method)
        self.allow_credentials = Simple(bool, allow_credentials)
        self.expose_header     = SimpleList(str, expose_header)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"


##############################################################################

class HealthV1(Base):
    """
    This class is used to represent the health check configuration for an
    application.
    """

    def __init__(self,
                    ping = None,
                    rule = None):
        """
        Initialise this class instance.  The parameters are as follows:

        @param ping : The reverse proxy can periodically ping each application 
                      server to determine whether it is running. This value is
                      an ibmsecurity.iag.system.config.HealthPing
        @param rule : Regular (client initiated) requests can also be observed 
                      to determine the application server health.  This entry 
                      is an ordered list of rules based on the response status 
                      codes. Status codes prefixed with a '+' are considered 
                      healthy, and codes prefixed with '-' unhealthy. The 
                      wildcard characters '*' and '?' can be used.
        """

        super(CorsPolicyV1, self).__init__()

        self.ping = self._check(HealthPingV1, ping)
        self.rule = SimpleList(str, rule)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"


##############################################################################

class HealthPingV1(Base):
    """
    This class is used to represent the ping check configuration for an
    application.
    """

    def __init__(self,
                    method,
                    url,
                    policy = None):

        """
        Initialise this class instance.  The parameters are as follows:

        @param method : Specifies the method which will periodically be pinged.
        @param url    : Specifies the URL which will periodically be pinged.
        @param policy : Specifies the rules about determining health status
                        based on the ping requests. This value is an
                        ibmsecurity.iag.system.config.HealthPingPolicy
        """

        super(HealthPingV1, self).__init__()

        self.method = Simple(str, method)
        self.url    = Simple(str, url)
        self.policy = self._check(HealthPingPolicyV1, policy)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"


#############################################################################

class HealthPingPolicyV1(Base):
    """
    This class is used to define the ping rules for the application ping
    health check.
    """

    def __init__(self,
                    frequency,
                    threshold,
                    recovery  = None,
                    timeout   = None,
                    rule      = None):
        """
        Initialise this class instance.  The parameters are as follows:

        @param frequency : Specifies how often (in seconds) the ping should 
                           be performed.
        @param threshold : Specifies how many consecutive times the ping must 
                           fail before the application server is considered 
                           unhealthy.
        @param recovery  : Specifies the rules for recovery - or when the
                           server can be considered health again after it is
                           determined to be unhealthy. This value is an
                           ibmsecurity.iag.system.config.HealthPingPolicyRecovery
        @param timeout   : Specifies how long the reverse proxy should wait for 
                           responses to ping requests.
        @param rule      : Specifies how to interpret responses to ping 
                           requests. This entry is an ordered list of rules 
                           based on the response status codes. Status codes
                           prefixed with a '+' are considered healthy, and 
                           codes prefixed with '-' unhealthy. The wildcard 
                           characters '*' and '?' can be used.
        """

        super(HealthPingPolicyV1, self).__init__()

        self.frequency = Simple(str, frequency)
        self.threshold = Simple(str, threshold)
        self.recovery  = self._check(HealthPingPolicyRecoveryV1, recovery)
        self.timeout   = Simple(str, timeout)
        self.rule      = SimpleList(str, rule)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"


#############################################################################

class HealthPingPolicyRecoveryV1(Base):
    """
    This class is used to define the ping recovery rules for the application 
    ping health check.    
    """

    def __init__(self,
                    frequency,
                    threshold):
        """
        Initialise this class instance.  The parameters are as follows:

        @param frequency : Specifies how often (in seconds) the ping should 
                           be performed.
        @param threshold : Specifies how many consecutive times the ping must 
                           fail before the application server is considered 
                           unhealthy.
        """

        super(HealthPingPolicyRecoveryV1, self).__init__()

        self.frequency = Simple(str, frequency)
        self.threshold = Simple(str, threshold)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"


##############################################################################

class RateLimitingV1(Base):
    """
    This class is used to represent a single rate limiting policy.
    """

    def __init__(self,
                    name,
                    method,
                    url,
                    rule):
        """
        Initialise this class instance.  The parameters are as follows:

        @param name   : The name of this policy.
        @param method : The HTTP methods which this policy will match.
                        This value is an array.
        @param url    : The URL pattern which this rule will match.
        @param rule   : The rate limiting policy YAML file.
        """

        super(RateLimitingV1, self).__init__()

        self.name   = Simple(str, name)
        self.method = SimpleList(str, method)
        self.url    = Simple(str, url)
        self.rule   = self._check(File, rule)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"


##############################################################################

class ContentInjectionV1(Base):
    """
    This class is used to represent a content injection policy.
    The reverse proxy can inject content into responses. Use these parameters
    to define the content and when injection should take place. Content 
    injection is performed based on the request URL and and a specific location
    within the response.
    """

    def __init__(self,
                    name,
                    url,
                    location,
                    content):
        """
        Initialise this class instance.  The parameters are as follows:

        @param name     : The name of this policy.
        @param url      : The URL pattern which this rule will match.
        @param location : The location where the content should be injected. 
                          The location is pattern matched against a line in 
                          the response using the '*.' wildcard characters.
                          The maximum length of a line which can be matched by 
                          this mechanism is 8192 bytes.
        @param content  : The content (snippet) to inject as a file.
        """

        super(ContentInjectionV1, self).__init__()

        self.name     = Simple(str, name)
        self.url      = Simple(str, url)
        self.location = Simple(str, location)
        self.content  = self._check(File, content)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"


##############################################################################

class WorkerThreadsV1(Base):
    """
    This class is used to define the worker threads configuration for an
    application.
    Limits can be set on the percentage of worker threads that may be consumed
    by this application.
    """

    def __init__(self,
                    soft_limit = None,
                    hard_limit = None):
        """
        Initialise this class instance.  The parameters are as follows:

        @param soft_limit : The soft limit, as an integer. This value is 
                            percentage.
                            This option causes warning messages to be displayed
                            when the application uses more worker threads than 
                            allowed.
        @param hard_limit : The hard limit, as an integer. This value is 
                            percentage.
                            This option causes warning messages to be displayed 
                            when the application uses more worker threads than 
                            allowed and clients are returned the 503 
                            Service Unavailable message.
        """

        super(WorkerThreadsV1, self).__init__()

        self.soft_limit = Simple(int, soft_limit)
        self.hard_limit = Simple(int, hard_limit)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"

##############################################################################
