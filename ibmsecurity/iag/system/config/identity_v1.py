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
from ibmsecurity.iag.system.config.base import SimpleList
from ibmsecurity.iag.system.config.file import File
from ibmsecurity.iag.system.config.base import AutoNumber

##############################################################################

class IdentityV1(Base):
    """
    This class is used to represent the identity configuration of an IAG
    container.  The identity configuration defines the authentication
    mechanism which is used by the IAG container.
    """

    def __init__(self,
                    config = None):
        """
        Initialise this class instance.  The parameters are as follows:

        @param config : One of the support identity configuration objects.
        """

        super(IdentityV1, self).__init__()

        setattr(self, config.name(), 
                self._check([ 
                        OidcCiIdentityV1, 
                        OidcIdentityV1, 
                        OAuthIdentityV1 
                    ], config))

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"

##############################################################################

class OidcRspTypesV1(AutoNumber):
    """
    This enumeration contains a list of all the supported response types.
    """

    code            = ()
    id_token        = ()
    id_token__token = ()

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"

##############################################################################

class OidcRspModesV1(AutoNumber):
    """
    This enumeration contains a list of all the supported response modes.
    """

    query     = ()
    fragment  = ()
    form_post = ()

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"

##############################################################################

class OAuthMethodTypeV1(AutoNumber):
    """
    This enumeration contains a list of all the supported authentication
    methods for OAuth.
    """

    client_secret_post  = ()
    client_secret_basic = ()

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"

##############################################################################

class IdentityRuleV1(Base):
    """
    This class is used to represent a rule.  A rule consists of a boolean
    value to indicate inclusion/exclusion and a string value.
    """

    def __init__(self,
                    include,
                    value):
        """
        Initialise this class instance.  The paramaters are as follows"

        @param include : A boolean value which is used to indicate whether
                         the value should be included or excluded.
        @param value   : The value itself, as a string.
        """

        super(IdentityRuleV1, self).__init__()

        self.include = self._check(bool, include)
        self.value   = self._check(str, value)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"

    def getData(self, version):
        """
        Return the data which is managed by this object.  
        """

        return "{0}{1}".format("+" if self.include else "-", self.value), \
                    version

##############################################################################

class OidcCiIdentityV1(Base):
    """
    This class is used to represent the configuration when OIDC authentication
    against Cloud Identity is required.
    """

    def __init__(self,
                    tenant,
                    client_id,
                    client_secret,
                    redirect_uri_host  = None,
                    response_type      = OidcRspTypesV1.code,
                    response_mode      = None,
                    proxy              = None,
                    scopes             = None,
                    allowed_query_args = None,
                    bearer_token_attrs = [IdentityRuleV1(False, "id_token")],
                    id_token_attrs     = None,
                    mapped_identity    = "{preferred_username}"):
        """
        Initialise this class instance.  The parameters are as follows:

        @param tenant             : The name of the CI tenant.
        @param client_id          : The client identifier.
        @param client_secret      : The client secret.
        @param redirect_uri_host  : The host which is used in the redirect
                                    URI registered with the OP.
        @param response_type      : An OidcRspTypes object which indicates the
                                    the required response type for 
                                    authentication responses.
        @param response_mode      : An OidcRspModes object which indicates the 
                                    required response mode for
                                    authentication responsees.
        @param proxy              : The proxy, if any, which is used to
                                    communicate with the OP.
        @param scopes             : An array of scopes to be sent in the
                                    authentication request.
        @param allowed_query_args : An array of query string arguments which
                                    can be provided to the authentication
                                    kick off URL.
        @param bearer_token_attrs : An array of IdentityRuleV1 objects which 
                                    govern whether a claim from the bearer 
                                    token is added to the credential.
        @param id_token_attrs     : An array of IdentityRuleV1 objects which 
                                    govern whether a claim from the identity 
                                    token is added to the credential.
        @param mapped_identity    : A formatted string which is used to
                                    construct the IAG principal name.
        """

        super(OidcCiIdentityV1, self).__init__()

        self.tenant             = Simple(str, tenant)
        self.client_id          = Simple(str, client_id)
        self.client_secret      = Simple(str, client_secret)
        self.redirect_uri_host  = Simple(str, redirect_uri_host)
        self.response_type      = self._check(OidcRspTypesV1, response_type)
        self.response_mode      = self._check(OidcRspModesV1, response_mode)
        self.proxy              = Simple(str, proxy)
        self.scopes             = SimpleList(str, scopes)
        self.allowed_query_args = SimpleList(str, allowed_query_args)
        self.bearer_token_attrs = self._checkList(IdentityRuleV1, bearer_token_attrs)
        self.id_token_attrs     = self._checkList(IdentityRuleV1, id_token_attrs)
        self.mapped_identity    = Simple(str, mapped_identity)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"

    def name(self):
        """
        Return the name of this identity type.
        """
        return "ci_oidc"

##############################################################################

class OidcIdentityV1(Base):
    """
    This class is used to represent the configuration when OIDC authentication
    against a generic OIDC OP is required.
    """

    def __init__(self,
                    certificate,
                    discovery_endpoint,
                    client_id,
                    client_secret,
                    redirect_uri_host  = None,
                    response_type      = OidcRspTypesV1.id_token__token,
                    response_mode      = OidcRspModesV1.form_post,
                    proxy              = None,
                    scopes             = [ "profile", "email" ],
                    allowed_query_args = None,
                    bearer_token_attrs = None,
                    id_token_attrs     = None,
                    mapped_identity    = "{iss}/{sub}"):
        """
        Initialise this class instance.  The parameters are as follows:

        @param certificate        : An ibmsecurity.iag.system.config.file 
                                    oject which points to the file which 
                                    contains the CA certificate of the OP.
        @param discovery_endpoint : The discovery endpoint of the OP.
        @param client_id          : The client identifier.
        @param client_secret      : The client secret.
        @param redirect_uri_host  : The host which is used in the redirect
                                    URI registered with the OP.
        @param response_type      : An OidcRspTypes object which indicates the
                                    the required response type for 
                                    authentication responses.
        @param response_mode      : An OidcRspModes object which indicates the 
                                    required response mode for
                                    authentication responsees.
        @param proxy              : The proxy, if any, which is used to
                                    communicate with the OP.
        @param scopes             : An array of scopes to be sent in the
                                    authentication request.
        @param allowed_query_args : An array of query string arguments which
                                    can be provided to the authentication
                                    kick off URL.
        @param bearer_token_attrs : An array of IdentityRuleV1 objects which 
                                    govern whether a claim from the bearer 
                                    token is added to the credential.
        @param id_token_attrs     : An array of IdentityRuleV1 objects which 
                                    govern whether a claim from the identity 
                                    token is added to the credential.
        @param mapped_identity    : A formatted string which is used to
                                    construct the IAG principal name.
        """

        super(OidcIdentityV1, self).__init__()

        self.certificate        = self._check(File, certificate)
        self.discovery_endpoint = Simple(str, discovery_endpoint)
        self.client_id          = Simple(str, client_id)
        self.client_secret      = Simple(str, client_secret)
        self.redirect_uri_host  = Simple(str, redirect_uri_host)
        self.response_type      = self._check(OidcRspTypesV1, response_type)
        self.response_mode      = self._check(OidcRspModesV1, response_mode)
        self.proxy              = Simple(str, proxy)
        self.scopes             = SimpleList(str, scopes)
        self.allowed_query_args = SimpleList(str, allowed_query_args)
        self.bearer_token_attrs = self._checkList(IdentityRuleV1, bearer_token_attrs)
        self.id_token_attrs     = self._checkList(IdentityRuleV1, id_token_attrs)
        self.mapped_identity    = Simple(str, mapped_identity)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"

    def name(self):
        """
        Return the name of this identity type.
        """
        return "oidc"

##############################################################################

class OAuthIdentityV1(Base):
    """
    This class is used to represent the configuration when OAuth introspection
    is required.
    """

    def __init__(self,
                    certificate,
                    introspection_endpoint,
                    proxy              = None,
                    client_id          = None,
                    client_id_hdr      = None,
                    client_secret      = None,
                    token_type_hint    = "access_token",
                    mapped_identity    = "{username}",
                    response_attrs     = None,
                    method             = None,
                    multivalue_scope   = True):
        """
        Initialise this class instance.  The parameters are as follows:

        @param certificate            : An ibmsecurity.iag.system.config.file 
                                        oject which points to the file which 
                                        contains the CA certificate of the 
                                        server.
        @param introspection_endpoint : The introspection endpoint of the
                                        server.
        @param proxy                  : The proxy, if any, which is used to
                                        communicate with the server .
        @param client_id              : The client identifier.
        @param client_id_hdr          : The name of the HTTP header which
                                        contains the client identity.
        @param client_secret          : The client secret.
        @param token_type_hint        : A hint about the type of token
                                        submitted for introspection.
        @param mapped_identity        : A formatted string which is used to
                                        construct the IAG principal name.
        @param response_attrs         : An array of IdentityRuleV1 objects 
                                        which govern which response attributes
                                        are added to the generated credential.
        @param method                 : An OAuthMethodType object which 
                                        indicates the introspection type to be
                                        used.
        @param multivalue_scope       : A boolean which is used to indicate
                                        whether the OAuth scope attributes are
                                        provided as a single space separated
                                        string or not.
        """

        super(OAuthIdentityV1, self).__init__()

        self.certificate            = self._check(File, certificate)
        self.introspection_endpoint = Simple(str, introspection_endpoint)
        self.proxy                  = Simple(str, proxy)
        self.client_id              = Simple(str, client_id)
        self.client_id_hdr          = Simple(str, client_id_hdr)
        self.client_secret          = Simple(str, client_secret)
        self.token_type_hint        = Simple(str, token_type_hint)
        self.mapped_identity        = Simple(str, mapped_identity)
        self.response_attrs         = self._checkList(IdentityRuleV1, response_attrs)
        self.method                 = self._check(OAuthMethodTypeV1, method)
        self.multivalue_scope       = Simple(bool, multivalue_scope)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"

    def name(self):
        """
        Return the name of this identity type.
        """
        return "oauth"

##############################################################################


