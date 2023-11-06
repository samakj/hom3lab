from typing import Optional
from fastapi import Depends, HTTPException, Query, Request

from auth.bearer_user import BearerUser
from stores.users import UsersStore, users_store
from stores.sessions import SessionsStore, sessions_store
from shared.python.models.authorisation import PermissionCredentials


class BearerPermission(BearerUser):
    scope: str

    def __init__(self, scope: str):
        super().__init__()
        self.scope = scope

    async def __call__(
        self,
        request: Request,
        access_token: Optional[str] = Query(default=None),
        users_store: UsersStore = Depends(users_store),
        sessions_store: SessionsStore = Depends(sessions_store),
    ) -> PermissionCredentials:
        bearer_user = await super().__call__(
            request=request,
            access_token=access_token,
            users_store=users_store,
            sessions_store=sessions_store,
        )

        match: Optional[dict[str, str]] = None

        for scope in bearer_user.user.scopes:
            if self.scope.startswith(scope):
                match = scope
                break

        if match is None:
            raise HTTPException(
                status_code=403, detail="User does not have access to this resource"
            )

        return PermissionCredentials(
            scheme=bearer_user.scheme,
            token=bearer_user.token,
            session=bearer_user.session,
            user=bearer_user.user,
            route_scope=self.scope,
            matched_scope=match,
        )
