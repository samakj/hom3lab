from datetime import datetime
from typing import Any, Dict, Optional

import jwt


def sign_jwt(payload: Dict[str, Any], config: Dict[str, Any]) -> str:
    secret = config.get("secret")
    algorithm = config.get("algorithm")

    if secret is None:
        raise TypeError("No secret provided to sign jwt with")
    if algorithm is None:
        raise TypeError("No algorithm provided to sign jwt with")

    return jwt.encode(payload=payload, key=secret, algorithm=algorithm)  # type: ignore


def decode_jwt(token: str, config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    secret = config.get("secret")
    algorithm = config.get("algorithm")

    if secret is None:
        raise TypeError("No secret provided to sign jwt with")
    if algorithm is None:
        raise TypeError("No algorithm provided to sign jwt with")

    try:
        payload = jwt.decode(jwt=token, key=secret, algorithms=[algorithm])  # type: ignore
        return (
            payload
            if datetime.fromisoformat(payload.get("expires", "2000-01-01"))
            > datetime.utcnow()
            else None
        )
    except Exception:
        return None
