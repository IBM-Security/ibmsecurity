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

from enum import Enum

from ibmsecurity.iag.system.config.base import Base
from ibmsecurity.iag.system.config.base import Simple
from ibmsecurity.iag.system.config.base import AutoNumber
from ibmsecurity.iag.system.config.file import File

##############################################################################

class ServerV1(Base):
    """
    This class is used to represent the front-end configuration of an IAG
    container.
    """

    def __init__(self,
                    ssl            = None,
                    session        = None,
                    worker_threads = 100,
                    http2          = True,
                    websocket      = None,
                    apps           = None,
                    failover       = None,
                    local_pages    = None,
                    mgmt_pages     = None,
                    error_pages    = None):
        """
        Initialise this class instance.  The parameters are as follows:

        @param ssl            : An ibmsecurity.iag.system.config.SSL object 
                                which is used to define the SSL configuration 
                                of the IAG.
        @param session        : An ibmsecurity.iag.system.config.Session object
                                which is used to define the configuration of the
                                session cache which is used by the IAG.
        @param worker_threads : The number of worker threads which will be used
                                by the IAG.
        @param http2          : A boolean which is used to indicate whether
                                HTTP2 support is enabled or not.
        @param websocket      : An ibmsecurity.iag.system.config.WebSocket 
                                object which is used to configure the Web Socket
                                support of the IAG.
        @param apps           : An array of ibmsecurity.iag.system.config.App
                                objects which are used to define which local
                                applications are enabled.
        @param failover       : An ibmsecurity.iag.system.config.Failover
                                object which contains configuration
                                information for failover support
                                between multiple IAG containers.
        @param local_pages    : An ibmsecurity.iag.system.config.LocalPagesV1
                                object which contains configuration information
                                for pages served by the local junction.
        @param mgmt_pages     : An array of 
                                ibmsecurity.iag.system.config.MgmtPagesV1
                                objects which contains configuration 
                                information for management pages.
        @param error_pages     : An array of 
                                ibmsecurity.iag.system.config.ErrorPagesV1
                                objects which contains configuration 
                                information for error pages.
        """

        super(ServerV1, self).__init__()

        self.ssl                = self._check(SSLV1, ssl)
        self.session            = self._check(SessionV1, session)
        self.worker_threads     = Simple(int, worker_threads)
        self.http2              = Simple(bool, http2)
        self.websocket          = self._check(WebSocketV1, websocket)
        self.local_applications = self._check(AppsV1, apps)
        self.failover           = self._check(FailoverV1, failover)
        self.local_pages        = self._check(LocalPagesV1, local_pages)
        self.management_pages   = self._checkList(MgmtPagesV1, mgmt_pages)
        self.error_pages        = self._checkList(ErrorPagesV1, error_pages)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"

##############################################################################

class SSLV1(Base):
    """
    This class is used to represent the SSL configuration of the IAG container.
    """

    def __init__(self,
                    front_end     = None,
                    applications  = None):
        """
        Initialise this class instance.  The parameters are as follows:

        @param front_end          : SSL configuration for the front-end.
        @param applications       : SSL configuration for the applications.

        """

        super(SSLV1, self).__init__()

        self.front_end            = self._check(SSLFrontEndV1, front_end)
        self.applications         = self._check(SSLApplicationsV1, applications)


    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"

##############################################################################

class SSLFrontEndV1(Base):
    """
    This class is used to represent the SSL configuration of the IAG container
    front-end.
    """

    def __init__(self,
                    certificate     = None,
                    tlsv10          = False,
                    tlsv11          = False,
                    tlsv12          = True,
                    tlsv13          = True,
                    fips_processing = False,
                    nist_compliance = False,
                    ciphers         = None,
                    sni             = None):
        """
        Initialise this class instance.  The parameters are as follows:

        @param certificate     : An ibmsecurity.iag.system.config.file object
                                 which points to the file which will be used
                                 as the server certificate.
        @param tlsv10          : Should TLS v1.0 be enabled?
        @param tlsv11          : Should TLS v1.1 be enabled?
        @param tlsv12          : Should TLS v1.2 be enabled?
        @param tlsv13          : Should TLS v1.3 be enabled?
        @param fips_processing : Should FIPS be enabled?
        @param nist_compliance : Should the ciphers be NIST compliant?
        @param ciphers         : An array of 
                                 ibmsecurity.iag.system.config.ssl_cipher 
                                 objects used to represent the ciphers which 
                                 will be enabled.
        @param sni             : An array of 
                                 ibmsecurity.iag.system.config.SSLFrontEndSNIV1
                                 objects used to represent the SNI 
                                 configuration for the server.
        """

        super(SSLFrontEndV1, self).__init__()

        self.certificate     = self._check(File, certificate)
        self.tlsv10          = Simple(bool, tlsv10)
        self.tlsv11          = Simple(bool, tlsv11)
        self.tlsv12          = Simple(bool, tlsv12)
        self.tlsv13          = Simple(bool, tlsv13)
        self.fips_processing = Simple(bool, fips_processing)
        self.nist_compliance = Simple(bool, nist_compliance)
        self.ciphers         = self._checkList(SSLCipherV1, ciphers)
        self.sni             = self._checkList(SSLFrontEndSNIV1, sni)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"

##############################################################################

class SSLFrontEndSNIV1(Base):
    """
    This class is used to represent the SNI SSL configuration of the IAG 
    container front-end.
    """

    def __init__(self,
                    certificate,
                    hostname):
        """
        Initialise this class instance.  The parameters are as follows:

        @param certificate : An ibmsecurity.iag.system.config.file object
                             which points to the file which will be used
                             as the SNI server certificate.
        @param hostname    : The hostname to be associated with the 
                             certificate.
        """

        super(SSLFrontEndSNIV1, self).__init__()

        self.certificate = self._check(File, certificate)
        self.hostname    = Simple(str, hostname)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"

##############################################################################

class SSLCipherV1(AutoNumber):
    """
    This class is used to represent a single SSL cipher.
    """

    SSL_RSA_FIPS_WITH_3DES_EDE_CBC_SHA = ()
    SSL_RSA_FIPS_WITH_DES_CBC_SHA = ()
    TLS_DHE_PSK_WITH_AES_128_CCM_8 = ()
    TLS_DHE_PSK_WITH_AES_128_CCM = ()
    TLS_DHE_PSK_WITH_AES_256_CCM_8 = ()
    TLS_DHE_PSK_WITH_AES_256_CCM = ()
    TLS_DHE_RSA_WITH_AES_128_CCM_8 = ()
    TLS_DHE_RSA_WITH_AES_128_CCM = ()
    TLS_DHE_RSA_WITH_AES_128_GCM_SHA256 = ()
    TLS_DHE_RSA_WITH_AES_256_CCM_8 = ()
    TLS_DHE_RSA_WITH_AES_256_CCM = ()
    TLS_DHE_RSA_WITH_AES_256_GCM_SHA384 = ()
    TLS_ECDHE_ECDSA_WITH_3DES_EDE_CBC_SHA = ()
    TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256 = ()
    TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA = ()
    TLS_ECDHE_ECDSA_WITH_AES_128_CCM_8 = ()
    TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256 = ()
    TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384 = ()
    TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA = ()
    TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384 = ()
    TLS_ECDHE_ECDSA_WITH_RC4_128_SHA = ()
    TLS_ECDHE_RSA_WITH_3DES_EDE_CBC_SHA = ()
    TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256 = ()
    TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA = ()
    TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 = ()
    TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384 = ()
    TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA = ()
    TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 = ()
    TLS_ECDHE_RSA_WITH_RC4_128_SHA = ()
    TLS_PSK_WITH_AES_128_CCM_8 = ()
    TLS_PSK_WITH_AES_128_CCM = ()
    TLS_PSK_WITH_AES_256_CCM_8 = ()
    TLS_PSK_WITH_AES_256_CCM = ()
    TLS_RSA_EXPORT1024_WITH_DES_CBC_SHA = ()
    TLS_RSA_EXPORT1024_WITH_RC4_56_SHA = ()
    TLS_RSA_EXPORT_WITH_RC2_CBC_40_MD5 = ()
    TLS_RSA_EXPORT_WITH_RC4_40_MD5 = ()
    TLS_RSA_WITH_3DES_EDE_CBC_SHA = ()
    TLS_RSA_WITH_AES_128_CBC_SHA256 = ()
    TLS_RSA_WITH_AES_128_CBC_SHA = ()
    TLS_RSA_WITH_AES_128_CCM_8 = ()
    TLS_RSA_WITH_AES_128_CCM = ()
    TLS_RSA_WITH_AES_128_GCM_SHA256 = ()
    TLS_RSA_WITH_AES_256_CBC_SHA256 = ()
    TLS_RSA_WITH_AES_256_CBC_SHA = ()
    TLS_RSA_WITH_AES_256_CCM_8 = ()
    TLS_RSA_WITH_AES_256_CCM = ()
    TLS_RSA_WITH_AES_256_GCM_SHA384 = ()
    TLS_RSA_WITH_DES_CBC_SHA = ()
    TLS_RSA_WITH_NULL_MD5 = ()
    TLS_RSA_WITH_NULL_NULL = ()
    TLS_RSA_WITH_NULL_SHA = ()
    TLS_RSA_WITH_RC4_128_MD5 = ()
    TLS_RSA_WITH_RC4_128_SHA = ()
    TLS_RSA_WITH_NULL_SHA256 = ()
    SSL_CK_RC4_128_WITH_MD5 = ()
    SSL_CK_RC4_128_EXPORT40_WITH_MD5 = ()
    SSL_CK_RC2_128_CBC_WITH_MD5 = ()
    SSL_CK_RC2_128_CBC_EXPORT40_WITH_MD5 = ()
    SSL_CK_DES_64_CBC_WITH_MD5 = ()
    SSL_CK_DES_192_EDE3_CBC_WITH_MD5 = ()
    TLS_ECDHE_ECDSA_WITH_NULL_SHA = ()
    TLS_ECDHE_RSA_WITH_NULL_SHA = ()
    TLS_AES_128_GCM_SHA256 = ()
    TLS_AES_256_GCM_SHA384 = ()
    TLS_CHACHA20_POLY1305_SHA256 = ()
    TLS_AES_128_CCM_SHA256 = ()
    TLS_AES_128_CCM_8_SHA256 = ()

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

        return self.name, version

##############################################################################

class SSLApplicationsV1(Base):
    """
    This class is used to represent the SSL configuration for applications.
    """

    def __init__(self,
                    tlsv10          = False,
                    tlsv11          = False,
                    tlsv12          = True,
                    tlsv13          = True,
                    fips_processing = True,
                    nist_compliance = True):
        """
        Initialise this class instance.  The parameters are as follows:

        @param tlsv10          : Should TLS v1.0 be enabled?
        @param tlsv11          : Should TLS v1.1 be enabled?
        @param tlsv12          : Should TLS v1.2 be enabled?
        @param tlsv13          : Should TLS v1.3 be enabled?
        @param fips_processing : Should FIPS be enabled?
        @param nist_compliance : Should the ciphers be NIST compliant?
        """

        super(SSLApplicationsV1, self).__init__()

        self.tlsv10          = Simple(bool, tlsv10)
        self.tlsv11          = Simple(bool, tlsv11)
        self.tlsv12          = Simple(bool, tlsv12)
        self.tlsv13          = Simple(bool, tlsv13)
        self.fips_processing = Simple(bool, fips_processing)
        self.nist_compliance = Simple(bool, nist_compliance)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"

##############################################################################

class SessionV1(Base):
    """
    This class is used to represent the session configuration of the IAG 
    container.
    """

    def __init__(self,
                    cookie_name      = "IAG_Session",
                    max_sessions     = 4096,
                    timeout          = 3600,
                    inactive_timeout = 600):
        """
        Initialise this class instance.  The parameters are as follows:

        @param cookie_name      : The name of the cookie which will house the
                                  session identifier.
        @param max_sessions     : The maximum number of sessions to be stored
                                  in the session cache.
        @param timeout          : The maximum lifetime of a session in the 
                                  session cache.
        @param inactive_timeout : The maximum length of inactivity for a session
                                  in the session cache.
        """

        super(SessionV1, self).__init__()

        self.cookie_name      = Simple(str, cookie_name)
        self.max_sessions     = Simple(int, max_sessions)
        self.timeout          = Simple(int, timeout)
        self.inactive_timeout = Simple(int, inactive_timeout)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"

##############################################################################

class FailoverV1(Base):
    """
    This class is used to represent the failover configuration of the IAG
    container.
    """

    def __init__(self,
                    cookie_name = "IAG_JWE",
                    key         = None):
        """
        Initialise this class instance.  The parameters are as follows:

        @param cookie_name : The name of the cookie which will house the
                             failover JWE token.
        @param key         : The key value which is used to protect the JWE.
                             The key should be 64 bytes in length.  If it is
                             more than 64 bytes it will be truncated, and if 
                             it is less than 64 bytes it will be right
                             padded with 0's.
        """

        super(FailoverV1, self).__init__()

        self.cookie_name = Simple(str, cookie_name)
        self.key         = Simple(str, key)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"

##############################################################################

class WebSocketV1(Base):
    """
    This class is used to represent the Web Socket configuration of the IAG 
    container.
    """

    def __init__(self,
                    max_worker_threads   = 50,
                    idle_worker_threads  = 0,
                    app_read_timeout     = 120,
                    app_write_timeout    = 20,
                    client_read_timeout  = 120,
                    client_write_timeout = 20):
        """
        Initialise this class instance.  The parameters are as follows:

        @param max_worker_threads:   The number of worker threads to allocate
                                     to the container.
        @param idle_worker_threads:  The minimum number of worker threads to keep
                                     allocated when idle.
        @param app_read_timeout:     The maximum length of time spent trying
                                     to read from an application.
        @param app_write_timeout:    The maximum length of time spent trying
                                     to write to an application.
        @param client_read_timeout:  The maximum length of time spent trying
                                     to read from a client.
        @param client_write_timeout: The maximum length of time spent trying
                                     to write to a client.
        """

        super(WebSocketV1, self).__init__()

        self.worker_threads = {
            "max" : Simple(int, max_worker_threads),
            "idle": Simple(int, idle_worker_threads)
        }

        self.timeouts = {
            "applications": {
                "read"  : Simple(int, app_read_timeout),
                "write" : Simple(int, app_write_timeout)
            },
            "front_end": {
                "read"  : Simple(int, client_read_timeout),
                "write" : Simple(int, client_write_timeout)
            }
        }

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"

##############################################################################

class AppsV1(Base):
    """
    This class is used to represent the local applications which can be
    enabled within the IAG container.
    """

    def __init__(self,
                 cred_viewer  = None,
                 azn_decision = None):
        """
        Initialise this class instance.  The parameters are as follows:

        @param cred_viewer  : Used to enable the credential viewer application. 
                              This value is an 
                              ibmsecurity.iag.system.config.CredViewerApp
                              object.
        @param azn_decision : Used to enabled the authorization decision 
                              application. This value is an 
                              ibmsecurity.iag.system.config.CredViewerApp
                              object.
        """

        super(AppsV1, self).__init__()

        self.cred_viewer  = self._check(CredViewerAppV1, cred_viewer)
        self.azn_decision = self._check(AznDecisionAppV1, azn_decision)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """

        return "19.12"

##############################################################################

class CredViewerAppV1(Base):
    """
    This class is used to represent the credential viewer local application
    which can be enabled within the IAG container.
    """

    def __init__(self,
                 path        = "creds",
                 enable_html = True):
        """
        Initialise this class instance.  The parameters are as follows:

        @param path        : The path at which the credential viewer 
                             application will be made available.
        @param enable_html : Enables an embedded HTML page which can
                             render the JSON in a browser.
        """

        super(CredViewerAppV1, self).__init__()

        self.path        = Simple(str, path)
        self.enable_html = Simple(bool, enable_html)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """

        return "19.12"

##############################################################################

class AznDecisionAppV1(Base):
    """
    This class is used to represent the authorization decision local 
    application which can be enabled within the IAG container.
    """

    def __init__(self,
                 path               = "azn",
                 max_cache_size     = 8192,
                 max_cache_lifetime = 300):
        """
        Initialise this class instance.  The parameters are as follows:

        @param path               : The path at which the authorization 
                                    decision application will be made 
                                    available.
        @param max_cache_size     : The maximum number of credentials which 
                                    can be cached.  If the addition of a new 
                                    credential will exceed this maximum cache 
                                    size a least-recently-used algorithm will
                                    be used to remove an older entry, making 
                                    room for the new credential.
        @param max_cache_lifetime : The maximum lifetime, in seconds, of an 
                                    entry in the cache.
        """

        super(AznDecisionAppV1, self).__init__()

        self.path               = Simple(str, path)
        self.max_cache_size     = Simple(int, max_cache_size)
        self.max_cache_lifetime = Simple(int, max_cache_lifetime)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """

        return "19.12"

##############################################################################

class LocalPagesV1(Base):
    """
    This class is used to represent the local pages which are served by the
    IAG container.
    """

    def __init__(self,
                 content):
        """
        Initialise this class instance.  The parameters are as follows:

        @param content : An array of 
                         ibmsecurity.iag.system.config.LocalContentV1 objects.
        """

        super(LocalPagesV1, self).__init__()

        self.content = self._checkList(LocalContentV1, content)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """

        return "19.12"

##############################################################################

class LocalContentV1(Base):
    """
    This class is used to represent the local pages which are served by the
    IAG container.
    """

    def __init__(self,
                 name,
                 content):
        """
        Initialise this class instance.  The parameters are as follows:

        @param name    : The name of the file, including any path information.
        @param content : An ibmsecurity.iag.system.config.file object
                         which points to the file content.
        """

        super(LocalContentV1, self).__init__()

        self.name    = Simple(str, name)
        self.content = self._check(File, content)

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

        data    = {}
        current = data

        # Find the correct node to add the data to.
        for dir in self.name.value_.split('/')[:-1]:
            current[dir] = []
            newData      = {}

            current[dir].append(newData)

            current = newData

        # Add the data to the node.
        current[self.name.value_.split('/')[-1:][0]] = self.content.value

        return data, version

##############################################################################

class MgmtPagesV1(Base):
    """
    This class is used to represent the management pages which are served by 
    the IAG container.
    """

    def __init__(self,
                 language,
                 content):
        """
        Initialise this class instance.  The parameters are as follows:

        @param language : The language for the supplied content.
        @param content  : An array of 
                          ibmsecurity.iag.system.config.MgmtContentV1
                          objects which contain configuration information
                          for pages served by the local junction.
        """

        super(MgmtPagesV1, self).__init__()

        self.language = Simple(str, language)
        self.content  = self._checkList(MgmtContentV1, content)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """

        return "19.12"

##############################################################################

class MgmtContentV1(Base):
    """
    This class is used to represent the management pages which are served by 
    the IAG container.
    """

    def __init__(self,
                 page_type,
                 pages):
        """
        Initialise this class instance.  The parameters are as follows:

        @param page_type : An ibmsecurity.iag.system.config.MgmtContentTypeV1
                           object which represents the page type.
        @param pages     : An array of 
                           ibmsecurity.iag.system.config.ResponsePageV1
                           objects which contain information related to a
                           single management page.
        """

        super(MgmtContentV1, self).__init__()

        self.page_type = self._check(MgmtContentTypeV1, page_type)
        self.pages     = self._checkList(ResponsePageV1, pages)

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

        data = {}

        data['page_type'], lversion = self.page_type.getData(version)

        if (lversion > version):
            version = lversion

        for page in self.pages:
            data[page.mime_type.value_], lversion = page.getData(version)

            if (lversion > version):
                version = lversion

        return data, version

##############################################################################

class MgmtContentTypeV1(AutoNumber):
    """
    This class is used to represent a single management page type.
    """

    default             = ()
    help                = ()
    login_success       = ()
    logout              = ()
    oidc_fragment       = ()
    ratelimit           = ()
    redirect            = ()
    temp_cache_response = ()

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

        return self.name, version

##############################################################################

class ErrorPagesV1(Base):
    """
    This class is used to represent the error pages which are served by 
    the IAG container.
    """

    def __init__(self,
                 language,
                 content):
        """
        Initialise this class instance.  The parameters are as follows:

        @param language : The language for the supplied content.
        @param content  : An array of 
                          ibmsecurity.iag.system.config.ErrorContentV1
                          objects which contain configuration information
                          for error pages served by the server.
        """

        super(ErrorPagesV1, self).__init__()

        self.language = Simple(str, language)
        self.content  = self._checkList(ErrorContentV1, content)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """

        return "19.12"

##############################################################################

class ErrorContentV1(Base):
    """
    This class is used to represent the error pages which are served by 
    the IAG container.
    """

    def __init__(self,
                 error_code,
                 pages):
        """
        Initialise this class instance.  The parameters are as follows:

        @param error_code : The hexidecimal error code for the supplied pages.
                            A special error page of 'default' can be used to
                            indicate the default error page.
        @param pages      : An array of 
                            ibmsecurity.iag.system.config.ResponsePageV1
                            objects which contain information related to a
                            single error page.
        """

        super(ErrorContentV1, self).__init__()

        self.error = Simple(str, error_code)
        self.pages = self._checkList(ResponsePageV1, pages)

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

        data = {}

        data['error'] = self.error.value_

        for page in self.pages:
            data[page.mime_type.value_], lversion = page.getData(version)

            if (lversion > version):
                version = lversion

        return data, version

##############################################################################

class ResponsePageV1(Base):
    """
    This class is used to represent a single management page.
    """

    def __init__(self,
                 mime_type,
                 content,
                 response_code = None):
        """
        Initialise this class instance.  The parameters are as follows:

        @param mime_type     : The mime type for which this page will be 
                               returned: e.g. json
        @param content       : An ibmsecurity.iag.system.config.file object
                               which points to the file content.
        @param response_code : The response code which will be returned with
                               the page.
        """

        super(ResponsePageV1, self).__init__()

        self.mime_type     = Simple(str, mime_type)
        self.content       = self._check(File, content)
        self.response_code = Simple(int, response_code)

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

        data = {}

        data['content'] = self.content.value

        if self.response_code.value_ is not None:
            data['response_code'] = self.response_code.value_

        return data, version

##############################################################################

