#!/usr/bin/env python3

import sys
import queue
import threading
import ipaddress
import subprocess

from socket import inet_aton, inet_ntoa
from struct import pack as struct_pack, unpack as struct_unpack

OPT = "-n 1 -w 1000" if sys.platform in ("win32", "cygwin") else "-c 1 -W 1"


def ping_ip(ip, results):
    ok = True
    try:
        subprocess.check_output("ping {0} {1}".format(OPT, ip), shell=True)
    except Exception:
        ok = False
        results.put(ip)
    print("Test  {:15} -->  {}".format(ip, "OK" if ok else "X"))


def _ping_ips(ips):
    tasks = []
    results = queue.Queue()
    for ip in ips:
        t = threading.Thread(target=ping_ip, args=(ip, results), daemon=True)
        t.start()
        tasks.append(t)

    for t in tasks:
        t.join()

    ips = []
    while True:
        try:
            ips.append(results.get_nowait())
            results.task_done()
        except Exception:
            break
    return ips


def ping_ips(ips, size=1000):
    results = []
    while ips:
        results.extend(_ping_ips(ips[:size]))
        ips = ips[size:]

    return results


def parse_ips(args):
    ips = set()
    for v in args:
        for ip in v.split(","):
            ip = ip.strip()
            if not ip:
                continue
            if "/" not in ip:
                ips.add(ip)
                continue
            for ip in ipaddress.IPv4Network(ip, strict=False).hosts():
                ips.add(str(ip))

    return sorted(ips)


if __name__ == "__main__":
    ips = parse_ips(sys.argv[1:])
    failed_ips = ping_ips(ips)
    print("\nFailed IPs:\n {}".format(failed_ips))
