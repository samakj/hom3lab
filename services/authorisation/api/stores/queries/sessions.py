GET_SESSION_BY_ID = """
SELECT id, user_id, expires, created, ip, disabled
FROM sessions
WHERE id = {id}
"""

GET_SESSIONS = """
SELECT id, user_id, expires, created, ip, disabled
FROM sessions
WHERE {where}
"""

CREATE_SESSION = """
INSERT INTO sessions(user_id, created, expires, ip, disabled)
VALUES ({user_id}, {created}, {expires}, {ip}, {disabled})
RETURNING id
"""

UPDATE_SESSION = """
UPDATE sessions
SET user_id = {user_id}, expires = {expires}, created = {created}, ip = {ip}, disabled={disabled}
WHERE id = {id}
"""

DELETE_SESSION = """
DELETE FROM sessions
WHERE id = {id}
"""
