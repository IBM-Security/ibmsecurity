import logging

import ibmsecurity.isam.base.ssl_certificates.signer_certificate
import ibmsecurity.isam.appliance
import pytest

def getTestData():
    testdata = [
        {
            "kdb_id": "pdsrv",
            "label": "github.io",
            "cert": """-----BEGIN CERTIFICATE-----
MIIGhTCCBW2gAwIBAgIRAJB3NEFHMW75lZl2eur98bkwDQYJKoZIhvcNAQELBQAw
gY8xCzAJBgNVBAYTAkdCMRswGQYDVQQIExJHcmVhdGVyIE1hbmNoZXN0ZXIxEDAO
BgNVBAcTB1NhbGZvcmQxGDAWBgNVBAoTD1NlY3RpZ28gTGltaXRlZDE3MDUGA1UE
AxMuU2VjdGlnbyBSU0EgRG9tYWluIFZhbGlkYXRpb24gU2VjdXJlIFNlcnZlciBD
QTAeFw0yNTAzMDcwMDAwMDBaFw0yNjAzMDcyMzU5NTlaMBYxFDASBgNVBAMMCyou
Z2l0aHViLmlvMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAxKQLElVm
JYKnZ9dmKMWrb4fy4BWFm658EQemS4hJgrt+1NFpL2tGVaFupVyV3vmKorCX3zej
c7+gH8Ugpemmj9r5tk1NZ0SXXALTjvT2i03oSqjwCzkn+R1o0TYg+G7PyQ5pE18A
E+K3VUcpch1f5RyBTEvE4+HUg4/6OpAIYFVznJ3yk8a+bo1i/HBp2MbtPzssSlT8
mPLY76SETtKdwgIdY91MkTiJd1x0KJDM2GPKM7pNTc81NMSw6WBzsxg4PFbR+BCY
82/sYu8iMy/AdYcUz72hh2DGXnVypzzV/LLgJ/VAP5m+md0lVH5KIG/cduDrajlo
LQ4LKJktO4VmwQIDAQABo4IDUjCCA04wHwYDVR0jBBgwFoAUjYxexFStiuF36Zv5
mwXhuAGNYeEwHQYDVR0OBBYEFBLwftAxb+SvNbWJ+0LZ7bcLk80EMA4GA1UdDwEB
/wQEAwIFoDAMBgNVHRMBAf8EAjAAMB0GA1UdJQQWMBQGCCsGAQUFBwMBBggrBgEF
BQcDAjBJBgNVHSAEQjBAMDQGCysGAQQBsjEBAgIHMCUwIwYIKwYBBQUHAgEWF2h0
dHBzOi8vc2VjdGlnby5jb20vQ1BTMAgGBmeBDAECATCBhAYIKwYBBQUHAQEEeDB2
ME8GCCsGAQUFBzAChkNodHRwOi8vY3J0LnNlY3RpZ28uY29tL1NlY3RpZ29SU0FE
b21haW5WYWxpZGF0aW9uU2VjdXJlU2VydmVyQ0EuY3J0MCMGCCsGAQUFBzABhhdo
dHRwOi8vb2NzcC5zZWN0aWdvLmNvbTCCAX4GCisGAQQB1nkCBAIEggFuBIIBagFo
AHYAlpdkv1VYl633Q4doNwhCd+nwOtX2pPM2bkakPw/KqcYAAAGVbeysdQAABAMA
RzBFAiEA+YIgsAqb2cqQVlF4JP2ERIVCH3RXdB7DjIPc6Ch5aK4CIHjqUoV7F5Mk
fcIQcmdn7Z5UR8nYtPA2OLvYc3mCFcLuAHcAGYbUxyiqb/66A294Kk0BkarOLXIx
D67OXXBBLSVMx9QAAAGVbeysDgAABAMASDBGAiEAjryAbXlHsXj/v4f7CWXJzDUX
SUuvA5kRH3doh4WPUQcCIQC+nojCqhCn/ZupbnI50O1T3FSKBQu/LOZ33fApzLJW
hQB1AMs49xWJfIShRF9bwd37yW7ymlnNRwppBYWwyxTDFFjnAAABlW3srDcAAAQD
AEYwRAIgS98L1D2W8nzV3tIQ0R4UJWxwxb7I/TT6e9ly0nA0QsACIFpl7s/WA1Qm
z1Vm8ZtihoNFubO/AiiaVGaeDQiznHFCMHsGA1UdEQR0MHKCCyouZ2l0aHViLmlv
ggwqLmdpdGh1Yi5jb22CFyouZ2l0aHVidXNlcmNvbnRlbnQuY29tggpnaXRodWIu
Y29tgglnaXRodWIuaW+CFWdpdGh1YnVzZXJjb250ZW50LmNvbYIOd3d3LmdpdGh1
Yi5jb20wDQYJKoZIhvcNAQELBQADggEBAHksjTVCptW9CtbBXu+7J2cDDmKRz/EA
kUyONuojOnKoI3d2f5DQDkqzu/gSj6B28YO3a4EYFktvwq3KnXAu9KzSM1ehlhtA
lxlvjjGUgXvux7DjnBH40ItKiE723opeWVbm2WExdRPSckm/CDwshz2U3Sl3M3Wt
v0xPuZJrg1tMIL58RqrS5PpFlAIIlEUC6dr+xVQrwLNcYXVVgvZsRSX/YbrzboLM
gWhuDSQPcaeDGHcy7NxRZHmlpHz+/Ot067VuxjGqm9veKNGZMUdroS+ocxAJBXv3
Z1NCCowvpZazNxKccQg7izYwd6HL70WMxCWFU0e70uw9KZqteG7SVcQ=
-----END CERTIFICATE-----
""",
            "preserve_label": "true"
        },
        {
            "kdb_id": "pdsrv",
            "label": "github.io",
            "cert": "test/scripts/github.io.txt",
            "preserve_label": "true"
        },
        {
            "kdb_id": "pdsrv",
            "label": "IBM Internal Root CA",
            "cert": """-----BEGIN CERTIFICATE-----
MIID5TCCAs2gAwIBAgIBFDANBgkqhkiG9w0BAQsFADBiMQswCQYDVQQGEwJVUzE0MDIGA1UEChMrSW50ZXJuYXRpb25hbCBCdXNpbmVzcyBNYWNoaW5lcyBDb3Jwb3JhdGlvbjEdMBsGA1UEAxMUSUJNIEludGVybmFsIFJvb3QgQ0EwHhcNMTYwMjI0MDUwMDAwWhcNMzUwMTAzMDQ1OTU5WjBiMQswCQYDVQQGEwJVUzE0MDIGA1UEChMrSW50ZXJuYXRpb25hbCBCdXNpbmVzcyBNYWNoaW5lcyBDb3Jwb3JhdGlvbjEdMBsGA1UEAxMUSUJNIEludGVybmFsIFJvb3QgQ0EwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDUKGuk9Tmri43R3SauS7gY9rQ9DXvRwklnbW+3Ts8/Meb4MPPxezdEcqVJtHVc3kinDpzVMeKJXlB8CABBpxMBSLApmIQywEKoVd0H0w62Yc3rYuhv03iYy6OozBV0BL6tzZE0UbvtLGuAQXMZ7ehzxqIta85JjfFN86AO2u7xrNF0FYyGH+E0Rn6yNhb25VrqxE0OYbSMIGoWdvS11K4SgVDqrJ9OqIk8NHrIJ8Ed24P/YPMeAp3jU409Gev1zGcuLdRr09WckQ145FZVDbPq42gcl7qYICPhZ4/eDUUjFgxpipfMGkMb1X+Y3kFDgb4BO8Xrdda2VQo1iDZs8A8bAgMBAAGjgaUwgaIwPwYJYIZIAYb4QgENBDIWMEdlbmVyYXRlZCBieSB0aGUgU2VjdXJpdHkgU2VydmVyIGZvciB6L09TIChSQUNGKTAOBgNVHQ8BAf8EBAMCAQYwDwYDVR0TAQH/BAUwAwEB/zAdBgNVHQ4EFgQU+d4Y5Z4wE2lRp/15hUiMfA5v2OMwHwYDVR0jBBgwFoAU+d4Y5Z4wE2lRp/15hUiMfA5v2OMwDQYJKoZIhvcNAQELBQADggEBAH87Ms8yFyAb9nXesaKjTHksLi1VKe2izESWozYFXnRtOgOW7/0xXcfK+7PW6xwcOqvTk61fqTGxj+iRyZf2e3FNtIB+T/Lg3SZF9sztPM0jEUELWycC8l6WPTvzQjZZBCsF+cWbU1nxvRNQluzCsTDUEIfThJIFcLu0WkoQclUrC3d2tM8jclLPssb6/OV8GaJ+4mx4ri7HbGaUAOtA/TXKR6AuhgkRNPKYhpPU0q/PRlGXdwJP8zXb8+CXMMTnI5Upur7Tc5T3I/x1Gqfz7n1sTRZfsuiQJ5uua4hz4te3oV2tm7LWcNItHD43zttBTTx/m5icg71JE2gcr2oincw=
-----END CERTIFICATE-----
    """,
            "preserve_label": "true"
        },
        {
            "kdb_id": "pdsrv",
            "label": "IBM INTERNAL INTERMEDIATE CA",
            "cert": """-----BEGIN CERTIFICATE-----
MIIFCjCCA/KgAwIBAgIBGTANBgkqhkiG9w0BAQsFADBiMQswCQYDVQQGEwJVUzE0MDIGA1UEChMrSW50ZXJuYXRpb25hbCBCdXNpbmVzcyBNYWNoaW5lcyBDb3Jwb3JhdGlvbjEdMBsGA1UEAxMUSUJNIEludGVybmFsIFJvb3QgQ0EwHhcNMjIwNTA2MDQwMDAwWhcNMzUwMTAxMDQ1OTU5WjBqMQswCQYDVQQGEwJVUzE0MDIGA1UEChMrSW50ZXJuYXRpb25hbCBCdXNpbmVzcyBNYWNoaW5lcyBDb3Jwb3JhdGlvbjElMCMGA1UEAxMcSUJNIElOVEVSTkFMIElOVEVSTUVESUFURSBDQTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALaMp8hDDYrxsHGc6j5/K2HKS/1peh2Hek1RKlR1NhP/9MPEu3/I63oEyelpN6kJb7Xru73mLe9DGEkopjUlf5bkCClJ2u8LpWNpVvpxoiAy1Cdi2RcODoGR4OeWA9u89ydyrGh5TRYLf6bSEe6kLuTo+4ksXaJe3g2Nhx3gwHu+IKxOwGK/N31Zawo0Jt36pFwG/SGcrBhXR8CkYtJPoJ7u93oK2U4RZNhS/fTL6ty1MrXSBxmgg+HFS1HFZyhPs3QXPuJGNBG1QYR6OEV1BKOu3S27ZPgSMc/R1ebPLqxiE3wtyhzYN3rsM4oztjqH140KfrkUnsE/3jwc2NASEK0CAwEAAaOCAcEwggG9MA4GA1UdDwEB/wQEAwIBBjAPBgNVHRMBAf8EBTADAQH/MIHKBgNVHR8EgcIwgb8weaB3oHWkczBxMQswCQYDVQQGEwJVUzE0MDIGA1UEChMrSW50ZXJuYXRpb25hbCBCdXNpbmVzcyBNYWNoaW5lcyBDb3Jwb3JhdGlvbjEdMBsGA1UEAxMUSUJNIEludGVybmFsIFJvb3QgQ0ExDTALBgNVBAMTBENSTDAwQqBAoD6GPGh0dHA6Ly9kYXltdnMxLnBvay5pYm0uY29tOjIwMDEvUEtJU2Vydi9jYWNlcnRzUm9vdC9DUkwwLmNybDAdBgNVHQ4EFgQUBi/ax5ofP4dRuU3Q9tqul0ZKncgwHwYDVR0jBBgwFoAU+d4Y5Z4wE2lRp/15hUiMfA5v2OMwgYwGA1UdIASBhDCBgTB/BgMqAwQweDB2BggrBgEFBQcCARZqaHR0cDovL3czLTAzLmlibS5jb20vdHJhbnNmb3JtL3Nhcy9hcy13ZWIubnNmL0NvbnRlbnREb2NzQnlUaXRsZS9JbmZvcm1hdGlvbitUZWNobm9sb2d5K1NlY3VyaXR5K1N0YW5kYXJkczANBgkqhkiG9w0BAQsFAAOCAQEAWwI8opg0H1ukbTLsf+XXRrHYBDUB3pwAApSh9fruGc3Nt5IbKD8687oiutxBFwJ0xxPdP1/BL3HycCqzSDQFtSVdUASJOF1+GB9DNDwrreOWaUTg2cHCIxOij9E9ypU64we9OL27FjcwYKnDbqfOrsxrtrRaxLmM2+lNaBHIMsAIbMH9vN11G7SpzsZ5Nr5hZXIlxfq9/HfQujE6hoCgt2hoM0i4gRyLdVOaNCHPeoVO6n7OsOKm36BgXT62B36e5rvdKzzbUZZLse9QPtvRychyAPAX89wiHIqiFstesWL+kImp1C9L6iVM4DGbwGCqKxTnX2asika0xH3gWuoZjA==
-----END CERTIFICATE-----
        """,
            "preserve_label": "true"
        },
    ]
    return testdata

@pytest.mark.order(after="test_0_base_1_ssl_certificate_databases.py::test_update_certificate_database")
@pytest.mark.parametrize("items", getTestData())
def test_import_signer_cert(iviaServer, caplog, items) -> None:
    """Import signer certificates"""
    caplog.set_level(logging.DEBUG)
    logging.log(logging.INFO, items)
    arg = {}
    kdb_id = None
    cert = None
    label = None
    preserve_label = 'false'
    for k, v in items.items():
        if k == 'kdb_id':
            kdb_id = v
            continue
        if k == 'cert':
            cert = v
            continue
        if k == 'label':
            label = v
            continue
        if k == 'preserve_label':
            preserve_label = v
            continue
        arg[k] = v
    returnValue = ibmsecurity.isam.base.ssl_certificates.signer_certificate.import_cert(iviaServer,
                                                                                        kdb_id,
                                                                                        cert,
                                                                                        label,
                                                                                        preserve_label,
                                                                                        **arg
                                                                                        )
    logging.log(logging.INFO, returnValue)

    assert not returnValue.failed()


def getTestDataSigners():
    testdata = [
        {"kdb_id": "pdsrv", "cert_id": "new_cert"},
    ]
    return testdata

@pytest.mark.order(after="test_import_signer_cert")
@pytest.mark.parametrize("items", getTestDataSigners())
def test_get_signer_cert_not_existing(iviaServer, caplog,items) -> None:
    """Get single signer."""
    caplog.set_level(logging.DEBUG)
    arg = {}
    kdb_id = None
    cert = None
    for k, v in items.items():
        if k == 'kdb_id':
            kdb_id = v
            continue
        if k == 'cert_id':
            cert = v
            continue
        arg[k] = v
    returnValue = ibmsecurity.isam.base.ssl_certificates.signer_certificate.get(iviaServer,
                                                  kdb_id,
                                                  cert,
                                                  **arg)
    logging.log(logging.INFO, returnValue)
    # Expect this to fail
    assert returnValue.failed()
