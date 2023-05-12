from passlib.context import CryptContext

# Define the defaulting hashing algorithm to passlib
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)