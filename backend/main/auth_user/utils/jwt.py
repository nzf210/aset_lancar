import jwt
from datetime import datetime, timedelta
import os


class TokenManager:
    """
    # Example usage:
    secret_key = "your_secret_key_here"
    token_manager = TokenManager(secret_key)

    # Generate a token
    payload = {"user_id": 123, "role": "admin"}
    token = token_manager.generate_token(payload)
    print(f"Generated Token: {token}")

    # Refresh a token
    new_token = token_manager.refresh_token(token)
    if new_token:
        print(f"Refreshed Token: {new_token}")
    else:
        print("Token expired, please re-authenticate.")
    """

    def __init__(self):
        self.secret_key = os.environ.get("JWT_ACCESS_TOKEN_PRIVATE_KEY")

    def generate_token(self, payload, expiration_minutes=10):
        expiration = datetime.utcnow() + timedelta(minutes=expiration_minutes)
        created = datetime.utcnow()
        payload["exp"] = expiration
        payload["iat"] = created
        new_secret = self.secret_key
        return jwt.encode(payload, new_secret, algorithm="HS256")

    def refresh_token(self, token):
        try:
            decoded_token = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            payload = decoded_token.copy()
            del payload["exp"]  # Remove the old expiration time
            del payload["iat"]
            return self.generate_token(payload, expiration_minutes=131400)
        except jwt.ExpiredSignatureError:
            # Handle token expiration error
            return None
        except jwt.exceptions.DecodeError:
            # Handle invalid token error
            return None
