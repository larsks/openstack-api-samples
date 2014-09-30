#!/usr/bin/python

import os
import sys
import argparse
import logging

from ceilometerclient.client import get_client

# Import code common to all of the examples.
import common
import keystone_example


def get_ceilometer_client(keystone_client):
    # Find an endpoint for the 'image' service.
    endpoint = keystone_client.service_catalog.url_for(
        service_type='metering',
        endpoint_type='publicURL')

    # Authenticate to neutron using our Keystone token.
    cc = get_client(2,
        ceilometer_url=endpoint,
        os_auth_token=keystone_client.auth_token,
        tenant_id=keystone_client.tenant_id,
        auth_url=keystone_client.auth_url)

    return cc

def parse_args():
    p = common.create_parser()
    return p.parse_args()

def main():
    logging.basicConfig(level=logging.DEBUG)

    args = parse_args()
    kc = keystone_example.get_keystone_client(
        os_username=args.os_username,
        os_password=args.os_password,
        os_tenant_name=args.os_tenant_name,
        os_tenant_id=args.os_tenant_id,
        os_auth_url=args.os_auth_url
    )

    # Authenticate to neutron using our Keystone token.
    cc = get_ceilometer_client(kc)
    import pprint
    for sample in cc.samples.list(meter_name='cpu_util', limit=10):
        print sample.timestamp, sample.counter_name, sample.counter_volume

if __name__ == '__main__':
    main()

