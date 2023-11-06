from typing import Optional
from fastapi import Depends, HTTPException, Query, Request

from auth.jwt_bearer import JWTBearer
from stores.users import UsersStore
from stores.sessions import SessionsStore
from shared.python.models.authorisation import UserCredentials


class BearerUser(JWTBearer):
    def __init__(self):
        super().__init__()

    async def __call__(
        self,
        request: Request,
        access_token: Optional[str] = Query(default=None),
        users_store: UsersStore = Depends(UsersStore),
        sessions_store: SessionsStore = Depends(SessionsStore),
    ) -> UserCredentials:
        jwt_bearer = await super().__call__(
            request=request,
            access_token=access_token,
            sessions_store=sessions_store,
        )
        user = await users_store.get_user(id=jwt_bearer.session.user_id)

        if user is None:
            raise HTTPException(status_code=401, detail="Invalid session user")

        return UserCredentials(
            scheme=jwt_bearer.scheme,
            token=jwt_bearer.token,
            session=jwt_bearer.session,
            user=user,
        )
