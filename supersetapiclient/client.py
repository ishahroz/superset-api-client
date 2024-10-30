"""A Superset REST API Client."""

import logging
from datetime import datetime

import jwt
import requests.adapters
import requests.exceptions
import requests_oauthlib

from supersetapiclient.assets import Assets
from supersetapiclient.base import raise_for_status
from supersetapiclient.charts import Charts
from supersetapiclient.css_templates import CssTemplates
from supersetapiclient.dashboards import Dashboards
from supersetapiclient.databases import Databases
from supersetapiclient.datasets import Datasets
from supersetapiclient.exceptions import QueryLimitReached
from supersetapiclient.saved_queries import SavedQueries

logger = logging.getLogger(__name__)


class SupersetClient:
    """A Superset Client."""

    assets_cls = Assets
    dashboards_cls = Dashboards
    charts_cls = Charts
    datasets_cls = Datasets
    databases_cls = Databases
    saved_queries_cls = SavedQueries
    css_templates_cls = CssTemplates
    http_adapter_cls = None

    def __init__(
        self,
        host,
        username=None,
        password=None,
        provider="db",
        verify=True,
        firstname="Superset",
        lastname="Admin",
    ):
        self.host = host
        self.base_url = self.join_urls(host, "api/v1")
        self.username = username
        self._password = password
        self.provider = provider
        if not verify:
            self.http_adapter_cls = NoVerifyHTTPAdapter
        self.firstname = firstname
        self.lastname = lastname

        # Related Objects
        self.assets = self.assets_cls(self)
        self.dashboards = self.dashboards_cls(self)
        self.charts = self.charts_cls(self)
        self.css_templates = self.css_templates_cls(self)
        self.datasets = self.datasets_cls(self)
        self.databases = self.databases_cls(self)
        self.saved_queries = self.saved_queries_cls(self)

        # Session Management
        self._session = None

    # Private Methods
    @property
    def _token(self):
        """Get the tokens."""
        if not (self._access_token and self._refresh_token):
            self._authenticate()
        return {
            "access_token": self._access_token,
            "refresh_token": self._refresh_token,
        }

    def _authenticate(self) -> dict:
        """Authenticate and return the tokens."""
        # No need for session here because we are before authentication
        response = requests.post(
            self.login_endpoint,
            json={
                "username": self.username,
                "password": self._password,
                "provider": self.provider,
                "refresh": "true",
            },
        )
        raise_for_status(response)
        self._access_token, self._refresh_token = (
            response.json()["access_token"],
            response.json()["refresh_token"],
        )

    def _create_session(self):
        """Create and store a new session."""
        self._access_token, self._refresh_token = None, None
        self._session = requests_oauthlib.OAuth2Session(token=self._token)
        if self.http_adapter_cls:
            self._session.mount(self.host, adapter=self.http_adapter_cls())
        self._session.headers.update(
            {
                "X-CSRFToken": f"{self._csrf_token(self._session)}",
                "Referer": f"{self.base_url}",
            }
        )

    def _csrf_token(self, session) -> str:
        """Get the CSRF token."""
        csrf_response = session.get(
            self.csrf_token_endpoint,
            headers={"Referer": f"{self.base_url}"},
        )
        raise_for_status(csrf_response)  # Check CSRF Token went well
        return csrf_response.json().get("result")

    def _refresh_access_token(self):
        """Refresh the access token."""
        # Create a new session to avoid messing up the current session
        refresh_r = requests_oauthlib.OAuth2Session(
            token={"access_token": self._refresh_token}
        ).post(self.refresh_endpoint)
        raise_for_status(refresh_r)
        new_token = refresh_r.json()
        if "refresh_token" not in new_token:
            new_token["refresh_token"] = self._refresh_token
        self._access_token, self._refresh_token = (
            new_token["access_token"],
            new_token["refresh_token"],
        )
        self._session.token = new_token

    def _refresh_csrf_token(self):
        """Refresh the CSRF token."""
        self._session.headers["X-CSRFToken"] = f"{self._csrf_token(self._session)}"

    # Public Methods
    @property
    def session(self):
        """Get or create a session, checking token expiry."""
        if self._session is None:
            self._create_session()
            return self._session

        try:
            now = datetime.now().timestamp()
            # Decode tokens to get their expiry times without verifying signatures
            tokens = {
                "access": jwt.decode(
                    self._access_token, options={"verify_signature": False}
                )["exp"],
                "refresh": jwt.decode(
                    self._refresh_token, options={"verify_signature": False}
                )["exp"],
            }

            # Check if the refresh token has expired and create a new session if so
            if now >= tokens["refresh"]:
                self._create_session()
            # Check if the access token has expired and refresh it if so
            elif now >= tokens["access"]:
                self._refresh_access_token()
                self._refresh_csrf_token()
        except jwt.InvalidTokenError:
            self._create_session()

        return self._session

    @property
    def get(self):
        """Get a resource."""
        return self.session.get

    @property
    def post(self):
        """Post a resource."""
        return self.session.post

    @property
    def put(self):
        """Put a resource."""
        return self.session.put

    @property
    def delete(self):
        """Delete a resource."""
        return self.session.delete

    @staticmethod
    def join_urls(*args) -> str:
        """Join multiple url parts together.

        Returns:
            str: joined urls

        """
        parts = [str(part).strip("/") for part in args]
        if str(args[-1]).endswith("/"):
            parts.append("")  # Preserve trailing slash
        return "/".join(parts)

    def run(self, database_id, query, query_limit=None):
        """Send SQL queries to Superset and returns the resulting dataset.

        :param database_id: Database ID of DB to query
        :type database_id: int
        :param query: Valid SQL Query
        :type query: str
        :param query_limit: limit size of resultset, defaults to -1
        :type query_limit: int, optional
        :raises Exception: Query exception
        :return: Resultset
        :rtype: tuple(dict)
        """
        payload = {
            "database_id": database_id,
            "sql": query,
        }
        if query_limit:
            payload["queryLimit"] = query_limit
        response = self.post(self._sql_endpoint, json=payload)
        raise_for_status(response)
        result = response.json()
        display_limit = result.get("displayLimit", None)
        display_limit_reached = result.get("displayLimitReached", False)
        if display_limit_reached:
            raise QueryLimitReached(
                f"You have exceeded the maximum number of rows that can be "
                f"returned ({display_limit}). Either set the `query_limit` "
                f"attribute to a lower number than this, or add LIMIT "
                f"keywords to your SQL statement to limit the number of rows "
                f"returned."
            )
        return result["columns"], result["data"]

    @property
    def password(self) -> str:
        """Get the password."""
        return "*" * len(self._password)

    @property
    def login_endpoint(self) -> str:
        """Get the login endpoint."""
        return self.join_urls(self.base_url, "security/login")

    @property
    def refresh_endpoint(self) -> str:
        """Get the refresh endpoint."""
        return self.join_urls(self.base_url, "security/refresh")

    @property
    def guest_token_endpoint(self) -> str:
        """Get the guest token endpoint."""
        return self.join_urls(self.base_url, "security/guest_token/")

    @property
    def _sql_endpoint(self) -> str:
        return self.join_urls(self.host, "superset/sql_json/")

    @property
    def csrf_token_endpoint(self) -> str:
        """Get the CSRF token endpoint."""
        return self.join_urls(self.base_url, "security/csrf_token/")

    def guest_token(self, uuid: str) -> str:
        """Retrieve a guest token from the Superset API.

        :param uuid: The UUID of the resource (e.g., dashboard).
        :type uuid: str
        :return: Guest token as a dictionary.
        """
        # Construct the request body
        request_body = {
            "resources": [{"id": uuid, "type": "dashboard"}],
            "rls": [],
            "user": {
                "first_name": self.firstname,
                "last_name": self.lastname,
                "username": self.username,
            },
        }

        response = self.post(self.guest_token_endpoint, json=request_body)
        raise_for_status(response)  # Check for errors in the response
        return response.json().get("token")


class NoVerifyHTTPAdapter(requests.adapters.HTTPAdapter):
    """An HTTP adapter that ignores TLS validation errors."""

    def cert_verify(self, conn, url, verify, cert):
        """Verify the certificate."""
        super().cert_verify(conn=conn, url=url, verify=False, cert=cert)
