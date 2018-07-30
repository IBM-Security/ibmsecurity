import logging.config
import pprint
from ibmsecurity.appliance.isamappliance import ISAMAppliance
from ibmsecurity.user.applianceuser import ApplianceUser
from ibmsecurity.user.isamuser import ISAMUser
import pkgutil
import importlib


def import_submodules(package, recursive=True):
    """
    Import all submodules of a module, recursively, including subpackages

    :param package: package (name or actual module)
    :type package: str | module
    :rtype: dict[str, types.ModuleType]
    """
    if isinstance(package, str):
        package = importlib.import_module(package)
    results = {}
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + '.' + name
        results[full_name] = importlib.import_module(full_name)
        if recursive and is_pkg:
            results.update(import_submodules(full_name))
    return results


import ibmsecurity

# Import all packages within ibmsecurity - recursively
# Note: Advisable to replace this code with specific imports for production code
import_submodules(ibmsecurity)

# Setup logging to send to stdout, format and set log level
# logging.getLogger(__name__).addHandler(logging.NullHandler())
logging.basicConfig()
# Valid values are 'DEBUG', 'INFO', 'ERROR', 'CRITICAL'
logLevel = 'DEBUG'
# logLevel = 'CRITICAL'
DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] [PID:%(process)d TID:%(thread)d] [%(levelname)s] [%(name)s] [%(funcName)s():%(lineno)s] %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': logLevel,
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'level': logLevel,
            'handlers': ['default'],
            'propagate': True
        },
        'requests.packages.urllib3.connectionpool': {
            'level': 'ERROR',
            'handlers': ['default'],
            'propagate': True
        }
    }
}
logging.config.dictConfig(DEFAULT_LOGGING)


# Function to pretty print JSON data and in YAML format
def p(jdata):
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(jdata)


#    print(yaml.dump(jdata, allow_unicode=True).decode('utf-8'))


# from ibmsecurity.utilities import tools
# assert tools.version_compare("1", "1") == 0
# assert tools.version_compare("2.1", "2.2") < 0
# assert tools.version_compare("3.0.4.10", "3.0.4.2") > 0
# assert tools.version_compare("4.08", "4.08.01") < 0
# assert tools.version_compare("3.2.1.9.8144", "3.2") > 0
# assert tools.version_compare("3.2", "3.2.1.9.8144") < 0
# assert tools.version_compare("1.2", "2.1") < 0
# assert tools.version_compare("2.1", "1.2") > 0
# assert tools.version_compare("5.6.7", "5.6.7") == 0
# assert tools.version_compare("1.01.1", "1.1.1") == 0
# assert tools.version_compare("1.1.1", "1.01.1") == 0
# assert tools.version_compare("1", "1.0") == 0
# assert tools.version_compare("1.0", "1") == 0
# assert tools.version_compare("1.0", "1.0.1") < 0
# assert tools.version_compare("1.0.1", "1.0") > 0
# assert tools.version_compare("1.0.2.0", "1.0.2") == 0
# assert tools.version_compare("10.0", "9.0.3") > 0
# exit(0)

# Create a user credential for ISAM appliance
u = ApplianceUser(username="admin@local", password="admin")
# u = ApplianceUser(username="admin@local", password="iS32z1rqWJ0L")
# u = ApplianceUser(username="admin@local", password="PLQgkW5Rz7Ky")
# u = ApplianceUser(username="rs379m", password="G6n8uxYv.zd6")
iu = ISAMUser(username="sec_master", password="hJHWsh84pRK8")
# Create an ISAM appliance with above credential
# isam_server = ISAMAppliance(hostname="rldv0175-dev3oac01-app.mt.att.com", user=u, lmi_port=443)
# isam_server = ISAMAppliance(hostname="rldv0178-dev3oa01-app.mt.att.com", user=u, lmi_port=443)
# isam_server = ISAMAppliance(hostname="rldv0177-dev3a01-app.mt.att.com", user=u, lmi_port=443)
# isam_server = ISAMAppliance(hostname="halo-ddr3-sbc01-app.mt.att.com", user=u, lmi_port=443)
# isam_server = ISAMAppliance(hostname="rldv0180-dev3sbc01-app.mt.att.com", user=u, lmi_port=443)
# isam_server = ISAMAppliance(hostname="rldv0176-dev3oaa01-app.mt.att.com", user=u, lmi_port=443)
# isam_server = ISAMAppliance(hostname="rldv0181-dev3ac01-app.mt.att.com", user=u, lmi_port=443)
# isam_server = ISAMAppliance(hostname="alpv1596-agoa01-app.aldc.att.com", user=u, lmi_port=443)
# isam_server = ISAMAppliance(hostname="135.16.104.210", user=u, lmi_port=443)
isam_server = ISAMAppliance(hostname="192.168.198.174", user=u, lmi_port=443)
# isam_server = ISAMAppliance(hostname="localhost", user=u, lmi_port=3333)

# p(ibmsecurity.isam.base.date_time.get_timezones(isam_server))
# p(ibmsecurity.isam.base.runtime.process.execute(isam_server, operation="reload"))
# p(ibmsecurity.isam.web.reverse_proxy.configuration.entry.get(isamAppliance=isam_server, reverseproxy_id='default', stanza_id='rtss-cluster:cluster1',entry_id='basic-auth-passwd'))

# p(ibmsecurity.isam.web.reverse_proxy.configuration.entry.set(isamAppliance=isam_server, reverseproxy_id='default', stanza_id='ssl-qop-mgmt-default',entries=[['default', 'DES-168'], ['default', 'RC2-128 #2'], ['default', 'RC4-128 #3'], ['default', 'AES-128 #4'], ['default', 'AES-256 #5']]))
# p(ibmsecurity.isam.web.reverse_proxy.configuration.entry.update(isamAppliance=isam_server, reverseproxy_id='default', stanza_id='logging',entry_id="request-log-format",value_id="TS:%{%Y-%m-%dT%H:%M:%S}t C:%a I:%A U:%{AZN_CRED_PRINCIPAL_NAME}C AL:%{AUTHENTICATION_LEVEL}C SI:%{tagvalue_session_index}C T:%d M:%m ST:%s B:%B F:%F URL:%U"))
# p(ibmsecurity.isam.web.reverse_proxy.configuration.entry.set(isamAppliance=isam_server, reverseproxy_id='default', stanza_id='logging',entries=[["request-log-format","TS:%{%Y-%m-%dT%H:%M:%S}t C:%a I:%A U:%{AZN_CRED_PRINCIPAL_NAME}C AL:%{AUTHENTICATION_LEVEL}C SI:%{tagvalue_session_index}C T:%d M:%m ST:%s B:%B F:%F URL:%U"]]))
# p(ibmsecurity.isam.web.reverse_proxy.configuration.entry.add(isamAppliance=isam_server, reverseproxy_id='default', stanza_id='interfaces',entries=[['interface1', 'network-interface=2001:1890:1c00:6239::c:46;https-port=443;certificate-label=ctcertoidc01']]))

# p(ibmsecurity.isam.base.management_authentication.set(isam_server,force=False, user_attribute="samAccountName", key_database="ldap_auth.kdb", ldap_port=636, admin_group_dn="CN=AP-ENTERPRISE-APPLIANCE-DEV-ACCESS,OU=Application,OU=Groups,DC=ITServices,DC=sbc,DC=com", anon_bind=False, ldap_host="its-ad-ldap.it.att.com", bind_dn="CN=m04475,OU=Users,OU=CorporateDesktop,OU=Desktop,DC=ITServices,DC=sbc,DC=com", enable_ssl=True, bind_password="iceH0ck3y!", base_dn="DC=ITServices,DC=sbc,DC=com", group_member_attribute="member", cert_label=""))
# p(ibmsecurity.isam.base.management_authentication.set(isam_server,force=False, user_attribute="samAccountName", key_database="ldap_auth.kdb", ldap_port=636, admin_group_dn="CN=AP-ENTERPRISE-APPLIANCE-DEV-ACCESS,OU=Application,OU=Groups,DC=ITServices,DC=sbc,DC=com", anon_bind=True, ldap_host="its-ad-ldap.it.att.com", enable_ssl=True, base_dn="DC=ITServices,DC=sbc,DC=com", group_member_attribute="member", cert_label=""))
# p(ibmsecurity.isam.base.network.static_routes.get_all(isam_server))
# p(ibmsecurity.isam.base.management_authentication.disable(isam_server))
# p(ibmsecurity.isam.base.lmi.restart(isam_server))
# p(ibmsecurity.isam.base.lmi.await_startup(isam_server))
# p(ibmsecurity.isam.web.reverse_proxy.management_root.directory.create(isamAppliance=isam_server, force=False, check_mode=True, instance_id="default", id="junction-root", filename="authtest"))
# p(ibmsecurity.isam.aac.api_protection.grants.delete(isam_server, state_id='uuidd704b10f-0163-10c7-a569-8103ee8a47eb'))
# p(ibmsecurity.isam.aac.api_protection.grants_user.delete(isam_server, 'sa117f'))
# p(ibmsecurity.isam.aac.api_protection.grants_user.get(isam_server, 'rs379m'))
# p(ibmsecurity.isam.aac.api_protection.grants_user.get_recent(isam_server, 'bm155c','2017-11-09T22:30:03Z'))
# p(ibmsecurity.isam.aac.api_protection.grants_user.get_recent(isam_server, 'bm155c','2017-10-10T20:00:00Z', token_type=None))
# p(ibmsecurity.isam.aac.api_protection.grants_user.get(isam_server, 'bm155c','2017-10-10T20:00:00Z'))
# p(ibmsecurity.isam.web.reverse_proxy.junctions.set(isamAppliance=isam_server, reverseproxy_id='default', junction_point='/test', stateful_junction='yes', server_hostname='127.0.0.1', server_port=80, case_sensitive_url='yes', junction_type='tcp', remote_http_header='all', server_uuid='7fc33448-b35d-11e7-88c8-000c29a8faf7'))
# p(ibmsecurity.isam.web.runtime.pdadmin.execute(isamAppliance=isam_server, isamUser=iu, commands=["server task default-webseald-halo-ddr3-a01-app create -t local / -f -l 50 -L 60"]))
# p(ibmsecurity.isam.web.reverse_proxy.junctions.get(isamAppliance=isam_server, reverseproxy_id='default', junctionname='/'))
# p(ibmsecurity.isam.web.reverse_proxy.junctions.get_all(isamAppliance=isam_server, reverseproxy_id='default'))
# p(ibmsecurity.isam.base.lmi.get(isamAppliance=isam_server))
# p(ibmsecurity.isam.base.cluster.node.get_id(isamAppliance=isam_server))
# p(ibmsecurity.isam.base.cluster.node.add(isamAppliance=isam_server, signature_file='/Users/ram/Documents/Work/primary.sign', restricted=True))

# p(ibmsecurity.isam.web.reverse_proxy.interfaces.get_next_http_port(isamAppliance=isam_server, ip_address='172.16.119.131'))
# p(ibmsecurity.isam.web.reverse_proxy.interfaces.get_default(isamAppliance=isam_server))
# p(ibmsecurity.isam.web.reverse_proxy.interfaces.get_ip_addresses(isamAppliance=isam_server))
# p(ibmsecurity.isam.base.ssl_certificates.personal_certificate.set(isamAppliance=isam_server, kdb_id='pdsrv', cert_id='WebSEAL-Test-Only', default='no'))

# p(ibmsecurity.isam.web.runtime.pdadmin.execute(isamAppliance=isam_server, isamUser=iu, commands=["authzrule create at \"<xsl:choose><xsl:when test=\\\"contains(uri, 'pwdmgmt/profile') or contains(uri, 'pwdmgmt/v2/verifyidentity') or contains(uri, 'pwdmgmt/reset/v2/email')\\\">!TRUE!</xsl:when><xsl:otherwise>!FALSE!</xsl:otherwise></xsl:choose>\" -desc \"Rule to allow only password mgmt\"", "authzrule list"]))
# p(ibmsecurity.isam.web.runtime.pdadmin.execute(isamAppliance=isam_server, isamUser=iu, commands=["acl create ramtest", "acl modify ramtest description testing11", "acl modify ramtest set group iv-admin TcmdbsvaBRrl"]))
# p(ibmsecurity.isam.web.runtime.pdadmin.execute(isamAppliance=isam_server, isamUser=iu, commands=["pop modify pt set ipauth add 192.168.199.145 255.255.255.254 forbidden", "pop show pt"]))
# p(ibmsecurity.isam.web.reverse_proxy.logs.delete(isamAppliance=isam_server, instance_id='default', file_id='msg__webseald-default.log.2016-11-10-18-35-24'))
# p(ibmsecurity.isam.web.reverse_proxy.logs.get_all(isamAppliance=isam_server, instance_id='default'))

# p(ibmsecurity.isam.base.admin.set(isam_server, maxFiles=2, sshdPort=22, httpsPort=443))
# p(ibmsecurity.isam.base.admin.get(isam_server))
# p(ibmsecurity.isam.web.reverse_proxy.junctions.set(isamAppliance=isam_server, reverseproxy_id='default', junction_point='/normtest', server_hostname='130.6.51.144', server_port=8080, basic_auth_mode='filter', client_ip_http=None, remote_http_header=["iv_user", "iv_groups"], scripting_support='yes', junction_cookie_javascript_block='trailer'))

# p(ibmsecurity.isam.base.snapshots.get(isam_server))
# p(ibmsecurity.isam.base.snapshots.search(isam_server, comment='Factory'))

# p(ibmsecurity.isam.web.reverse_proxy.instance.get(isamAppliance=isam_server))
# p(ibmsecurity.isam.web.reverse_proxy.junctions.get_all(isamAppliance=isam_server, reverseproxy_id='default'))
# p(ibmsecurity.isam.web.reverse_proxy.junctions.get(isamAppliance=isam_server, reverseproxy_id='default', junctionname='/mga'))
# r = ibmsecurity.isam.web.reverse_proxy.junctions.get(isamAppliance=isam_server, reverseproxy_id='default', junctionname='/mga1')
# p(r['data'])
# p(len(r['data']))
# p(ibmsecurity.isam.web.reverse_proxy.junctions_server.search(isamAppliance=isam_server, reverseproxy_id='default', junction_point='/test',server_hostname='127.0.0.1', server_port=443))


# p(ibmsecurity.isam.base.available_updates.uploaded(isamAppliance=isam_server, file='/Users/ram/Documents/Work/Software/isam_9.0.2.1_20170116-1957.pkg'))
# p(ibmsecurity.isam.base.available_updates._check_file(isamAppliance=isam_server, file='/Users/ram/Documents/Work/Software/isam_9.0.2.1_20170116-1957.pkg'))
# p(ibmsecurity.isam.base.available_updates.install(isamAppliance=isam_server, version='9.0.2.1', release_date='2017-01-16', name='Firmware', type='firmware'))

# p(ibmsecurity.isam.base.fixpack.install(isam_server, '/Users/ram/Documents/Work/Software/eai_allow_empty_headers_9030.fixpack'))

# p(ibmsecurity.isam.aac.authentication.policies.get_all(isamAppliance=isam_server, count=2, filter='description%20contains%20Consent'))
# p(ibmsecurity.isam.aac.authentication.policies.get(isamAppliance=isam_server, name='RSA One-time Password'))
# p(ibmsecurity.isam.aac.authentication.policies.activate(isamAppliance=isam_server, name='RSA One-time Password'))

# p(ibmsecurity.isam.aac.api_protection.definitions.get_all(isamAppliance=isam_server))
# p(ibmsecurity.isam.aac.api_protection.clients.get_all(isamAppliance=isam_server))
# p(ibmsecurity.isam.aac.api_protection.clients.add(isamAppliance=isam_server, definitionName='test', name='scrpttest', companyName='sd',requirePkce=True, jwksUri='https://tested.com'))

# p(ibmsecurity.isam.fed.sts.modules.get_all(isamAppliance=isam_server))
# p(ibmsecurity.isam.fed.sts.modules.get(isamAppliance=isam_server, name='Default Jwt Module'))
# p(ibmsecurity.isam.fed.sts.modules._get(isamAppliance=isam_server, id='com.tivoli.am.fim.trustserver.sts.modules.JwtSTSModule'))
# p(ibmsecurity.isam.fed.sts.modules.search(isamAppliance=isam_server, name='HTTP Map Module to call REST service'))
# p(ibmsecurity.isam.fed.sts.modules.get_types(isamAppliance=isam_server))

# p(ibmsecurity.isam.fed.sts.templates.search(isamAppliance=isam_server, name='issue_jwt'))
# p(ibmsecurity.isam.fed.sts.templates.get(isamAppliance=isam_server, name='issue_jwt'))
# p(ibmsecurity.isam.fed.sts.templates.set(isamAppliance=isam_server, name='issue_jwt', description='test again',chainItems=[{'id': 'default-stsuu', 'mode': 'validate', 'prefix': 'ram123'},{'id': 'default-jwt', 'mode': 'issue', 'prefix': 'ramabc'}]))
# p(ibmsecurity.isam.fed.sts.templates.delete(isamAppliance=isam_server, name='issue_jwt'))
# p(ibmsecurity.isam.fed.sts.templates.get_all(isamAppliance=isam_server))


# p(ibmsecurity.isam.fed.sts.module_chains.get_all(isamAppliance=isam_server))
# p(ibmsecurity.isam.fed.sts.module_chains.search(isamAppliance=isam_server, name='oidc_access_token_chain'))
# p(ibmsecurity.isam.fed.sts.module_chains.get(isamAppliance=isam_server, name='oidc_access_token_chain'))
# p(ibmsecurity.isam.fed.sts.module_chains.set(isamAppliance=isam_server, name='issue_jwt_chain', chainName='issue_jwt', requestType='http://schemas.xmlsoap.org/ws/2005/02/trust/Validate', description=None, tokenType=None, xPath=None, signResponses=False, signatureKey=None, validateRequests=False, validationKey=None, sendValidationConfirmation=False, issuer={ 'address': 'http://issuer/stsuu'}, appliesTo={ 'address': 'http://appliesto/jwt'}, properties={ u'partner': [], u'self': [{u'name': u'FIMConsole.EntGroup.Type', u'value': [u'OTHER']}, {u'name': u'ramabc.nbfOffset', u'value': [u'125']}, {u'name': u'ramabc.iss', u'value': [u'https://op.ccmk.att.com']}, {u'name': u'ramabc.signing.symmetricKey', u'value': [u'5WyDRovii0vqUC1CtRau']}, {u'name': u'ramabc.exp', u'value': [u'7200']}, {u'name': u'ramabc.jtiLength', u'value': [u'0']}, {u'name': u'ramabc.includeIat',
#                                             u'value': [u'true']},
#                                           { u'name': u'ramabc.signing.alg',
#                                             u'value': [u'HS256']}]}))

# p(ibmsecurity.isam.base.update_servers.get_all(isamAppliance=isam_server))
# p(ibmsecurity.isam.base.update_servers.get(isamAppliance=isam_server, name="IBM ISS Default License and Update Server"))
# p(ibmsecurity.isam.base.update_servers.search(isamAppliance=isam_server, name="IBM ISS Default License and Update Server"))
# p(ibmsecurity.isam.base.update_servers.set(isamAppliance=isam_server, priority=2, name="Tester", enabled=False,
#                                            hostName="test.ibm.com", port=443, trustLevel="explicit-trust-ibm-xpu", useProxy=False,
#                                            useProxyAuth=False, cert=None, proxyHost=None, proxyPort=None,
#                                            proxyUser=None, proxyPwd=None, check_mode=False, force=False))
# p(ibmsecurity.isam.base.update_servers.enable(isamAppliance=isam_server, name="Tester", enabled=True))
# p(ibmsecurity.isam.base.update_servers.update(isamAppliance=isam_server, priority=2, name="Tester", enabled=True,
#                                            hostName="test1.ibm.com", port=443, trustLevel="explicit-trust-ibm-xpu", useProxy=True,
#                                            useProxyAuth=True, cert=None, proxyHost="ibm.com", proxyPort=443,
#                                            proxyUser='test', proxyPwd='pwd', check_mode=False, force=False))
# p(ibmsecurity.isam.base.update_servers.delete(isamAppliance=isam_server, name="Tester"))

# p(ibmsecurity.isam.base.scheduled_security_updates.set(isamAppliance=isam_server, enableAutoCheck=False))
# p(ibmsecurity.isam.base.scheduled_security_updates.set(isamAppliance=isam_server, enableAutoCheck=True, dailyFrequencySettings={"interval":"70"}, schedule_type="interval"))
# p(ibmsecurity.isam.base.scheduled_security_updates.get(isamAppliance=isam_server))

# p(ibmsecurity.isam.base.application_database_settings.set(isamAppliance=isam_server, enableAutoUpdate=False, enableIprAutoUpdate=False))
# p(ibmsecurity.isam.base.application_database_settings.set(isamAppliance=isam_server, enableAutoUpdate=True, enableIprAutoUpdate=True, useProxy=True, proxyHost='ibm.com', proxyPort='443', useProxyAuth=True, proxyUser='test', proxyPwd='pwd', enableIprFeedback=False, enableWeblearn=False, includeIprInfo=False))
# p(ibmsecurity.isam.base.application_database_settings.get(isamAppliance=isam_server))

# p(ibmsecurity.isam.base.fips.set(isamAppliance=isam_server,fipsEnabled=True, tlsv10Enabled=False, tlsv11Enabled=False))
# p(ibmsecurity.isam.base.fips.get(isamAppliance=isam_server))

# p(ibmsecurity.isam.web.kerberos_configuration.defaults.get_all(isamAppliance=isam_server))
# p(ibmsecurity.isam.web.kerberos_configuration.defaults.get(isamAppliance=isam_server, name='default_tgs_enctypes'))
# p(ibmsecurity.isam.web.kerberos_configuration.defaults.search(isamAppliance=isam_server, name='default_tgs_enctypes'))
# p(ibmsecurity.isam.web.kerberos_configuration.defaults.add(isamAppliance=isam_server, name='allowweakcrypto', value=False))
# p(ibmsecurity.isam.web.kerberos_configuration.defaults.update(isamAppliance=isam_server, name='default_tgs_enctypes', value='rc4-hmac des-cbc-md5 des-cbc-crc aes256-cts'))
# p(ibmsecurity.isam.web.kerberos_configuration.defaults.delete(isamAppliance=isam_server, name='allowweakcrypto'))

# p(ibmsecurity.isam.web.kerberos_configuration.realms.get_all(isamAppliance=isam_server))

# p(ibmsecurity.isam.aac.runtime_template.root.export_file(isamAppliance=isam_server, filename='/Users/ram/Downloads/extract.zip'))
# p(ibmsecurity.isam.aac.runtime_template.root.import_file(isamAppliance=isam_server, filename='/Users/ram/Downloads/extract.zip'))

# p(ibmsecurity.isam.base.network.test_connection.connect(isamAppliance=isam_server, server="rldv0178-dev3oa01-app.mt.att.com", port=443, ssl=False, timeout=4))
# p(ibmsecurity.isam.base.network.interfaces.search(isamAppliance=isam_server, label="1.1"))
# p(ibmsecurity.isam.base.network.interfaces.get_all(isamAppliance=isam_server))
# p(ibmsecurity.isam.base.network.interfaces_ipv4.search(isamAppliance=isam_server, address="192.168.194.200"))
# p(ibmsecurity.isam.base.network.interfaces_ipv4.search(isamAppliance=isam_server, address="127.0.0.1"))

# p(ibmsecurity.isam.web.rsa_securid_config.get(isamAppliance=isam_server))
# p(ibmsecurity.isam.web.rsa_securid_config.upload(isamAppliance=isam_server, filename="/Users/ram/Downloads/sdconf.rec"))
# p(ibmsecurity.isam.web.rsa_securid_config.delete(isamAppliance=isam_server))
# p(ibmsecurity.isam.web.rsa_securid_config.test(isamAppliance=isam_server, username='abc', passcode='123456'))

# p(ibmsecurity.isam.base.cli.execute(isamAppliance=isam_server, command='isam/aac/config',
#                                     input=["\n", "1", "192.168.198.164",
#                                            "443", "admin", "admin", "y", "1", "192.168.198.164", "443", "admin",
#                                            "admin", "y", "1", "1", "sec_master", "passw0rd", "Default", "1", "localhost", "443",
#                                            "2", "easuser", "passw0rd", "y", "y", "1", "1", "1", "2", "3", "1", "y",
#                                            "1", "1"]))
# PLQgkW5Rz7Ky (admin)
# hJHWsh84pRK8 (sec_master)
# lkdTz6CNw7CK
# dEtVQKfcPny7 (cn=root)

# rldv0181.mt.att.com:lmi> reset_lmi_cert
# Enter 'YES' to confirm: YES

# p(ibmsecurity.isam.web.reverse_proxy.junctions_server.add(isamAppliance=isam_server, reverseproxy_id='default', junction_point='/cspapi', server_hostname='site1-api3-junc.csp.sbc.com', server_port=6050, case_sensitive_url='yes', windows_style_url='yes', junction_type='tcp', query_contents='/pd/query_contents.exe', virtual_hostname='site1-api3-junc.csp.sbc.com:6050', stateful_junction='no'))
# p(ibmsecurity.isam.web.reverse_proxy.junctions_server.add(isamAppliance=isam_server, reverseproxy_id='default', junction_point='/cspapi', server_hostname='site1-api4-junc.csp.att.com', server_port=6050, case_sensitive_url='yes', windows_style_url='yes', junction_type='tcp', query_contents='/pd/query_contents.exe', virtual_hostname='site1-api4-junc.csp.att.com:6050', stateful_junction='no'))

# p(ibmsecurity.isam.base.license.install(isamAppliance=isam_server, license='/Users/ram/Downloads/389799_21769420_1170.isslicense'))

# p(ibmsecurity.isam.aac.access_control.policy_attachments.authenticate(isamAppliance=isam_server, username='sec_master', password='hJHWsh84pRK8'))
# p(ibmsecurity.isam.aac.access_control.policy_attachments.get_resources(isamAppliance=isam_server))
# p(ibmsecurity.isam.aac.access_control.policy_attachments.get_all(isamAppliance=isam_server))
# p(ibmsecurity.isam.aac.access_control.policy_attachments.get(isamAppliance=isam_server, server="enterprise", resourceUri='/isam/oidc/endpoint/amapp-runtime-AttFpForSuperusers/authorize'))
# p(ibmsecurity.isam.aac.access_control.policy_attachments.update(isamAppliance=isam_server, server="enterprise", resourceUri='/isam/oidc/endpoint/amapp-runtime-AttFpForSuperusers/authorize', cache=-1, policyCombiningAlgorithm="denyOverrides"))

# p(ibmsecurity.isam.base.network.interfaces_vlan.update(isamAppliance=isam_server, label='1.1', vlanId=None, name='SVC/APP', comment='Intranet Facing - SVC / Application Interface - APP', enabled=True, check_mode=True))
# r = ibmsecurity.isam.web.reverse_proxy.logs.get_all(isamAppliance=isam_server, instance_id='default')
# p(r)
# rl = 0
# ml = 0
# for f in r['data']:
#     if f['id'].startswith('request.log'):
#         rl += f['file_size']
#     if f['id'].startswith('msg__webseald-default.log'):
#         ml += f['file_size']
# print ("request.log: "+str(rl))
# print ("message.log: "+str(ml))

# p(ibmsecurity.isam.web.reverse_proxy.common_configurations.get_all(isamAppliance=isam_server, reverseproxy_id='default'))
# p(ibmsecurity.isam.web.reverse_proxy.common_configurations.get(isamAppliance=isam_server, reverseproxy_id='default', configuration_id='auth-timeout1'))

# p(ibmsecurity.isam.base.ssl_certificates.signer_certificate.import_cert(isamAppliance=isam_server, kdb_id='pdsrv', label='Symantec Class 3 Secure Server CA - G4', cert='/Users/ram/Downloads/Symantec Class 3 Secure Server CA - G4.cer'))

# r = ibmsecurity.isam.fed.federations.get_all(isamAppliance=isam_server)
# for fed in r['data']:
#     partnr = ibmsecurity.isam.fed.partners.get_all(isamAppliance=isam_server, federation_name=fed['name'])
#     for pr in partnr['data']:
#         print("Federaion: {0} Partner: {1} ClientID: {2}".format(fed['name'], pr['name'], pr['configuration']['clientId']))

# p(ibmsecurity.isam.appliance.rollback(isamAppliance=isam_server))

# p(ibmsecurity.isam.aac.advanced_configuration.get_all(isamAppliance=isam_server))

# p(ibmsecurity.isam.base.runtime.tuning_parameters.get(isamAppliance=isam_server))
# p(ibmsecurity.isam.base.runtime.tuning_parameters.set(isamAppliance=isam_server, option='max_heap_size', value="4096", check_mode=True))
# p(ibmsecurity.isam.base.runtime.tuning_parameters.reset(isamAppliance=isam_server, option='enable_sso'))

# p(ibmsecurity.isam.base.runtime.listening_interfaces.get(isamAppliance=isam_server))
# p(ibmsecurity.isam.base.runtime.listening_interfaces.set(isamAppliance=isam_server, interface='local-interface', port=80, secure=False))
# p(ibmsecurity.isam.base.runtime.listening_interfaces.delete(isamAppliance=isam_server, interface='local-interface', port=80, check_mode=True))

# p(ibmsecurity.isam.web.kerberos_configuration.defaults.get_all(isamAppliance=isam_server))
# p(ibmsecurity.isam.web.kerberos_configuration.defaults.get(isamAppliance=isam_server, name='default_realm'))
# p(ibmsecurity.isam.web.kerberos_configuration.defaults.search(isamAppliance=isam_server, name='ramtest'))
# p(ibmsecurity.isam.web.kerberos_configuration.defaults.add(isamAppliance=isam_server, name='ramtest', value='test'))
# p(ibmsecurity.isam.web.kerberos_configuration.defaults.update(isamAppliance=isam_server, name='ramtest', value='tested'))
# p(ibmsecurity.isam.web.kerberos_configuration.defaults.delete(isamAppliance=isam_server, name='ramtest'))

# p(ibmsecurity.isam.web.kerberos_configuration.realms.get_all(isamAppliance=isam_server))
# p(ibmsecurity.isam.web.kerberos_configuration.realms.get(isamAppliance=isam_server, realm='test'))
# p(ibmsecurity.isam.web.kerberos_configuration.realms.add(isamAppliance=isam_server, realm='ramtest'))
# p(ibmsecurity.isam.web.kerberos_configuration.realms.delete(isamAppliance=isam_server, realm='ramtest'))
# p(ibmsecurity.isam.web.kerberos_configuration.realms.search(isamAppliance=isam_server, realm='ramtest'))

# p(ibmsecurity.isam.web.kerberos_configuration.domains.get_all(isamAppliance=isam_server))
# p(ibmsecurity.isam.web.kerberos_configuration.domains.get(isamAppliance=isam_server, name='1.1.1.1'))
# p(ibmsecurity.isam.web.kerberos_configuration.domains.search(isamAppliance=isam_server, name='1.1.1.1'))
# p(ibmsecurity.isam.web.kerberos_configuration.domains.add(isamAppliance=isam_server, name='1.1.2.2', value='test'))
# p(ibmsecurity.isam.web.kerberos_configuration.domains.update(isamAppliance=isam_server, name='1.1.2.2', value='test1'))
# p(ibmsecurity.isam.web.kerberos_configuration.domains.delete(isamAppliance=isam_server, name='1.1.2.2'))

# p(ibmsecurity.isam.web.kerberos_configuration.ca_paths.get_all(isamAppliance=isam_server))
# p(ibmsecurity.isam.web.kerberos_configuration.ca_paths.get(isamAppliance=isam_server, name='testy'))
# p(ibmsecurity.isam.web.kerberos_configuration.ca_paths.search(isamAppliance=isam_server, name='testy'))
# p(ibmsecurity.isam.web.kerberos_configuration.ca_paths.add(isamAppliance=isam_server, name='testy1'))
# p(ibmsecurity.isam.web.kerberos_configuration.ca_paths.delete(isamAppliance=isam_server, name='testy1'))

# p(ibmsecurity.isam.web.runtime.configuration.entry.add(isamAppliance=isam_server, resource_id='ivmgrd.conf', stanza_id='aznapi-configuration', entries=[['test', 'a b']]))
# p(ibmsecurity.isam.web.runtime.configuration.entry.delete(isamAppliance=isam_server, resource_id='ivmgrd.conf', stanza_id='aznapi-configuration', entry_id='test', value_id=''))
# p(ibmsecurity.isam.web.runtime.configuration.entry.get(isamAppliance=isam_server, resource_id='ivmgrd.conf', stanza_id='aznapi-configuration', entry_id='test'))
# p(ibmsecurity.isam.web.runtime.configuration.entry.delete_all(isamAppliance=isam_server, resource_id='ivmgrd.conf', stanza_id='aznapi-configuration', entry_id='test'))

# p(ibmsecurity.isam.web.reverse_proxy.configuration.entry.add(isamAppliance=isam_server, reverseproxy_id='default', stanza_id='aznapi-configuration', entries=[['test', 'a b']]))
# p(ibmsecurity.isam.web.reverse_proxy.configuration.entry.delete(isamAppliance=isam_server, reverseproxy_id='default', stanza_id='aznapi-configuration', entry_id='test', value_id='a b'))
# p(ibmsecurity.isam.web.reverse_proxy.configuration.entry.delete_all(isamAppliance=isam_server, reverseproxy_id='default', stanza_id='aznapi-configuration', entry_id='test'))

# p(ibmsecurity.isam.web.kerberos_configuration.keyfiles.get(isamAppliance=isam_server))
# p(ibmsecurity.isam.web.kerberos_configuration.keyfiles.import_keytab(isamAppliance=isam_server, id='username.keytab', file='/Users/ram/Downloads/username.keytab'))
# p(ibmsecurity.isam.web.kerberos_configuration.keyfiles.import_keytab(isamAppliance=isam_server, id='ram.keytab', file='/Users/ram/Downloads/ram.keytab'))
# p(ibmsecurity.isam.web.kerberos_configuration.keyfiles.delete(isamAppliance=isam_server, id='test'))
# p(ibmsecurity.isam.web.kerberos_configuration.keyfiles.combine(isamAppliance=isam_server, newname='test.keytab', keytab_files=['ram.keytab', 'username.keytab']))

# p(ibmsecurity.isam.base.cluster.configuration.get(isamAppliance=isam_server))

# p(ibmsecurity.isam.statistics.get_rp_throughput_summary(isamAppliance=isam_server, summary=False, date=1519070400, duration=86400, aspect='junction'))
# p(ibmsecurity.isam.statistics.get_rp_traffic_summary(isamAppliance=isam_server, instance='default', summary=True, date=1519070400, duration=86400, aspect='junction'))
# p(ibmsecurity.isam.statistics.get_rp_traffic_summary(isamAppliance=isam_server, instance='default', summary=None, date=1519070400, duration=86400, aspect='junction'))
# p(ibmsecurity.isam.statistics.get_network(isamAppliance=isam_server, application_interface='1.1', statistics_duration='5d'))
# p(ibmsecurity.isam.statistics.get_cpu(isamAppliance=isam_server, statistics_duration='5d'))
# p(ibmsecurity.isam.statistics.get_memory(isamAppliance=isam_server, statistics_duration='5d'))
# p(ibmsecurity.isam.statistics.get_storage(isamAppliance=isam_server, statistics_duration='5d'))


# r = ibmsecurity.isam.application_logs.get_all(isamAppliance=isam_server, file_path='access_control/runtime', recursive='no', flat_details='yes')
# p(r)
# for a in r['data']['contents']:
#     if 'children' in a:
#         continue
#     if 'javacore' in a['name']:
#         print ("access_control/runtime/{0}".format(a['name']))
# p(ibmsecurity.isam.application_logs.delete(isamAppliance=isam_server, file_id='/access_control/runtime/javacore.20180226.164852.1812.0003.txt'))
# p(ibmsecurity.isam.application_logs.get(isamAppliance=isam_server, file_path='access_control/runtime/javacore.20180227.192932.1804.0099.txt', length=1, start=1))
# p(ibmsecurity.isam.application_logs.export_file(isamAppliance=isam_server, file_path='access_control/runtime/console.log', filename='/Users/ram/Downloads/console.test.log'))

# p(ibmsecurity.isam.base.advanced_tuning_parameters.get(isamAppliance=isam_server))
# p(ibmsecurity.isam.base.advanced_tuning_parameters.set(isamAppliance=isam_server, key='abc', value=[789, 123, 456]))
# p(ibmsecurity.isam.base.advanced_tuning_parameters.delete(isamAppliance=isam_server, key='abc'))

# p(ibmsecurity.isam.base.remote_syslog.forwarder.get_all(isamAppliance=isam_server))
# p(ibmsecurity.isam.base.remote_syslog.forwarder.get(isamAppliance=isam_server, server='test.qradar.com', port=443, protocol='udp'))
# p(ibmsecurity.isam.base.remote_syslog.forwarder.delete(isamAppliance=isam_server, server='test.qradar.com', port=443, protocol='udp'))
# p(ibmsecurity.isam.base.remote_syslog.forwarder.set(isamAppliance=isam_server, server='test.qradar.com', port=443, protocol='udp'))
# p(ibmsecurity.isam.base.remote_syslog.forwarder.set(isamAppliance=isam_server, server='testagain.qradar.com', port=443, protocol='udp'))
# p(ibmsecurity.isam.base.remote_syslog.forwarder.delete(isamAppliance=isam_server, server='testagain.qradar.com', port=443, protocol='udp'))

# p(ibmsecurity.isam.base.remote_syslog.forwarder_sources.get_all(isamAppliance=isam_server, server='test.qradar.com', port=443, protocol='udp'))
# p(ibmsecurity.isam.base.remote_syslog.forwarder_sources.get(isamAppliance=isam_server, server='test.qradar.com', port=443, protocol='udp', name='WebSEAL:default:msg__webseald-default.log'))
# p(ibmsecurity.isam.base.remote_syslog.forwarder_sources.delete(isamAppliance=isam_server, server='test.qradar.com', port=443, protocol='udp', name='WebSEAL:default:request.log'))
# p(ibmsecurity.isam.base.remote_syslog.forwarder_sources.set(isamAppliance=isam_server, server='test.qradar.com', port=443, protocol='udp', name='LMI Messages', severity='debug', facility='syslog', tag='request log'))

# p(ibmsecurity.isam.base.remote_syslog.facility.get(isamAppliance=isam_server))
# p(ibmsecurity.isam.base.remote_syslog.instance_logs.get(isamAppliance=isam_server, source_name='webseal', instance_name='default'))
# p(ibmsecurity.isam.base.remote_syslog.instances.get(isamAppliance=isam_server, source_name='webseal'))
# p(ibmsecurity.isam.base.remote_syslog.severity.get(isamAppliance=isam_server))
# p(ibmsecurity.isam.base.remote_syslog.sources.get(isamAppliance=isam_server))

# p(ibmsecurity.isam.aac.access_policy.get_all(isamAppliance=isam_server))
# p(ibmsecurity.isam.aac.access_policy.get(isamAppliance=isam_server, name='test'))
# p(ibmsecurity.isam.aac.access_policy.add(isamAppliance=isam_server, name='test', content='/* test */'))
# p(ibmsecurity.isam.aac.access_policy.export_file(isamAppliance=isam_server, name='test', filename='/Users/ram/Downloads/test-access-policy.js'))
# p(ibmsecurity.isam.aac.access_policy.update(isamAppliance=isam_server, name='test', content='/* test 123 */'))
# p(ibmsecurity.isam.aac.access_policy.delete(isamAppliance=isam_server, name='test'))
# p(ibmsecurity.isam.aac.access_policy.upload(isamAppliance=isam_server, name='test', file='/Users/ram/Downloads/test-access-policy.js'))
# p(ibmsecurity.isam.aac.access_policy.import_file(isamAppliance=isam_server, name='test', file='/Users/ram/Downloads/test-access-policy.js'))
# p(ibmsecurity.isam.aac.access_policy.set(isamAppliance=isam_server, name='test1', content='/* test 123 */'))
# p(ibmsecurity.isam.aac.access_policy.compare(isamAppliance1=isam_server, isamAppliance2=isam_server))

# p(ibmsecurity.isam.base.geolocation_db.get(isamAppliance=isam_server))
# p(ibmsecurity.isam.base.geolocation_db.cancel(isamAppliance=isam_server))
# p(ibmsecurity.isam.base.geolocation_db.upload(isamAppliance=isam_server, file='/Users/ram/Downloads/GeoLiteCityv6.csv.zip'))

# p(ibmsecurity.isam.aac.mapping_rules.get_all(isamAppliance=isam_server))
