#!/usr/bin/python

import os
import sys
import argparse

def create_parser():
    p = argparse.ArgumentParser()

    p.add_argument('--os-username',
                   default=os.environ.get('OS_USERNAME'))
    p.add_argument('--os-password',
                   default=os.environ.get('OS_PASSWORD'))
    p.add_argument('--os-tenant-name',
                   default=os.environ.get('OS_TENANT_NAME'))
    p.add_argument('--os-tenant-id',
                   default=os.environ.get('OS_TENANT_ID'))
    p.add_argument('--os-region-name',
                   default=os.environ.get('OS_REGION_NAME'))
    p.add_argument('--os-auth-url',
                   default=os.environ.get('OS_AUTH_URL'))

    return p

