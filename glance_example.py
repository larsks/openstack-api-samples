#!/usr/bin/python

import os
import sys
import argparse

from glanceclient.v2 import client as glanceclient

# Import code common to all of the examples.
import common
import keystone_example

def parse_args():
    p = common.create_parser()
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

    # Find an endpoint for the 'image' service.
    endpoint = kc.service_catalog.url_for(
        service_type='image',
        endpoint_type='publicURL')

    # Authenticate to glance using our Keystone token.
    gc = glanceclient.Client(
        endpoint=endpoint,
        token=kc.auth_token)

    # Print information about available images.
    for image in gc.images.list():
        print image['id'], image['name'], image['disk_format']

if __name__ == '__main__':
    main()

