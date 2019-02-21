from charmhelpers.core import (
    hookenv,
    host,
    templating
)
from charmhelpers import fetch


class NfsganeshaHelper():
    def __init__(self):
        self.charm_config = hookenv.config()
        self.config_file = '/etc/ganesha/ganesha.conf'
        self.default_mode = self.charm_config['ganesha-default-access-mode'].upper()
        self.default_acls_line = self.charm_config['ganesha-default-acls']
        self.export_line = self.charm_config['ganesha-exports']
        self.exports = []
        self.default_acls = []

    def restart_service(self):
        ''' Restart NFS Ganesha '''
        host.service('restart', 'nfs-ganesha')
        return True

    def reload_config(self):
        ''' Reload the config by sending SIGHUP '''
        # TODO: reload doesn't seem to work from charm hook, restart for now
        host.service('restart', 'nfs-ganesha')
        return True

    def start_enable_service(self):
        ''' Start and enable NFS Ganesha '''
        host.service('enable', 'nfs-ganesha')
        host.service('start', 'nfs-ganesha')
        return True

    def install_nfs_ganesha(self):
        fetch.apt_install([
            'nfs-ganesha',
            'nfs-ganesha-vfs'
        ])
        self.start_enable_service()
        return True

    def parse_acls(self, acls, default_mode=None):
        '''
        Create a dict of ACLs based on string input
        format is -
        [
            clients <-- network mask for clients
            access  <-- access mode, RO, RW for example
        ]
        The string input takes format -
        x.x.x.x/y=mode, where =mode is =ro or =rw and is optional
        when =mode is not specified, mode will be set to
        default_mode, which defaults to the charm default
        '''
        if not default_mode:
            default_mode = self.default_mode
        acls_parsed = []
        acl_list = acls.split(',')
        for acl in acl_list:
            parsed_acl = {}
            if '=' in acl:
                split_acl = acl.split('=')
                if split_acl[1].lower() == 'rw':
                    split_acl[1] = 'RW'
                else:
                    split_acl[1] = 'RO'

                parsed_acl = {
                    'clients': split_acl[0],
                    'access': split_acl[1],
                }
            else:
                parsed_acl = {
                    'clients': acl,
                    'access': default_mode
                }
            acls_parsed.append(parsed_acl)
        return acls_parsed

    def parse_exports(self, exportline):
        '''
        Created a dict of exports for passing to the template
        render routine. The format is -
        [
            {
                path <-- this is set to the export path
                access <-- ro or rw, based on mode specified in
                           export, or the default acccess mode
                acls [ <-- optional list of ACLs, will be made up
                           of default ACLs, or export-specific ACLs
                    clients <-- network mask for this ACL
                    access  <-- access mode, defaults to export
                                access mode, which inherently defaults
                                to charm-level default access mode
                ]
        ]
        '''
        # dict for finished exports
        exports = []
        # parse default ACLs to list, fill with default mode
        exports_parse = self.export_line.split(',')
        # parse each entry, splitting out options by ':'
        for export_entry in exports_parse:
            export = {}
            export['acls'] = self.default_acls
            # parse exports to list, add default acls, and any export acls
            if ':' in export_entry:
                options = export_entry.split(':')
                export['path'] = options[0]
                if len(options) > 2:
                    # we have acls
                    acls = options[2:]
                    for acl in acls:
                        export['acls'].extend(
                            self.parse_acls(acl, export['access']))
                if len(options) > 1:
                    # we have an export mode
                    # check if it's a supported mode otherwise
                    # set to charm default
                    mode = options[1]
                    if mode.lower() == 'rw':
                        export['access'] = 'RW'
                    elif mode.lower() == 'ro':
                        export['access'] = 'RO'
                    else:
                        export['access'] = self.default_mode
                else:
                    export['access'] = self.default_mode
            else:
                # no export mode or acls, use defaults
                export['path'] = export_entry
                export['access'] = self.default_mode
            exports.append(export)
        return exports

    def clean_default_mode(self):
        if self.default_mode == 'rw':
            self.default_mode = 'RW'
        else:
            self.default_mode = 'RO'

    def configure_nfs_ganesha(self):
        self.clean_default_mode()
        self.default_acls = self.parse_acls(
            self.default_acls_line
        )
        self.exports = self.parse_exports(
            self.export_line
        )
        templating.render('ganesha.conf.j2',
                          self.config_file,
                          {
                              'exports': self.exports
                          })
        self.reload_config()
        self.start_enable_service()
