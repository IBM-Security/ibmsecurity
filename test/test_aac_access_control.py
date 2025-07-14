import logging

import ibmsecurity.isam.aac.access_control.policies
import ibmsecurity.isam.aac.access_control.policy_attachments
import ibmsecurity.isam.aac.access_control.policy_sets
import ibmsecurity.isam.appliance

import pytest
import os


def getTestData():
    testdata = [
        {
            "dialect": "urn:oasis:names:tc:xacml:2.0:policy:schema:os",
            "attributesRequired": False,
            "name": "Test Access Control Policy",
            "description": "Permit access",
            "predefined": False,
            "formatting": "json",
            "policy": {
                "PolicyTag": "urn:ibm:security:isam:8.0:xacml:2.0:config-policy",
                "PolicyName": "Test Access Control Policy",
                "PolicySet": {
                    "Policy": [
                        {
                            "RuleCombiningAlgId": "urn:oasis:names:tc:xacml:1.0:rule-combining-algorithm:first-applicable",
                            "Rule": {
                                "Condition": {
                                    "Apply": [
                                        {
                                            "FunctionId": "urn:oasis:names:tc:xacml:1.0:function:and",
                                            "Apply": [
                                                {
                                                    "FunctionId": "urn:oasis:names:tc:xacml:1.0:function:any-of-any",
                                                    "Function": {
                                                        "FunctionId": "urn:oasis:names:tc:xacml:1.0:function:integer-less-than-or-equal"
                                                    },
                                                    "Apply": [
                                                        {
                                                            "FunctionId": "urn:oasis:names:tc:xacml:1.0:function:integer-bag",
                                                            "AttributeValue": {
                                                                "DataType": "http://www.w3.org/2001/XMLSchema#integer",
                                                                "content": 50
                                                            }
                                                        }
                                                    ],
                                                    "SubjectAttributeDesignator": [
                                                        {
                                                            "Issuer": "urn:ibm:security:issuer:RiskCalculator",
                                                            "AttributeId": "urn:ibm:security:subject:riskScore",
                                                            "MustBePresent": False,
                                                            "DataType": "http://www.w3.org/2001/XMLSchema#integer"
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                },
                                "RuleId": "urn:ibm:security:rule:0",
                                "Effect": "Permit"
                            },
                            "PolicyId": "urn:ibm:security:rule-container:0"
                        }
                    ],
                    "PolicyCombiningAlgId": "urn:oasis:names:tc:xacml:1.0:policy-combining-algorithm:first-applicable",
                    "Description": "Permit access"
                }
            }
        },
        {
            "dialect": "urn:oasis:names:tc:xacml:2.0:policy:schema:os",
            "attributesRequired": False,
            "name": "Test Access Control Policy 2",
            "description": "Permit access",
            "predefined": False,
            "formatting": "json",
            "policy": {
                "PolicyTag": "urn:ibm:security:isam:8.0:xacml:2.0:config-policy",
                "PolicyName": "Test Access Control Policy 2",
                "PolicySet": {
                    "Policy": [
                        {
                            "RuleCombiningAlgId": "urn:oasis:names:tc:xacml:1.0:rule-combining-algorithm:first-applicable",
                            "Rule": {
                                "Condition": {
                                    "Apply": [
                                        {
                                            "FunctionId": "urn:oasis:names:tc:xacml:1.0:function:and",
                                            "Apply": [
                                                {
                                                    "FunctionId": "urn:oasis:names:tc:xacml:1.0:function:any-of-any",
                                                    "Function": {
                                                        "FunctionId": "urn:oasis:names:tc:xacml:1.0:function:integer-less-than-or-equal"
                                                    },
                                                    "Apply": [
                                                        {
                                                            "FunctionId": "urn:oasis:names:tc:xacml:1.0:function:integer-bag",
                                                            "AttributeValue": {
                                                                "DataType": "http://www.w3.org/2001/XMLSchema#integer",
                                                                "content": 50
                                                            }
                                                        }
                                                    ],
                                                    "SubjectAttributeDesignator": [
                                                        {
                                                            "Issuer": "urn:ibm:security:issuer:RiskCalculator",
                                                            "AttributeId": "urn:ibm:security:subject:riskScore",
                                                            "MustBePresent": True,
                                                            "DataType": "http://www.w3.org/2001/XMLSchema#integer"
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                },
                                "RuleId": "urn:ibm:security:rule:0",
                                "Effect": "Deny"
                            },
                            "PolicyId": "urn:ibm:security:rule-container:0"
                        }
                    ],
                    "PolicyCombiningAlgId": "urn:oasis:names:tc:xacml:1.0:policy-combining-algorithm:first-applicable",
                    "Description": "Deny access"
                }
            }
        }
    ]
    return testdata


def getPolicyAttachmentData():
    testdata = [
        {"server": "isva11kvm-default",
         "resourceUri": "/molecule.html",
         "policyCombiningAlgorithm": "denyOverrides",
         "policies": [
             {"name": "Test Access Control Policy",
              "type": "policy"
              }
             ],
         "type": "reverse_proxy",
         "cache": 0
         },
        {"server": "isva11kvm-default",
         "resourceUri": "/index.html",
         "policyCombiningAlgorithm": "denyOverrides",
         "policies": [
             {"name": "Test Access Control Policy 2",
              "type": "policy"
              }
         ],
         "type": "reverse_proxy",
         "cache": 0
         },
        {"server": "mobileApp",
         "resourceUri": "/registerApp",
         "policyCombiningAlgorithm": "denyOverrides",
         "policies": [
             {"name": "Test Access Control Policy",
              "type": "policy"
              }
         ],
         "type": "application",
         "cache": 0
         },
        {"server": "mobileApp",
         "resourceUri": "/somethingelseApp",
         "policyCombiningAlgorithm": "denyOverrides",
         "policies": [
             {"name": "Test Access Control Policy",
              "type": "policy"
              }
         ],
         "type": "application",
         "cache": 0
         },
    ]
    return testdata


@pytest.mark.parametrize("items", getTestData())
def test_set_accesscontrol_policies(iviaServer, caplog, items) -> None:
    """Set api protection"""
    caplog.set_level(logging.DEBUG)
    # items is a key-value pair
    logging.log(logging.INFO, items)
    arg = {}
    for k, v in items.items():
        if k == 'name':
            name = v
            continue
        if k in ('attributesrequired', 'attributesRequired'):
            attributesrequired = v
            continue
        if k == 'policy':
            policy = v
            continue
        arg[k] = v

    returnValue = ibmsecurity.isam.aac.access_control.policies.set(iviaServer,
                                                                      name,
                                                                      attributesrequired,
                                                                      policy,
                                                                      **arg
                                                                      )
    logging.log(logging.INFO, returnValue)
    assert not returnValue.failed()


def test_authenticate(iviaServer, caplog) -> None:
    """Authenticate"""
    caplog.set_level(logging.DEBUG)
    # items is a key-value pair
    _secmaster = os.getenv('IVIA_SECMASTER') or 'sec_master'
    _secmasterpw = os.getenv('IVIA_SECMASTER_PW')

    returnValue = ibmsecurity.isam.aac.access_control.policy_attachments.authenticate(iviaServer,
                                                                      _secmaster,
                                                                      _secmasterpw
                                                                      )
    logging.log(logging.INFO, returnValue)

    assert not returnValue.failed()

@pytest.mark.parametrize("items", getPolicyAttachmentData())
def test_set_accesscontrol_policyattachments(iviaServer, caplog, items) -> None:
    """Set api protection"""
    caplog.set_level(logging.DEBUG)
    # items is a key-value pair
    logging.log(logging.INFO, items)
    arg = {}
    for k, v in items.items():
        if k == 'server':
            server = v
            continue
        if k in ('resourceUri', 'resourceuri'):
            resourceuri = v
            continue
        if k == 'policy':
            policy = v
            continue
        if k == 'type':
            arg['policyType'] = v
            continue
        arg[k] = v

    returnValue = ibmsecurity.isam.aac.access_control.policy_attachments.config(iviaServer,
                                                                      server,
                                                                      resourceuri,
                                                                      **arg
                                                                      )
    logging.log(logging.INFO, returnValue)
    assert not returnValue.failed()

@pytest.mark.parametrize("items", getPolicyAttachmentData())
def test_publish_policyattachment(iviaServer, caplog, items) -> None:
    """Publish"""
    caplog.set_level(logging.DEBUG)
    # items is a key-value pair
    logging.log(logging.INFO, items)
    arg = {}
    for k, v in items.items():
        if k == 'server':
            server = v
            continue
        if k in ('resourceUri', 'resourceuri'):
            resourceuri = v
            continue

    returnValue = ibmsecurity.isam.aac.access_control.policy_attachments.publish(iviaServer,
                                                                      server,
                                                                      resourceuri,
                                                                      **arg
                                                                      )
    logging.log(logging.INFO, returnValue)
    assert not returnValue.failed()
