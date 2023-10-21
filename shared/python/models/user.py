from pydantic import BaseModel, Field


class CreateUser(BaseModel):
    username: str = Field(description="The users username.")
    password: str = Field(description="The users password.")
    name: str = Field(description="The informal name to use for users.")
    scopes: list[str] = Field(
        description="The scopes that the user has access to.", default=[]
    )


class User(BaseModel):
    id: int = Field(description="The users id.")
    username: str = Field(description="The users username.")
    password: str = Field(description="The users password.")
    name: str = Field(description="The informal name to use for users.")
    scopes: list[str] = Field(
        description="The scopes that the user has access to.", default=[]
    )


class UserNoPassword(BaseModel):
    id: int = Field(description="The users id.")
    username: str = Field(description="The users username.")
    name: str = Field(description="The informal name to use for users.")
    scopes: list[str] = Field(
        description="The scopes that the user has access to.", default=[]
    )
