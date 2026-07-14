import bcrypt
import jwt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plaintext: str, hashed: str) -> bool:
    return bcrypt.checkpw(plaintext.encode('utf-8'), hashed.encode('utf-8'))

def create_jwt_token(data: dict, key: str, algorithm: str = "HS256") -> str:
    encoded_jwt = jwt.encode(data, key, algorithm=algorithm)
    return encoded_jwt

def decode_jwt_token(token: str, key: str, algorithms: list[str] = ["HS256"]) -> dict:
    decoded_jwt = jwt.decode(token, key, algorithms=algorithms)
    return decoded_jwt