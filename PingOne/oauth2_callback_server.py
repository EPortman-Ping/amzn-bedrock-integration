"""
OAuth2 Callback Server for Amazon Bedrock AgentCore Identity.

This module implements a local callback server that handles OAuth2 authorization code flows.
It serves as an intermediary between the user's browser, the identity provider (e.g., PingOne),
and AgentCore Identity during local development and testing.
"""

import time
import argparse
import logging
from typing import Annotated, Optional
from datetime import datetime, timedelta, timezone

import uvicorn
import requests
from fastapi import Cookie, FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from bedrock_agentcore.services.identity import IdentityClient, UserIdIdentifier


# Configuration constants
OAUTH2_CALLBACK_SERVER_PORT = 9090
PING_ENDPOINT = '/ping'
OAUTH2_CALLBACK_ENDPOINT = '/oauth2/callback'
USER_IDENTIFIER_ENDPOINT = '/userIdentifier/userId'

logger = logging.getLogger(__name__)


class OAuth2CallbackServer:
    """Local server that captures OAuth2 authorization codes and completes token exchange."""

    def __init__(self, region: str):
        self.identity_client = IdentityClient(region=region)
        self.user_id_identifier: Optional[UserIdIdentifier] = None
        self.app = FastAPI()
        self._setup_routes()

    def _setup_routes(self):
        @self.app.get(PING_ENDPOINT)
        async def _handle_ping() -> JSONResponse:
            """Health check endpoint."""
            return JSONResponse(status_code=200, content={'status': 'success'})

        @self.app.post(USER_IDENTIFIER_ENDPOINT)
        async def _store_user_id(user_id_val: UserIdIdentifier) -> JSONResponse:
            """Store the user identity before the OAuth flow starts (session binding)."""
            if not user_id_val:
                raise HTTPException(status_code=400, detail='Missing user_identifier')

            self.user_id_identifier = user_id_val
            response = JSONResponse(status_code=200, content={'status': 'success'})

            # Set a secure cookie for session binding
            response.set_cookie(
                key='user_id_identifier',
                value=user_id_val.user_id,
                secure=True,
                httponly=True,
                expires=datetime.now(timezone.utc) + timedelta(hours=1),
            )
            return response

        @self.app.get(OAUTH2_CALLBACK_ENDPOINT)
        async def _handle_oauth2_callback(
            session_id: str,
            user_id_cookie: Annotated[str | None, Cookie(alias='user_id_identifier')] = None
        ) -> HTMLResponse:
            """Handle the redirect from the identity provider and complete token exchange."""
            if not session_id:
                raise HTTPException(status_code=400, detail='Missing session_id')

            # Priority: cookie first, then in-memory
            user_id = user_id_cookie or (
                self.user_id_identifier.user_id if self.user_id_identifier else None
            )

            if not user_id:
                logger.error('No user identity found for session binding')
                raise HTTPException(status_code=400, detail='User session not found')

            # Complete the token exchange with AgentCore Identity
            self.identity_client.complete_resource_token_auth(
                session_uri=session_id,
                user_identifier=UserIdIdentifier(user_id=user_id)
            )

            return HTMLResponse(content='''
                <html>
                <body style="font-family: Arial, sans-serif; text-align: center; padding-top: 100px; background-color: #f8f9fa;">
                    <div style="display: inline-block; padding: 40px; background: white; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                        <h1 style="color: #28a745;">Success!</h1>
                        <p style="font-size: 18px; color: #555;">Authorization complete.</p>
                        <p style="color: #888;">You can close this window and return to your notebook.</p>
                    </div>
                </body>
                </html>
            ''')


def get_oauth2_callback_url() -> str:
    """Returns the local callback URL for OAuth2 redirect configuration."""
    return f'http://localhost:{OAUTH2_CALLBACK_SERVER_PORT}{OAUTH2_CALLBACK_ENDPOINT}'


def store_user_id_in_oauth2_callback_server(user_id: str):
    """Register the user with the callback server before starting the OAuth flow."""
    requests.post(
        f'http://localhost:{OAUTH2_CALLBACK_SERVER_PORT}{USER_IDENTIFIER_ENDPOINT}',
        json={'user_id': user_id},
        timeout=5
    ).raise_for_status()


def wait_for_oauth2_server_to_be_ready(timeout: int = 30) -> bool:
    """Poll the ping endpoint until the server is ready."""
    start = time.time()
    while time.time() - start < timeout:
        try:
            resp = requests.get(
                f'http://localhost:{OAUTH2_CALLBACK_SERVER_PORT}{PING_ENDPOINT}',
                timeout=2
            )
            if resp.status_code == 200:
                return True
        except requests.RequestException:
            pass
        time.sleep(1)
    return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='OAuth2 Callback Server for AgentCore Identity')
    parser.add_argument('--region', required=True, help='AWS region for AgentCore Identity')
    args = parser.parse_args()

    server = OAuth2CallbackServer(region=args.region)
    uvicorn.run(server.app, host='127.0.0.1', port=OAUTH2_CALLBACK_SERVER_PORT)
