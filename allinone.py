#!/usr/bin/python

import logging
import os

import keystoneclient.auth as keystone_auth
import keystoneclient.auth.identity as keystone_identity
import keystoneclient.session as keystone_session
import keystoneclient.client as keystone_client
import novaclient.client as nova_client
import glanceclient.client as glance_client
import cinderclient.client as cinder_client
import neutronclient.neutron.client as neutron_client
import heatclient.client as heat_client

LOG = logging.getLogger(__name__)


class OpenStack(object):
    def __init__(self,
                 sess=None,
                 identity_api_version=None,
                 username=None,
                 password=None,
                 tenant_name=None,
                 tenant_id=None,
                 user_domain_id=None,
                 project_domain_id=None,
                 auth_url=None):

        self.username = username or os.environ.get('OS_USERNAME')
        self.password = password or os.environ.get('OS_PASSWORD')
        self.tenant_name = tenant_name or os.environ.get('OS_TENANT_NAME')
        self.tenant_id = tenant_id or os.environ.get('OS_TENANT_ID')
        self.user_domain_id = (
            user_domain_id or os.environ.get('OS_USER_DOMAIN_ID',
                                             'default'))
        self.project_domain_id = (
            project_domain_id or os.environ.get('OS_PROJECT_DOMAIN_ID',
                                                'default'))
        self.auth_url = (
            auth_url if auth_url else os.environ.get('OS_AUTH_URL'))

        self.identity_api_version = (
            identity_api_version if identity_api_version
            else os.environ.get('OS_IDENTITY_API_VERSION'))

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
            username=self.username,
            password=self.password,
            tenant_name=self.tenant_name,
            tenant_id=self.tenant_id)

    def get_keystone_v3_auth(self):
        return keystone_identity.v3.Password(
            auth_url=self.auth_url,
            username=self.username,
            password=self.password,
            user_domain_id=self.user_domain_id,
            project_name=self.tenant_name,
            project_id=self.tenant_id,
            project_domain_id=self.project_domain_id)

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

    def get_heat_client(self):
        # XXX (Lars Kellogg-Stedman): Why is it necessary to specify
        # service_type here? Heat should already know it is the
        # orchestration service.
        return heat_client.Client(
            '1', service_type='orchestration',
            session=self.sess,
            endpoint=self.keystone.service_catalog.url_for(
                service_type='orchestration',
                endpoint_type='publicURL'))

    @property
    def token(self):
        return self.sess.get_token()

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

    @property
    def heat(self):
        try:
            return self._heat
        except AttributeError:
            self._heat = self.get_heat_client()
            return self._heat


if __name__ == '__main__':
    logging.basicConfig(level='DEBUG')
    clients = OpenStack()
