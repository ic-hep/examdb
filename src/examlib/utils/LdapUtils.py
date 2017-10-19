#!/usr/bin/env python
""" A module for interacting with an LDAP addressbooks.
"""

from __future__ import print_function

import ldap
import ldap.filter


class LdapDB(object):
    """ A Caching LDAP Database object. """

    def __init__(self, url, basedn, timeout=15):
        """ Connect to the LDAP server
            url - The ldap style URL to connect to (ldap://...).
            basedn - The Base DN of the server.
            timeout - Number of seconds to wait for queries to return.
        """
        self.__conn = None
        self.__basedn = basedn
        self.__timeout = timeout
        # Now connect & bind
        self.__conn = ldap.initialize(url)
        self.__conn.simple_bind_s()

    def __del__(self):
        """ Close LDAP server connection. """
        if self.__conn:
            self.__conn.unbind()
            self.__conn = None

    def __run_query(self, filterstr):
        fullfilter = "(&(objectClass=inetOrgPerson)(%s))" % filterstr
        attrs = ['uid', 'cn', 'sn', 'givenName', 'mail']
        users = []
        try:
            results = self.__conn.search_st(self.__basedn,       # Base
                                            ldap.SCOPE_SUBTREE,  # Scope
                                            fullfilter,          # Filter
                                            attrs,               # Attributes
                                            0,                   # Attrs only
                                            self.__timeout)      # Timeout
            for _, details in results:
                # LDAP returns a list of values,
                # These items should only have one element
                bad_user = False
                user = {}
                for attr in attrs:
                    if not attr in details:
                        # User is incomplete, skip them
                        bad_user = True
                        break
                    else:
                        user[attr] = details[attr][0]
                if not bad_user:
                    users.append(user)
        except ldap.LDAPError:
            # TODO: Do something else here? Log error?
            raise
        return users

    def uid_to_user(self, uid):
        """ Find a user by user id (aka username).
            uid - The username to search for.
            Returns a list of dictionaries, one entry for each user found,
            keys are uid, cn, sn, givenName and mail.
        """
        safeuid = ldap.filter.escape_filter_chars(uid, escape_mode=1)
        filterstr = 'uid=%s' % safeuid
        return self.__run_query(filterstr)

    def name_to_user(self, given_name, surname):
        """ Find a user by first & last name.
            given_name - The first name to search for.
            surname - The last name to search for.
            Returns a list of dictionaries, one entry for each user found,
            keys are uid, cn, sn, givenName and mail.
        """
        safe_gn = ldap.filter.escape_filter_chars(given_name, escape_mode=1)
        safe_sn = ldap.filter.escape_filter_chars(surname, escape_mode=1)
        filterstr = '&(givenName=%s)(sn=%s)' % (safe_gn, safe_sn)
        return self.__run_query(filterstr)
