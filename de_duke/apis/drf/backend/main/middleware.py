from channels.auth import AuthMiddlewareStack
from django.contrib.auth.models import AnonymousUser
from urllib.parse import parse_qs
from rest_framework_simplejwt.tokens import AccessToken, UntypedToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model


@database_sync_to_async
def get_user_from_token(token_key):
    try:
        access_token = AccessToken(token_key)
        user_id = access_token.get("user_id")
        return get_user_model().objects.get(id=user_id)
    except (InvalidToken, TokenError) as e:
        print("Invalid token: ", e)
        return None


class TokenAuthMiddleware:
    """
    Custom middleware that takes a token from the query string and authenticates the user.
    """

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        # Parse the query string to extract the 'token' parameter
        query_params = parse_qs(scope["query_string"].decode())
        token_key = query_params.get("token", [None])[0]
        # try to authenticate the user asynchronously
        user = await get_user_from_token(token_key)
        if user:
            scope["user"] = user
        else:
            # If no token, set the user to AnonymousUser
            scope["user"] = AnonymousUser()

        # Call the next middleware in the stack
        return await self.inner(scope, receive, send)


# Helper function to get the full middleware stack
def TokenAuthMiddlewareStack(inner):
    return TokenAuthMiddleware(AuthMiddlewareStack(inner))
