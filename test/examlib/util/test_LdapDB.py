#!/usr/bin/env python

from __future__ import print_function

import mock
import unittest
from mockldap.filter import parse
from examlib.utils import LdapUtils

import ldap


TEST_URL = "ldap://addressbook.ic.ac.uk"
TEST_BASE = "o=Test Org,c=GB"

TEST_DIR = {
  'uid=testuser,o=Test Org,c=GB':
    { 
      'objectClass': 'inetOrgPerson',
      'uid': 'testuser',
      'cn': 'test user',
      'givenName': 'test',
      'sn': 'user',
      'mail': 'test@test.test',
    },
  'uid=another,o=Test Org,c=GB':
    {
      'objectClass': 'inetOrgPerson',
      'uid': 'another',
      'cn': 'a. n. other',
      'givenName': 'an',
      'sn': 'other',
      'mail': 'otheruser@test.test',
    },
  'uid=dup1,o=Test Org,c=GB':
    {
      'objectClass': 'inetOrgPerson',
      'uid': 'dup1',
      'cn': 'duplicate user',
      'givenName': 'duplicate',
      'sn': 'user',
      'mail': 'dupuser@domain.test',
    },
  'uid=dup2,o=Test Org,c=GB':
    {
      'objectClass': 'inetOrgPerson',
      'uid': 'dup2',
      'cn': 'duplicate user',
      'givenName': 'duplicate',
      'sn': 'user',
      'mail': 'dupuser@other.test',
    },
  'uid=incomplete,o=Test Org,c=GB':
    {
      'objectClass': 'inetOrgPerson',
      'uid': 'incomplete',
      'mail': 'incomplete@test.test',
      # No other fields... User is incomplete.
    },
}


class FakeLdapInterface(object):

  def __filter_match(self, filterstr, dn, entry):
    filterbin = parse(filterstr)
    return filterbin.matches(dn, entry)

  def __entry_to_res(self, entry, attrs):
    res = {}
    search_attrs = attrs
    if not search_attrs:
      search_attrs = entry.keys()
    for attr in search_attrs:
      if attr in entry:
        if type(entry[attr]) == list:
          res[attr] = entry[attr]
        else:
          res[attr] = [entry[attr]]
    return res

  def simple_bind_s(self):
    return

  def search_st(self, basedn, scope, filterstr, attrs,
                attrs_only, timeout):
    assert(basedn == TEST_BASE)
    assert(scope == ldap.SCOPE_SUBTREE)
    assert(attrs_only == 0)
    assert(timeout > 0)
    # Now we have to do a minimal fake filter
    match_dns = []
    for key, entry in TEST_DIR.items():
      if self.__filter_match(filterstr, key, entry):
        match_dns.append(key)
    # Now handle attr filter
    res = []
    for dn in match_dns:
      res.append((dn, self.__entry_to_res(TEST_DIR[dn], attrs)))
    return res

  def unbind(self):
    return


class TestLdapDB(unittest.TestCase):

  def __init__(self, *args, **kwargs):
    super(TestLdapDB, self).__init__(*args, **kwargs)

  def setUp(self):
    self.__ldap_patcher = mock.patch('examlib.utils.LdapUtils.ldap.initialize')
    self.__ldap_patch = self.__ldap_patcher.start()
    self.__ldap_patch.return_value = FakeLdapInterface()
    self.__ldap_mod = LdapUtils.LdapDB(TEST_URL, TEST_BASE)

  def tearDown(self):
    self.__ldap_patcher.stop()

  def test_params(self):
    """ Check the parameters to the initialise call. """
    self.__ldap_patch.assert_called_once_with(TEST_URL)

  def test_basic(self):
    """ Check that we can find users using the basic functions. """
    # Find user by uid
    res = self.__ldap_mod.uid_to_user("testuser")
    assert(len(res) == 1)
    assert(res[0]['uid'] == "testuser")
    assert(res[0]['sn'] == "user")
    # Find user by name
    res = self.__ldap_mod.name_to_user('an', 'other')
    assert(len(res) == 1)
    assert(res[0]['uid'] == "another")
    assert(res[0]['mail'] == "otheruser@test.test")
    # Check things work if two people have the same name
    res = self.__ldap_mod.name_to_user('duplicate', 'user')
    assert(len(res) == 2)
    ## Order is not guarenteed!
    users = [res[0]['uid'], res[1]['uid']]
    assert("dup1" in users)
    assert("dup2" in users)
 
  def test_incomplete(self):
    """ Check that incomplete users don't throw exceptions. """
    res = self.__ldap_mod.uid_to_user("incomplete")
    assert(len(res) == 0)

