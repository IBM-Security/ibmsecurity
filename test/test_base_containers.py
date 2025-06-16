import logging

import ibmsecurity.isam.base.container_ext.container
import ibmsecurity.isam.base.container_ext.volume
import ibmsecurity.isam.base.container_ext.image
import ibmsecurity.isam.appliance

import pytest

def getTestData():
    containerConfig = [
        {"name": "oidcop",
         "image": "icr.io/ivia/ivia-oidc-provider:25.03",
         "type": "verify-access-oidc-provider",
         "ports": [{"name": "https",
                  "value": "0.0.0.0:32443"},
                   {"name": "http",
                     "value": "0.0.0.0:32080"}
          ],
         "volumes": [{"name": "configuration",
             "volume_name": "config.volume.oidc"}
            ]
        }
    ]
    return containerConfig

def getTestDataVolumes():
    c = [
        {"filename": "test/files/oidcop.zip",
         "volume_name": "config.volume.oidc"}
    ]
    return c

def test_get_images(iviaServer, caplog) -> None:
    """Get container images"""
    caplog.set_level(logging.DEBUG)
    arg = {}

    returnValue = ibmsecurity.isam.base.container_ext.image.get_all(iviaServer,
                                                                **arg
                                                               )
    logging.log(logging.INFO, returnValue)

    assert not returnValue.failed()

@pytest.mark.parametrize("items", getTestData())
def test_set_image(iviaServer, caplog, items) -> None:
    """Set image"""
    caplog.set_level(logging.DEBUG)
    # items is a key-value pair
    logging.log(logging.INFO, items)
    arg = {}
    image = None
    for k, v in items.items():
        if k == 'image':
            image = v
            continue
        #if k == 'key':
        #    key = v
        #    continue
        # arg[k] = v
        else:
            logging.log(logging.INFO,"Skipping all other items")
            continue

    returnValue = ibmsecurity.isam.base.container_ext.image.set(iviaServer, image,  **arg)

    logging.log(logging.INFO, returnValue)

    if returnValue is not None:
        assert not returnValue.failed()

def test_get_volumes(iviaServer, caplog) -> None:
    """Get volumes"""
    caplog.set_level(logging.DEBUG)
    arg = {}

    returnValue = ibmsecurity.isam.base.container_ext.volume.get_all(iviaServer,
                                                                **arg
                                                               )
    logging.log(logging.INFO, returnValue)

    assert not returnValue.failed()


@pytest.mark.parametrize("items", getTestData())
def test_set_volumes(iviaServer, caplog, items) -> None:
    """Set container volumes"""
    caplog.set_level(logging.DEBUG)
    # items is a key-value pair
    logging.log(logging.INFO, items)
    arg = {}
    _volumes = None
    for k, v in items.items():
        if k == 'volumes':
            _volumes = v
            continue
        #if k == 'key':
        #    key = v
        #    continue
        # arg[k] = v
        else:
            logging.log(logging.INFO,"Skipping all other items")
            continue

    for i in _volumes:
        if i.get('volume_name', None) is not None:
            returnValue = ibmsecurity.isam.base.container_ext.volume.add(iviaServer, i['volume_name'], **arg)

            logging.log(logging.INFO, returnValue)

            if returnValue is not None:
                assert not returnValue.failed()
            continue
        else:
            logging.log(logging.INFO, "Skip invalid volume item")
            continue

@pytest.mark.parametrize("items", getTestDataVolumes())
def test_config_volume(iviaServer, caplog, items) -> None:
    """Import data into container volume"""
    caplog.set_level(logging.DEBUG)
    # items is a key-value pair
    logging.log(logging.INFO, items)
    arg = {}
    filename = None
    for k, v in items.items():
        if k == 'filename':
            filename = v
            continue
        arg[k] = v

    returnValue = ibmsecurity.isam.base.container_ext.volume.import_zip(iviaServer, filename, **arg)

    logging.log(logging.INFO, returnValue)

    if returnValue is not None:
        assert not returnValue.failed()


def test_get_containers(iviaServer, caplog) -> None:
    """Get sms protection"""
    caplog.set_level(logging.DEBUG)
    arg = {}

    returnValue = ibmsecurity.isam.base.container_ext.container.get_all(iviaServer,
                                                                **arg
                                                               )
    logging.log(logging.INFO, returnValue)

    assert not returnValue.failed()

@pytest.mark.parametrize("items", getTestData())
def test_set_containers(iviaServer, caplog, items) -> None:
    """Set admin ssh keys"""
    caplog.set_level(logging.DEBUG)
    # items is a key-value pair
    logging.log(logging.INFO, items)
    arg = {}
    name, image, _type, ports, volumes = None, None, None, None, None
    for k, v in items.items():
        if k == 'name':
            name = v
            continue
        if k == 'image':
            image = v
            continue
        if k == 'type':
            _type = v
            continue
        if k == 'ports':
            ports = v
            continue
        if k == 'volumes':
            volumes = v
            continue
        arg[k] = v
    if arg == {}:
        returnValue = ibmsecurity.isam.base.container_ext.container.set(iviaServer, name, image, _type, ports, volumes)
    else:
        returnValue = ibmsecurity.isam.base.container_ext.container.set(iviaServer, name, image, _type, ports, volumes,
                                                                    **arg)

    logging.log(logging.INFO, returnValue)

    if returnValue is not None:
        assert not returnValue.failed()
