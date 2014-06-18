#!/usr/bin/python

import os
import sys
import argparse

from cinderclient.v2 import client as cinderclient

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
        service_type='volume',
        endpoint_type='publicURL')

    # The cinder library does not appear to know how to make use
    # of an existing Keystone auth_token, so we need to provide it with a
    # username and password.
    cc = cinderclient.Client(
        args.os_username,
        args.os_password,
        None,
        auth_url=args.os_auth_url,
        tenant_id=args.os_tenant_id)

    # Print information about available volumes.
    for volume in cc.volumes.list():
        print volume.id, volume.name, volume.size

if __name__ == '__main__':
    main()

