import logging
import pytest

import ibmsecurity.isam.aac.scim
import ibmsecurity.isam.aac.scim.scim
import ibmsecurity.isam.appliance


def getTestData():
    testdata = [
        {       "enable_header_authentication": True,
                "enable_authz_filter": True,
                "admin_group": "adminGroup",
                "max_user_responses": 256,
                "urn:ietf:params:scim:schemas:extension:isam:1.0:User": {
                    "ldap_connection": "Verify Access Runtime",
                    "isam_domain": "Default",
                    "update_native_users": True,
                    "connection_type": "isamruntime",
                    "enforce_password_policy": False,
                    "mapping": []
                },
                "urn:ietf:params:scim:schemas:core:2.0:Group": {
                    "ldap_object_classes": [
                        {
                            "name": "groupOfNames"
                        }
                    ],
                    "group_dn": "cn"
                },
                "urn:ietf:params:scim:schemas:core:2.0:User": {
                    "ldap_connection": "Verify Access Runtime",
                    "search_suffix": "o=ibm",
                    "user_suffix": "ou=people,o=ibm",
                    "user_dn": "uid",
                    "user_id": "uid",
                    "attrs_dir": "",
                    "connection_type": "isamruntime",
                    "enforce_password_policy": False,
                    "ldap_object_classes": [
                        {
                            "name": "top"
                        },
                        {
                            "name": "person"
                        },
                        {
                            "name": "organizationalPerson"
                        },
                        {
                            "name": "inetOrgPerson"
                        },
                        {
                            "name": "nsiPerson"
                        }
                    ],
                    "mappings": [
                        {
                            "scim_attribute": "userName",
                            "mapping": {
                                "source": "cn",
                                "type": "ldap"
                            }
                        },
                        {
                            "scim_attribute": "displayName",
                            "mapping": {
                                "source": "displayName",
                                "type": "ldap"
                            }
                        },
                        {
                            "scim_attribute": "preferredLanguage",
                            "mapping": {
                                "source": "preferredLanguage",
                                "type": "ldap"
                            }
                        },
                        {
                            "scim_attribute": "title",
                            "mapping": {
                                "source": "title",
                                "type": "ldap"
                            }
                        },
                        {
                            "scim_attribute": "password",
                            "mapping": {
                                "source": "userPassword",
                                "type": "ldap"
                            }
                        },
                        {
                            "scim_attribute": "name",
                            "mapping": [
                                {
                                    "source": "sn",
                                    "scim_subattribute": "familyName",
                                    "type": "ldap"
                                },
                                {
                                    "source": "givenName",
                                    "scim_subattribute": "givenName",
                                    "type": "ldap"
                                }
                            ]
                        },
                        {
                            "scim_attribute": "emails",
                            "mapping": [
                                {
                                    "extended_scim_attributes": [
                                        {
                                            "name": "type",
                                            "source": "work",
                                            "type": "fixed"
                                        },
                                        {
                                            "name": "primary",
                                            "source": "True",
                                            "type": "fixed"
                                        },
                                        {
                                            "name": "value",
                                            "source": "mail",
                                            "type": "ldap"
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "scim_attribute": "addresses",
                            "mapping": [
                                {
                                    "extended_scim_attributes": [
                                        {
                                            "name": "type",
                                            "source": "home",
                                            "type": "fixed"
                                        },
                                        {
                                            "name": "formatted",
                                            "source": "homePostalAddress",
                                            "type": "ldap"
                                        }
                                    ]
                                },
                                {
                                    "extended_scim_attributes": [
                                        {
                                            "name": "type",
                                            "source": "work",
                                            "type": "fixed"
                                        },
                                        {
                                            "name": "formatted",
                                            "source": "postalAddress",
                                            "type": "ldap"
                                        },
                                        {
                                            "name": "streetAddress",
                                            "source": "street",
                                            "type": "ldap"
                                        },
                                        {
                                            "name": "postalCode",
                                            "source": "postalCode",
                                            "type": "ldap"
                                        },
                                        {
                                            "name": "locality",
                                            "source": "l",
                                            "type": "ldap"
                                        },
                                        {
                                            "name": "region",
                                            "source": "st",
                                            "type": "ldap"
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "scim_attribute": "phoneNumbers",
                            "mapping": [
                                {
                                    "extended_scim_attributes": [
                                        {
                                            "name": "type",
                                            "source": "pager",
                                            "type": "fixed"
                                        },
                                        {
                                            "name": "primary",
                                            "source": "false",
                                            "type": "fixed"
                                        },
                                        {
                                            "name": "value",
                                            "source": "pager",
                                            "type": "ldap"
                                        }
                                    ]
                                },
                                {
                                    "extended_scim_attributes": [
                                        {
                                            "name": "type",
                                            "source": "work",
                                            "type": "fixed"
                                        },
                                        {
                                            "name": "primary",
                                            "source": "true",
                                            "type": "fixed"
                                        },
                                        {
                                            "name": "value",
                                            "source": "telephoneNumber",
                                            "type": "ldap"
                                        }
                                    ]
                                },
                                {
                                    "extended_scim_attributes": [
                                        {
                                            "name": "type",
                                            "source": "home",
                                            "type": "fixed"
                                        },
                                        {
                                            "name": "primary",
                                            "source": "false",
                                            "type": "fixed"
                                        },
                                        {
                                            "name": "value",
                                            "source": "homePhone",
                                            "type": "ldap"
                                        }
                                    ]
                                },
                                {
                                    "extended_scim_attributes": [
                                        {
                                            "name": "type",
                                            "source": "mobile",
                                            "type": "fixed"
                                        },
                                        {
                                            "name": "primary",
                                            "source": "false",
                                            "type": "fixed"
                                        },
                                        {
                                            "name": "value",
                                            "source": "mobile",
                                            "type": "ldap"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                "urn:ietf:params:scim:schemas:extension:enterprise:2.0:User": {
                    "mappings": [
                        {
                            "scim_attribute": "employeeNumber",
                            "mapping": {
                                "source": "employeeNumber",
                                "type": "ldap"
                            }
                        },
                        {
                            "scim_attribute": "organization",
                            "mapping": {
                                "source": "o",
                                "type": "ldap"
                            }
                        },
                        {
                            "scim_attribute": "department",
                            "mapping": {
                                "source": "departmentNumber",
                                "type": "ldap"
                            }
                        },
                        {
                            "scim_attribute": "manager",
                            "mapping": {
                                "source": "manager",
                                "scim_subattribute": "value",
                                "type": "ldap"
                            }
                        }
                    ]
                }

        }
    ]
    return testdata

@pytest.mark.skip(reason="Work in progress")
@pytest.mark.parametrize("items", getTestData())
def test_set_scim(iviaServer, caplog, items) -> None:
    """Set api protection"""
    caplog.set_level(logging.DEBUG)
    # items is a key-value pair
    logging.log(logging.INFO, items)
    # arg = {}
    # for k, v in items.items():
    #    arg[k] = v

    returnValue = ibmsecurity.isam.aac.scim.scim.set_all(iviaServer,
                                                    items
                                                    )
    logging.log(logging.INFO, returnValue)

    assert not returnValue.failed()
