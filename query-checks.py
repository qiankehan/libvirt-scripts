#!/usr/bin/python3
import libvirt
import libvirt_qemu
import argparse
import json
import subprocess
import logging
from tempfile import NamedTemporaryFile


def queries_comapare(dom: libvirt.virDomain, qmps: list, cmd: str) -> bool:
    results_before_cmd = {q: json.loads(
                          libvirt_qemu.qemuMonitorCommand(dom, '{"execute": "%s"}' % q, 0)).get('return') for q in qmps}
    subprocess.getoutput(cmd)
    results_after_cmd = {q: json.loads(
                         libvirt_qemu.qemuMonitorCommand(dom, '{"execute": "%s"}' % q, 0)).get('return') for q in qmps}
    for q in qmps:
        if results_before_cmd[q] != results_after_cmd[q]:
            with NamedTemporaryFile('wt', prefix='{0}_{1}_'.format(dom.name(), q), suffix='.json', delete=False) as a, \
                    NamedTemporaryFile('wt', prefix='{0}_{1}_'.format(dom.name(), q), suffix='.json', delete=False) as b:
                json.dump(results_before_cmd[q], a, indent=4)
                json.dump(results_after_cmd[q], b, indent=4)
                logging.warning("The results of QMP {0} don't equal. They are saved to {1} {2}".format(
                    q, a.name, b.name))


def get_query_qmps(dom: libvirt.virDomain) -> list:
    qmp = '{"execute": "query-commands"}'
    return ','.join(sorted([i["name"] for i in json.loads(libvirt_qemu.qemuMonitorCommand(dom, qmp, 0))["return"] if 'query' in i["name"]]))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        "Check QMP queries before and after a command")
    parser.add_argument('-u', '--uri', help="The uri of libvirt",
                        type=str, default="qemu:///system")
    parser.add_argument(
        '-d', '--domain', help="The running domain name", type=str, required=True)
    parser.add_argument(
        '-c', '--cmd', help="The cmd that will run before or after the qmps", type=str)
    parser.add_argument('-l', '--list', action='store_true',
                        help="List the supported query commands")
    parser.add_argument('-q', '--qmps', type=str,
                        help="The QMP query command list, like qmp1,qmp2,...")

    args = parser.parse_args()
    with libvirt.open(args.uri) as conn:
        dom = conn.lookupByName(args.domain)
        if args.list:
            print(get_query_qmps(dom))
            exit(0)

        queries_comapare(dom, args.qmps.split(','), args.cmd)

    exit(0)
