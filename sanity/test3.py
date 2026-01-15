from core.security import hash_password, verify_password
import warnings

warnings.filterwarnings("ignore", module="passlib")


# Example usage
plain_password = "mysecretpassword"
hashed = hash_password(plain_password)
print(f"Hashed Password: {hashed}")

is_valid = verify_password(plain_password, hashed)
print(f"Password valid: {is_valid}")

is_invalid = verify_password("wrongpassword", hashed)
print(f"Password valid: {is_invalid}")
