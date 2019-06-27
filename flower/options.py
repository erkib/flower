from __future__ import absolute_import

import types

from tornado.options import define
from tornado.options import options

DEFAULT_CONFIG_FILE = 'flowerconfig.py'


define("port", default=5555,
       help="run on the given port", type=int)
define("address", default='',
       help="run on the given address", type=str)
define("unix_socket", default='',
       help="path to unix socket to bind", type=str)
define("debug", default=False,
       help="run in debug mode", type=bool)
define("inspect_timeout", default=1000, type=float,
       help="inspect timeout (in milliseconds)")
define("auth", default='', type=str,
       help="regexp of emails to grant access")
define("basic_auth", type=str, default=None, multiple=True,
       help="enable http basic authentication")
define("oauth2_key", type=str, default=None,
       help="OAuth2 key (requires --auth)")
define("oauth2_secret", type=str, default=None,
       help="OAuth2 secret (requires --auth)")
define("oauth2_redirect_uri", type=str, default=None,
       help="OAuth2 redirect uri (requires --auth)")
define("max_workers", type=int, default=5000,
       help="maximum number of workers to keep in memory")
define("max_tasks", type=int, default=10000,
       help="maximum number of tasks to keep in memory")
define("db", type=str, default='flower',
       help="flower database file")
define("persistent", type=bool, default=False,
       help="enable persistent mode")
define("broker_api", type=str, default=None,
       help="inspect broker e.g. http://guest:guest@localhost:15672/api/")
define("ca_certs", type=str, default=None,
       help="SSL certificate authority (CA) file")
define("certfile", type=str, default=None,
       help="SSL certificate file")
define("keyfile", type=str, default=None,
       help="SSL key file")
define("xheaders", type=bool, default=False,
       help="enable support for the 'X-Real-Ip' and 'X-Scheme' headers.")
define("auto_refresh", default=True,
       help="refresh dashboards", type=bool)
define("cookie_secret", type=str, default=None,
       help="secure cookie secret")
define("conf", default=DEFAULT_CONFIG_FILE,
       help="configuration file")
define("enable_events", type=bool, default=True,
       help="periodically enable Celery events")
define("format_task", type=types.FunctionType, default=None,
       help="use custom task formatter")
define("natural_time", type=bool, default=False,
       help="show time in relative format")
define("tasks_columns", type=str,
       default="name,uuid,state,args,kwargs,result,received,started,runtime,worker",
       help="slugs of columns on /tasks/ page, delimited by comma")
define("auth_provider", default='flower.views.auth.GoogleAuth2LoginHandler',
       help="auth handler class")
define("url_prefix", type=str, help="base url prefix")
define("ldap_server_uri", type=str, default=None, help="ldap server uri")
define("ldap_bind_dn", type=str, default=None, help="ldap user for searching")
define("ldap_bind_password", type=str, default=None, help="ldap user password for searching")
define("ldap_user_search_base", type=str, default=None, help="ldap base DN for user searching")
define("ldap_user_search_criteria", type=str, default=None, help="ldap criteria for user searching")
define("ldap_allowed_groups", type=list, default=[], help="ldap allowed groups DN-s to login")

# deprecated options
define("inspect", default=False, help="inspect workers", type=bool)

default_options = options
