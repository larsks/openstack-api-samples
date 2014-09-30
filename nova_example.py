#!/usr/bin/python

import os
import sys
import argparse

from novaclient.v1_1 import client as novaclient

# Import code common to all of the examples.
import common
import keystone_example

def get_nova_client(keystone_client):
    # We pass username, password, and project_id as None
    # because we want to use our existing Keystone token rather
    # than having Nova acquire a new one.
    return novaclient.Client(
        None,
        None,
        None,
        auth_url=keystone_client.auth_url,
        tenant_id=keystone_client.tenant_id,
        auth_token=keystone_client.auth_token)


def parse_args():
    p = common.create_parser()
    p.add_argument('--all-tenants',
                   action='store_true')
    return p.parse_args()

def main():
    args = parse_args()

    kc = keystone_example.get_keystone_client(
        os_username=args.os_username,
        os_password=args.os_password,
        os_tenant_name=args.os_tenant_name,
        os_tenant_id=args.os_tenant_id,
        os_auth_url=args.os_auth_url
    )
    nc = get_nova_client(kc)

    # Print a list of running servers.
    for server in nc.servers.list(search_opts={'all_tenants':
                                               args.all_tenants}):
        print server.id, server.name
        for network_name, network in server.networks.items():
            print '    ', network_name, ', '.join(network)

if __name__ == '__main__':
    main()

