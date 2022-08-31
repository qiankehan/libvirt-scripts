This project is to store the scripts that help test the libvirt project

# validate_all_xml
It could be used to validate all the [libvirt objects](https://libvirt.org/format.html) or a XML
file of libvirt by libvirt [RNG schemas](https://relaxng.org/).

## Requirement
Install these packeages before running it:
- python3-libvirt
- python3-lxml

## Examples
1. Validate all the libvirt objects from a [libvirt uri](https://libvirt.org/uri.html):
```
./validate_all_xml -c qemu+ssh://root@HOSTNAME/system
```
The default uri is the local system uri `qemu:///system`

2. Validate all the libvirt objects by a specific libvirt version:
```
./validate_all_xml -t v8.6.0
```
By default, libvirt will use the master branch of RNG schemas for validation. For all the arguments
for `-t`, get them from the [tags of libvirt project](https://gitlab.com/libvirt/libvirt/-/tags)  
It also support to validate the objects by the local RNG files:
`./validate_all_xml -d <rngfiles_dir>`

3. Validate a libvirt XML file:
```
./validate_all_xml -d domain.xml
```
