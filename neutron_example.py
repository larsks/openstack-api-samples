#!/usr/bin/python

import os
import sys
import argparse

from neutronclient.common.exceptions import *
import neutronclient.v2_0.client as neutronclient

# Import code common to all of the examples.
import common
import keystone_example

def parse_args():
    p = common.create_parser()
    return p.parse_args()

def main():
    args = parse_args()
    kc = keystone_example.get_keystone_client(args)

    # Find an endpoint for the 'image' service.
    endpoint = kc.service_catalog.url_for(
        service_type='network',
        endpoint_type='publicURL')

    # Authenticate to neutron using our Keystone token.
    nc = neutronclient.Client(
        endpoint_url=endpoint,
        token=kc.auth_token,
        tenant_id=args.os_tenant_id,
        auth_url=args.os_auth_url)

    networks = nc.list_networks()
    for network in networks.get('networks', []):
        print network['id'], network['name']
        for subnet in network['subnets']:
            try:
                data = nc.show_subnet(subnet)
                print '    ', subnet, data['subnet']['cidr']
            except NeutronClientException:
                print '    ', subnet, 'not found'


if __name__ == '__main__':
    main()

