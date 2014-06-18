#!/usr/bin/python

import os
import sys
import argparse

import keystoneclient.v2_0.client as ksclient

# Import code common to all of the examples.
import common

def get_keystone_client(args):
    '''Returns a keystone client.  Other examples that need an
    authenticated keystone client can simply:

        import common
        import keystone_example
        parser = common.create_parser()
        args = parser.parse_args()
        client = keystone_example.get_keystone_client(args)
    '''

    return ksclient.Client(username=args.os_username, 
                           password=args.os_password,
                           tenant_name=args.os_tenant_name,
                           tenant_id=args.os_tenant_id,
                           auth_url=args.os_auth_url)
     


def parse_args():
    p = common.create_parser()
    return p.parse_args()

def main():
    args = parse_args()
    client = get_keystone_client(args)

    # Iterate through the service catalog and display all endpoint
    # URLs for all services.
    for endpoint_type, endpoints in client.service_catalog.get_endpoints().items():
        print endpoint_type
        for i, endpoint in enumerate(endpoints):
            for url in ['adminURL', 'internalURL', 'publicURL']:
                print '    ', i, url, endpoint[url]


if __name__ == '__main__':
    main()

 
