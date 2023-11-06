GET_USER_BY_ID = """
SELECT id, username, password, name, scopes
FROM users
WHERE id = {id}
"""

GET_USER_BY_USERNAME = """
SELECT id, username, password, name, scopes
FROM users
WHERE username = {username}
"""

GET_USERS = """
SELECT id, username, password, name, scopes
FROM users
WHERE {where}
"""

CREATE_USER = """
INSERT INTO users(username, password, name, scopes)
VALUES ({username}, {password}, {name}, {scopes})
RETURNING id
"""

UPDATE_USER = """
UPDATE users
SET username = {username}, name = {name}, scopes = {scopes}
WHERE id = {id}
"""

UPDATE_USER_PASSWORD = """
UPDATE users
SET username = {username}, password = {password}, name = {name}, scopes = {scopes}
WHERE id = {id}
"""

DELETE_USER = """
DELETE FROM users
WHERE id = {id}
"""
