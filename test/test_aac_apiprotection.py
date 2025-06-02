import logging

import ibmsecurity.isam.aac.api_protection.definitions
import ibmsecurity.isam.appliance

import pytest


def getTestData():
    testdata = [
        {
            "name": "test1",
            "tcmBehavior": "NEVER_PROMPT",
            "authorizationCodeLength": 30,
            "enforceSingleAccessTokenPerGrant": True,
            "accessTokenLength": 20,
            "enableMultipleRefreshTokensForFaultTolerance": True,
            "pinPolicyEnabled": False,
            "issueRefreshToken": False,
            "description": "Issue Tokens",
            "oidc": {
                'issueSecret': True,
                'fapiCompliant': False,
                'poc': 'https://webseal01/mga',
                'iss': 'https://webseal01',
                'lifetime': 3600,
                'cert': 'WebSEAL-Test-Only',
                'enabled': True,
                'dynamicClients': True,
                'enc': {
                    'enabled': False
                },
                'includeIssInAuthResp': True,
                'alg': 'RS256',
                'db': 'pdsrv',
                'oidcCompliant': False
            },
            "refreshTokenLength": 40,
            "grantTypes": ['JWT_BEARER',
                           'IMPLICIT_GRANT',
                           'CLIENT_CREDENTIALS',
                           'AUTHORIZATION_CODE'
                           ],
            "tokenCharSet": '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwx',
            "authorizationCodeLifetime": 300,
            "enforceSingleUseAuthorizationGrant": True,
            "pinLength": 4,
            "maxAuthorizationGrantLifetime": 604800,
            "accessTokenLifetime": 900
        },
        {
            "name": "test2",
            "description": "Issue Tokens",
            "grantTypes": ['JWT_BEARER',
                           'IMPLICIT_GRANT',
                           'CLIENT_CREDENTIALS',
                           'AUTHORIZATION_CODE'
                           ],
        },
    ]
    return testdata


@pytest.mark.parametrize("items", getTestData())
def test_set_apiprotection_definition(iviaServer, caplog, items) -> None:
    """Set api protection"""
    caplog.set_level(logging.DEBUG)
    # items is a key-value pair
    logging.log(logging.INFO, items)
    arg = {}
    for k, v in items.items():
        if k == 'name':
            name = v
            continue
        arg[k] = v

    returnValue = ibmsecurity.isam.aac.api_protection.definitions.set(iviaServer,
                                                                      name,
                                                                      **arg
                                                                      )
    logging.log(logging.INFO, returnValue)

    assert not returnValue.failed()
