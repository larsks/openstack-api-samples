#!/usr/bin/python

import os
import sys
import argparse

import keystoneclient.v2_0.client as ksclient

def parse_args():
    p = argparse.ArgumentParser()
    return p.parse_args()

def main():
    args = parse_args()

    os_username = os.environ['OS_USERNAME']
    os_password = os.environ['OS_PASSWORD']
    os_tenant_id = os.environ.get('OS_TENANT_ID')
    os_tenant_name = os.environ.get('OS_TENANT_NAME')
    os_auth_url = os.environ['OS_AUTH_URL']

    client = ksclient.Client(username=os_username, 
                               password=os_password,
                               tenant_name=os_tenant_name,
                               tenant_id=os_tenant_id,
                               auth_url=os_auth_url)
     
    for endpoint_type, endpoints in client.service_catalog.get_endpoints().items():
        print endpoint_type
        for i, endpoint in enumerate(endpoints):
            for url in ['adminURL', 'internalURL', 'publicURL']:
                print '    ', i, url, endpoint[url]


if __name__ == '__main__':
    main()

 
