from typing import List

# noinspection PyPackageRequirements
import ldap


def parse_domain_from_dn(dn: str, base_dn: str) -> str:
    patched_dn = ','.join([item for item in dn.split(',') if item.startswith('DC=')])
    patched_dn = patched_dn.replace(base_dn, '').strip(',')
    return patched_dn.split('=')[1]


class LdapError(Exception):
    pass


class LdapManager:
    """LDAP authenticator using python-ldap module"""

    def __init__(self, ldap_server_uri, ldap_bind_dn, ldap_bind_password, ldap_user_search_base,
                 ldap_user_search_criteria, ldap_allowed_groups):
        self.ldap_server_uri = ldap_server_uri
        self.ldap_bind_dn = ldap_bind_dn
        self.ldap_bind_password = ldap_bind_password
        self.ldap_user_search_base = ldap_user_search_base
        self.ldap_user_search_criteria = ldap_user_search_criteria
        self.ldap_allowed_groups = ldap_allowed_groups

    def login(self, username: str, password: str):
        connection = None

        try:
            ad_results = self._ad_search(self.ldap_user_search_base, self.ldap_user_search_criteria % username)
            if len(ad_results) == 0:
                raise LdapError("Unknown user")

            elif len(ad_results) > 1:
                raise LdapError("Multiple users with this username found")

            connection = self._ad_connection()
            domain = parse_domain_from_dn(ad_results[0][0], self.ldap_user_search_base)
            connection.simple_bind_s(f"{domain}\\{username}", password)

            groups = [item.decode("utf-8") for item in ad_results[0][1].get('memberOf', [])]
            if self.ldap_allowed_groups and not self._has_valid_groups(groups):
                raise LdapError("User not allowed to connect")

            return {
                'name': ad_results[0][1]['cn'][0].decode("utf-8"),
                'dn': ad_results[0][0],
            }

        except ldap.INVALID_CREDENTIALS:
            raise LdapError("Invalid credentials")

        except ldap.SERVER_DOWN:
            raise LdapError("Unable to connect to LDAP server")

        finally:
            if connection:
                connection.unbind()

    def _has_valid_groups(self, user_groups: List[str]) -> bool:
        if not user_groups:
            return False

        for grp in self.ldap_allowed_groups:
            if grp in user_groups:
                return True

        return False

    def _ad_connection(self):
        connection = ldap.initialize(self.ldap_server_uri)

        connection.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, 0)
        connection.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
        connection.set_option(ldap.OPT_REFERRALS, 0)
        connection.set_option(ldap.OPT_X_TLS_NEWCTX, 0)

        return connection

    def _ad_search(self, base_dn: str, criteria: str):
        connection = None

        try:
            connection = self._ad_connection()
            connection.simple_bind_s(self.ldap_bind_dn, self.ldap_bind_password)
            return connection.search_s(base_dn, ldap.SCOPE_SUBTREE, criteria)

        except ldap.SERVER_DOWN:
            raise LdapError("Unable to connect to LDAP server")

        finally:
            if connection:
                connection.unbind()
