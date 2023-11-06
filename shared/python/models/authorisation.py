from pydantic import BaseModel, Field
from shared.python.models.session import Session
from shared.python.models.user import User, UserNoPassword


class JWTAuthorizationCredentials(BaseModel):
    scheme: str = Field(description="The scheme provided in the auth.")
    token: str = Field(description="The token provided in the auth.")
    session: Session = Field(description="The parsed session from the token.")


class UserCredentials(JWTAuthorizationCredentials):
    user: User = Field(description="The user in the session.")


class PermissionCredentials(UserCredentials):
    route_scope: str = Field(description="The required scope for the route.")
    matched_scope: str = Field(
        description="The user scope that matched to the route scope."
    )


class LoginResponse(BaseModel):
    access_token: str = Field(
        description="The access token that can be used on subsequent requests."
    )
    user: UserNoPassword = Field(description="The user that has logged in.")
    session: Session = Field(
        description="The session that has just been created for this login."
    )


class LogoutResponse(BaseModel):
    session: Session = Field(description="The session that has ended for this logout.")
