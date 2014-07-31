#!/usr/bin/python

import os
import sys
import argparse

from novaclient.v1_1 import client as novaclient

# Import code common to all of the examples.
import common
import keystone_example

def parse_args():
    p = common.create_parser()
    return p.parse_args()

def main():
    args = parse_args()

    kc = keystone_example.get_keystone_client(args)

    # We pass username, password, and project_id as None
    # because we want to use our existing Keystone token rather
    # than having Nova acquire a new one.
    nc = novaclient.Client(
        None,
        None,
        None,
        auth_url=args.os_auth_url,
        tenant_id=kc.tenant_id,
        auth_token=kc.auth_token)

    # Print a list of running servers.
    for server in nc.servers.list():
        print server.id, server.name
        for network_name, network in server.networks.items():
            print '    ', network_name, ', '.join(network)

if __name__ == '__main__':
    main()

