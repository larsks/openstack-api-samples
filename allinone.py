#!/usr/bin/python

import logging
import os
import sys

import keystoneclient.auth.identity as keystone_identity
import keystoneclient.session as keystone_session
import keystoneclient.client as keystone_client
import novaclient.client as nova_client
import glanceclient.client as glance_client
import cinderclient.client as cinder_client

LOG = logging.getLogger(__name__)

logging.basicConfig(level='INFO')

IDENTITY_API_VERSION = os.environ.get(
    'OS_IDENTITY_API_VERSION', '3')


def get_keystone_v2_auth():
    return keystone_identity.v2.Password(
        auth_url=os.environ['OS_AUTH_URL'],
        username=os.environ['OS_USERNAME'],
        password=os.environ['OS_PASSWORD'],
        tenant_name=os.environ['OS_TENANT_NAME'])


def get_keystone_v3_auth():
    return keystone_identity.v3.Password(
        auth_url=os.environ['OS_AUTH_URL'],
        username=os.environ['OS_USERNAME'],
        password=os.environ['OS_PASSWORD'],
        user_domain_id=os.environ.get('OS_USER_DOMAIN_ID',
                                      'default'),
        project_name=os.environ['OS_TENANT_NAME'],
        project_domain_id=os.environ.get('OS_PROJECT_DOMAIN_ID',
                                         'default'),
    )


def get_session(auth=None, identity_api_version=IDENTITY_API_VERSION):
    if auth is None:
        if identity_api_version == '3':
            LOG.info('using keystone v3 api')
            auth = get_keystone_v3_auth()
        else:
            LOG.info('using keystone v2 api')
            auth = get_keystone_v2_auth()

    # establish a keystone session
    sess = keystone_session.Session(auth=auth)

    return sess


def get_keystone_client(sess, identity_api_version=IDENTITY_API_VERSION):
    kc = keystone_client.Client(identity_api_version,
                                session=sess,
                                project_id=sess.get_project_id(),
                                tenant_id=sess.get_project_id(),
                                auth_url=sess.auth.auth_url)

    kc.authenticate(token=sess.get_token())

    return kc


def get_nova_client(sess):
    return nova_client.Client('2', session=sess)


def get_glance_client(sess):
    kc = get_keystone_client(sess)

    return glance_client.Client(
        '2', endpoint=kc.service_catalog.url_for(
            service_type='image',
            endpoint_type='publicURL'),
        token=sess.get_token())


def get_cinder_client(sess):
    return cinder_client.Client('2', session=sess)

sess = get_session()
kc = get_keystone_client(sess)
nc = get_nova_client(sess)
gc = get_glance_client(sess)
cc = get_cinder_client(sess)
