import os
import pytest
from juju.model import Model

# Treat tests as coroutines
pytestmark = pytest.mark.asyncio

series = ['xenial', 'bionic']
juju_repository = os.getenv('JUJU_REPOSITORY', '.').rstrip('/')


@pytest.fixture
async def model():
    model = Model()
    await model.connect_current()
    yield model
    await model.disconnect()


@pytest.fixture
async def apps(model):
    apps = []
    for entry in series:
        app = model.applications['nfs-ganesha-{}'.format(entry)]
        apps.append(app)
    return apps


@pytest.fixture
async def units(apps):
    units = []
    for app in apps:
        units.extend(app.units)
    return units


@pytest.mark.parametrize('series', series)
async def test_nfsganesha_deploy(model, series):
    # Starts a deploy for each series
    await model.deploy('{}/builds/nfs-ganesha'.format(juju_repository),
                       series=series,
                       application_name='nfs-ganesha-{}'.format(series))
    assert True


async def test_nfsganesha_status(apps, model):
    # Verifies status for all deployed series of the charm
    for app in apps:
        await model.block_until(lambda: app.status == 'blocked')
    assert True


async def test_nfsganesha_export(apps, model):
    for app in apps:
        await app.set_config({'ganesha-default-acls':
                              "127.0.0.0/8=rw,192.168.0.0/8=ro,172.16.0.0/16"})
        await app.set_config({'ganesha-default-access-mode':
                              "ro"})
        await app.set_config({'ganesha-exports':
                              "/:ro:10.0.0.0/8=rw,/home:rw"})
    for app in apps:
        await model.block_until(lambda: app.status == 'blocked')


async def test_restart_action(units):
    for unit in units:
        action = await unit.run_action('restart')
        action = await action.wait()
        assert action.status == 'completed'


async def test_reload_action(units):
    for unit in units:
        action = await unit.run_action('reload')
        action = await action.wait()
        assert action.status == 'completed'
