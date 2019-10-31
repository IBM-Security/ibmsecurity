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
                    failover       = None):
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
        """

        super(ServerV1, self).__init__()

        self.ssl            = self._check(SSLV1, ssl)
        self.session        = self._check(SessionV1, session)
        self.worker_threads = Simple(int, worker_threads)
        self.http2          = Simple(bool, http2)
        self.websocket      = self._check(WebSocketV1, websocket)
        self.apps           = self._check(AppsV1, apps)
        self.failover       = self._check(FailoverV1, failover)

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
                    ciphers         = None):
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
        @param key         : An ibmsecurity.iag.system.config.File object
                             which contains the key which is used to protect
                             the JWE.
        """

        super(FailoverV1, self).__init__()

        self.cookie_name = Simple(str, cookie_name)
        self.key         = self._check(File, key)

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
            "application": {
                "read"  : Simple(int, app_read_timeout),
                "write" : Simple(int, app_write_timeout)
            },
            "client": {
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
                 cred_viewer = None):
        """
        Initialise this class instance.  The parameters are as follows:

        @param cred_viewer : The credential viewer application. Defining this
                             parameter will enable the credential viewer app.
                             This value is an 
                             ibmsecurity.iag.system.config.CredViewerApp
                             object.
        """

        super(AppsV1, self).__init__()

        self.cred_viewer = self._check(CredViewerAppV1, cred_viewer)

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
                 path="creds"):
        """
        Initialise this class instance.  The parameters are as follows:

        @param path : The path at which the credential viewer application 
                      will be made available.
        """

        super(CredViewerAppV1, self).__init__()

        self.path = Simple(str, path)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """

        return "19.12"

##############################################################################
