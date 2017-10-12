#!/usr/bin/env python

import mock
import unittest
from fakeldap import MockLDAP
from examlib.utils import LdapUtils


TEST_URL = "ldap://addressbook.ic.ac.uk"
TEST_BASE = "o=Imperial College,c=GB"
TEST_USER = "testuser"


class TestLdapDB(unittest.TestCase):

  TESTTREE = {
    'o=Imperial College,c=GB': {},
    'ou=test,o=Imperial College,c=GB': {},
    'uid=testuser,ou=test,o=Imperial College,c=GB': {
          'mail': 'test@user.test',
    },
  }

  LDAP = MockLDAP(TESTTREE)

  @staticmethod
  def __ldap__unbind(*args, **kwargs):
    return None

  @staticmethod
  def __ldap__search_st(base, scope,
                        filterstr='(objectClass=*)',
                        attrlist=None, attrsonly=0, timeout=-1):
    return TestLdapDB.LDAP.search_s(base, scope,
                                    filterstr, attrlist, attrsonly)

  LDAP.search_st = __ldap__search_st
  LDAP.unbind = __ldap__unbind


  def __init__(self, *args, **kwargs):
    super(TestLdapDB, self).__init__(*args, **kwargs)
    TestLdapDB.LDAP.search_st = self.__ldap__search_st
    TestLdapDB.LDAP.unbind = self.__ldap__unbind

  def setUp(self):
    self.__ldap_patcher = mock.patch('examlib.utils.LdapUtils.ldap.initialize')
    self.__ldap_patch = self.__ldap_patcher.start()
    self.__ldap_patch.return_value = TestLdapDB.LDAP

  def tearDown(self):
    self.__ldap_patcher.stop()
    TestLdapDB.LDAP.reset()

  def test_basic(self):
    x = LdapUtils.LdapDB(TEST_URL, TEST_BASE)
    # TODO: Make the test actually work
    assert(True)

