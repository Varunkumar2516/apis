# password Hashing
'using passlib library Older library'
# from passlib.context import CryptContext

# pwd_context = CryptContext(
#     schemes=['argon2'],
#     deprecated ="auto"
# )
# password = 'hello123'
# hashed_value = pwd_context.hash(password)

# result = pwd_context.verify('hello123',hashed_value)

# print(hashed_value)
# print(result)


'using pwdlib modern library '

from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher
from pwdlib.hashers.argon2 import Argon2Hasher

password_hasher = PasswordHash([Argon2Hasher(),BcryptHasher()])


def main():
    password = 'hello123'
    hashed_value1 = password_hasher.hash(password)
    
    result1 = password_hasher.verify(password,hashed_value1)
   
    print(hashed_value1)
    print(result1)
   

if __name__=='__main__':
    main()


def hash(password : str):
    return password_hasher.hash(password)


def VerifyHash(password:str,hashedPass:str):
    return password_hasher.verify(password,hashedPass)


from datetime import datetime,timezone
from fastapi import HTTPException,status
def TimeFromDate(user):
    # 1. Grab current time in UTC
    now = datetime.now(timezone.utc)
    
    # 2. Safely ensure last_changed has a UTC timezone label
    # If database datetime is naive, use .replace(tzinfo=timezone.utc)
    # If database datetime is already timezone-aware, use .astimezone(timezone.utc)
    if user.password_changed_at.tzinfo is None:
        last_changed = user.password_changed_at.replace(tzinfo=timezone.utc)
    else:
        last_changed = user.password_changed_at.astimezone(timezone.utc)
    
    # 3. Calculate time difference
    time_since_last_change = now - last_changed
    
    # Convert total seconds to clean minutes
    minutes_since_change = time_since_last_change.total_seconds() / 60

    if minutes_since_change < 20:
        # Use ceil so it rounds up nicely (e.g., 18.2 minutes left shows as 19 minutes left)
        import math
        minutes_left = math.ceil(20 - minutes_since_change)
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Security Cooldown: You recently changed your password. Please wait another {minutes_left} minutes."
        )