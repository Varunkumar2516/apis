from fastapi import APIRouter,Depends,status,HTTPException,Response,Request
from app.database import get_db
from sqlalchemy.orm import Session
from app.schema import UserLogin,TokenData,refreshToken,Token
from app.models import UserModel,RefreshToken

from app.utils import VerifyHash
from app import oauth2
from datetime import datetime ,timezone

from fastapi.security import OAuth2PasswordRequestForm


from app.auth_service import Login_service,refresh_service,logout_service,logout_all_service
router = APIRouter(
    tags=['Authentication']

)

@router.post('/login',response_model=Token)
def login(request: Request,credential_data : OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    # OAuth2PasswordRequestForm
    # {'username' : 
    #  'password' : }
    return Login_service(request,credential_data,db)



@router.get('/auth/me')
def me(current_user = Depends(oauth2.get_current_user)):
    return current_user




@router.post('/refresh',response_model = Token)
def refresh(request: Request,token : refreshToken,db: Session = Depends(get_db)):
    return refresh_service(request,token,db)


@router.post('/logout',status_code=status.HTTP_204_NO_CONTENT)
def logout(token : refreshToken,db:Session = Depends(get_db)):
    return logout_service(token,db)

@router.post('/logoutAll',status_code=status.HTTP_204_NO_CONTENT)
def logoutall(token : refreshToken,db:Session = Depends(get_db)):
    return logout_all_service(token,db)



