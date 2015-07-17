#!/usr/bin/python

import logging
import os
import sys

import keystoneclient.auth as keystone_auth
import keystoneclient.auth.identity as keystone_identity
import keystoneclient.session as keystone_session
import keystoneclient.client as keystone_client
import novaclient.client as nova_client
import glanceclient.client as glance_client
import cinderclient.client as cinder_client
import neutronclient.neutron.client as neutron_client

LOG = logging.getLogger(__name__)

logging.basicConfig(level='INFO')

IDENTITY_API_VERSION = os.environ.get(
    'OS_IDENTITY_API_VERSION', '3')

class OpenStack(object):
    def __init__(self,
                 sess=None,
                 identity_api_version=None,
                 auth_url=None):

        self.auth_url = (
            auth_url if auth_url
            else os.environ.get('OS_AUTH_URL'))
        self.identity_api_version = identity_api_version
        self.sess = sess or self.get_session()

    def get_session(self):
        if self.auth_url is None:
            raise ValueError('Missing auth_url')

        if self.identity_api_version is None:
            self.identity_api_version = (
                '2' if 'v2.0' in self.auth_url
                else '3')

        if self.identity_api_version == '3':
            LOG.info('using keystone v3 api')
            auth = self.get_keystone_v3_auth()
        else:
            LOG.info('using keystone v2 api')
            auth = self.get_keystone_v2_auth()

        # establish a keystone session
        sess = keystone_session.Session(auth=auth)

        return sess

    def get_keystone_v2_auth(self):
        return keystone_identity.v2.Password(
            auth_url=self.auth_url,
            username=os.environ['OS_USERNAME'],
            password=os.environ['OS_PASSWORD'],
            tenant_name=os.environ['OS_TENANT_NAME'])

    def get_keystone_v3_auth(self):
        return keystone_identity.v3.Password(
            auth_url=self.auth_url,
            username=os.environ['OS_USERNAME'],
            password=os.environ['OS_PASSWORD'],
            user_domain_id=os.environ.get('OS_USER_DOMAIN_ID',
                                          'default'),
            project_name=os.environ['OS_TENANT_NAME'],
            project_domain_id=os.environ.get('OS_PROJECT_DOMAIN_ID',
                                             'default'),
        )

    def get_keystone_client(self):
        kc = keystone_client.Client(
            self.identity_api_version,
            session=self.sess,
            project_id=self.sess.get_project_id(),
            tenant_id=self.sess.get_project_id(),
            auth_url=self.sess.get_endpoint(
                interface=keystone_auth.AUTH_INTERFACE))

        kc.authenticate(token=self.sess.get_token())

        return kc

    def get_nova_client(self):
        return nova_client.Client('2', session=self.sess)

    def get_glance_client(self):
        return glance_client.Client(
            '2', endpoint=self.keystone.service_catalog.url_for(
                service_type='image',
                endpoint_type='publicURL'),
            token=self.sess.get_token())

    def get_cinder_client(self):
        return cinder_client.Client('2', session=self.sess)

    def get_neutron_client(self):
        return neutron_client.Client('2.0', session=self.sess)

    @property
    def keystone(self):
        try:
            return self._keystone
        except AttributeError:
            self._keystone = self.get_keystone_client()
            return self._keystone

    @property
    def nova(self):
        try:
            return self._nova
        except AttributeError:
            self._nova = self.get_nova_client()
            return self._nova

    @property
    def glance(self):
        try:
            return self._glance
        except AttributeError:
            self._glance = self.get_glance_client()
            return self._glance

    @property
    def cinder(self):
        try:
            return self._cinder
        except AttributeError:
            self._cinder = self.get_cinder_client()
            return self._cinder

    @property
    def neutron(self):
        try:
            return self._neutron
        except AttributeError:
            self._neutron = self.get_neutron_client()
            return self._neutron


if __name__ == '__main__':
    clients = OpenStack()
