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
    kc = keystone_example.get_keystone_client(args)

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


