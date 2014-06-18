#!/usr/bin/python

import os
import sys
import argparse

from novaclient.v1_1 import client as novaclient

import common
import keystone_example

def parse_args():
    p = common.create_parser()
    return p.parse_args()

def main():
    args = parse_args()

    nc = novaclient.Client(
        args.os_username,
        args.os_password,
        args.os_tenant_id,
        auth_url=args.os_auth_url,
        tenant_id=args.os_tenant_id)

    for server in nc.servers.list():
        print server.id, server.name
        for network_name, network in server.networks.items():
            print '    ', network_name, ', '.join(network)

if __name__ == '__main__':
    main()


