from lib_nfs_ganesha import NfsganeshaHelper
from charmhelpers.core import hookenv
from charms.reactive import (
    set_flag,
    clear_flag,
    when_not,
    when
)

ganesha = NfsganeshaHelper()


@when_not('nfs-ganesha.installed')
def install_nfs_ganesha():
    hookenv.status_set('maintenance', 'Installing nfs-ganesha')
    ganesha.install_nfs_ganesha()
    set_flag('nfs-ganesha.installed')
    hookenv.status_set('maintenance', 'Installed nfs-ganesha')


@when('config.changed')
def reconfigure_nfs_ganesha():
    clear_flag('nfs_ganesha.configured')
    hookenv.status_set('maintenance', 'Configuring nfs-ganesha')
    ganesha.configure_nfs_ganesha()
    set_flag('nfs-ganesha.configured')
    hookenv.status_set('active', 'nfs-ganesha ready')


@when_not('nfs-ganesha.configured')
@when('nfs-ganesha.installed')
def configure_nfs_ganesha():
    if ganesha.charm_config['ganesha-exports']:
        hookenv.status_set('maintenance', 'Configuring nfs-ganesha')
        ganesha.configure_nfs_ganesha()
        set_flag('nfs-ganesha.configured')
        hookenv.status_set('active', 'nfs-ganesha ready')
    else:
        hookenv.status_set('blocked', 'At least one export needs to be added to ganesha_exports')
