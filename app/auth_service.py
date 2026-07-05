 
from fastapi import status,HTTPException,Response


from app.schema import UserLogin,TokenData,refreshToken,Token
from app.models import UserModel,RefreshToken

from app.utils import VerifyHash
from app import oauth2
from datetime import datetime ,timezone

from fastapi.security import OAuth2PasswordRequestForm




def Login_service(request,credential_data,db):
    User = db.query(UserModel).filter(UserModel.email == credential_data.username).first()

    if not User:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Password or User Incorrect')
    
    if not VerifyHash(credential_data.password , User.password) : 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Password or User Incorrect')
    if not User.is_verified:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please verify your email."
        )
    # create a JWT token And Return That Token 
    
    access_token = oauth2.create_access_token(user_id = User.id)[0]
    refresh_token,refresh_token_data = oauth2.create_refresh_token(user_id=User.id)
    refresh_token_obj = RefreshToken(user_id = refresh_token_data.user_id,
                jwid = refresh_token_data.jti,
                expires_at = refresh_token_data.exp,
                user_agent=request.headers.get("User-Agent"))
    
    db.add(refresh_token_obj)
    db.commit()
    return {'access_token':access_token,
            'refresh_token':refresh_token,
            'token_type':'bearer'}


def refresh_service(request,token,db):
    payload : TokenData = oauth2.verify_refresh_token(token.refresh_token)

    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Could not Validate Credentials',
                                           headers={'WWW-Authenticate':'Bearer'})
    
    # check if the Db has that Token or not?
    refresh_token_obj = db.query(RefreshToken).filter(RefreshToken.jwid ==  payload.jti).first()

    # if not exist then GIve error .. 
    # if token is revoked give error ..
    # if token is expired give error ..
    if refresh_token_obj is None or \
    refresh_token_obj.revoked or \
    refresh_token_obj.expires_at < datetime.now(timezone.utc):
        
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Could not Validate Credentials',
                                           headers={'WWW-Authenticate':'Bearer'})
    
    # now entire Validation is COmplete We can easily Create New TOkens
    new_access_token = oauth2.create_access_token(payload.user_id)[0]

    new_refresh_token,new_refresh_payload = oauth2.create_refresh_token(payload.user_id)

    # now we have new TOkens But We need to perfrom Token ROtation of
    # refresh Session 
    # that old Refresh TOken Becomes revoked
    refresh_token_obj.revoked=True
    refresh_token_obj.last_used_at = datetime.now(timezone.utc)

    # logging the new Refresh Token to The DB
    new_refresh_token_obj = RefreshToken(
        user_id = new_refresh_payload.user_id,
                  jwid = new_refresh_payload.jti,
                  expires_at = new_refresh_payload.exp,
                  user_agent=request.headers.get("User-Agent")
    )
    # now adding new object and commit 
    db.add(new_refresh_token_obj)
    db.commit()

    return {'access_token':new_access_token,
            'refresh_token':new_refresh_token,
            'token_type':'bearer'}
    


def logout_service(token,db):
    payload : TokenData = oauth2.verify_refresh_token(token.refresh_token)

    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Could not Validate Credentials',
                                           headers={'WWW-Authenticate':'Bearer'})
    
    refresh_token_obj = db.query(RefreshToken).filter(RefreshToken.jwid ==  payload.jti).first()
    if refresh_token_obj is None or refresh_token_obj.revoked:
        raise HTTPException(
        status_code=401,
        detail="Invalid refresh token"
    )
    refresh_token_obj.revoked = True
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def logout_all_service(token,db):
    payload : TokenData = oauth2.verify_refresh_token(token.refresh_token)

    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Could not Validate Credentials',
                                           headers={'WWW-Authenticate':'Bearer'})
    
    db.query(RefreshToken).filter(RefreshToken.user_id ==  payload.user_id).update({'revoked':True})
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)