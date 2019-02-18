# NFS-Ganesha

The NFS Ganesha charm installs configures exports and ACLs for the
nfs-ganesha userspace NFS implementation. 

# Usage

`juju deploy cs:~pirate-charmers/nfs-ganesha`

# Configuration

The following configuration options are supported:

```
  ganesha-exports:
    type: string
    default: ""
```
A comma separated list of filesystems to export via NFS and 9P.
Optionally, access modes and ACLs can be appended separated by commas.
Access mode and ACL specified in the export will override the
settings in ganesha-default-acl and ganesha-default-access-mode.
Multiple ACLs can be added to each export, by appending them to the
export separated by colons.
The access mode for an ACL can be overridden by appending =ro or =rw
to the ACL.

A complex example: `/fs:rw:192.168.0.0/24=ro:172.16.50.0/24=rw,/fs2,/fs3:ro"`

```
  ganesha-default-access-mode:
    type: string
    default: "ro"
```

The default access mode to set on exported filesystems.
This will also be the default access mode for any ACLs.
Defaults to read only.

```
  ganesha-default-acls:
    type: string
    default: ""
```

The default ACLs to add to exported filesystems, unrestricted is the default.
Multiple default ACLs can be set, separated by commas.
The access mode for each ACL can be specified by appending =ro or =rw to the ACL.

# Contact Information

Though this will be listed in the charm store itself don't assume a user will
know that, so include that information here:


  - [Upstream wiki](https://github.com/nfs-ganesha/nfs-ganesha/wiki)
  - [Upstream bug tracker](https://github.com/nfs-ganesha/nfs-ganesha/issues)
  - [Charm bug trackers](https://github.com/pirate-charmers/layer-nfs-ganesha/issues)
  - [Charm source](https://github.com/pirate-charmers/layer-nfs-ganesha)
  - [Pirate Charmers](https://github.com/pirate-charmers/ 

