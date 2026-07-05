from fastapi import Depends, APIRouter, status, HTTPException, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app import schema
from app import models
from app.utils import hash
from app.services.email.email import send_verification_email,send_password_refresh_email
from app import oauth2
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from app.services.email.email_template import render_template
from datetime import datetime ,timezone,timedelta
from app import utils
router = APIRouter(
    prefix='/password',
    tags=['password']
)



# CHange Password
@router.put('/change-password')
def changePass(Password : schema.PasswordChange,
               current_user : models.UserModel = Depends(oauth2.get_current_user),
               db: Session = Depends(get_db)):
    if Password.new_password != Password.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Passwords Not match')
    
    if Password.old_password == Password.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='New Password Must be DIfferent from Old Password')
    
    result = utils.VerifyHash(Password.old_password,current_user.password)
    if not result:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Incorrect Password')
    
    current_user.password = utils.hash(Password.confirm_password)
    db.commit()

    return {
        'message':'Password Changed SUccessfully'
        }




# forget Password and Reset Password
@router.post('/forgot-password')
async def ForgetPassword(email : schema.PasswordForget,
                   db: Session = Depends(get_db)):
    
    User = db.query(models.UserModel).filter(models.UserModel.email == email.email).first()

    if not User:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Wrong Email Try Again!')
    if not User.is_verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='User Not Verified')
    try:
        reset_token,_ = oauth2.create_password_reset_token(user_id=User.id)
        await send_password_refresh_email(User.email,reset_token,username = User.name)
    except Exception as e:
         raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send Password refresh email. Please try again. Error: {str(e)}"
        )
    


@router.get('/reset-password')
def ResetPassword(token:str,
                  db:Session = Depends(get_db)):
    payload = oauth2.verify_forget_password_token(token)

    user = db.query(models.UserModel).filter(models.UserModel.id == payload.user_id).first()
    if not user:        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    

    html = render_template(

        "pages/reset_password.html",

        username=user.name,

        token=token,

        logo_url=""

    )

    return HTMLResponse(content=html)
    


@router.post('/reset-password')
def ResetPasswordPost(
    data: schema.PasswordReset,
    db: Session = Depends(get_db)):

    if data.new_password != data.confirm_password:

        html = render_template(
            "pages/reset_password.html",
            token=data.token,
            error="Passwords do not match",
            logo_url=""
        )
        return HTMLResponse(content=html)
    

    payload = oauth2.verify_forget_password_token(data.token)
    user = (db.query(models.UserModel).filter(models.UserModel.id == payload.user_id).first())
    if not user:
        html = render_template(
            "pages/reset_password.html",
            token=data.token,
            error="Email Not Exist",
            logo_url=""
        )
        return HTMLResponse(content=html)
    
    if user.password_changed_at:
         utils.TimeFromDate(user)
        
    user.password = utils.hash(data.new_password)
    user.password_changed_at = datetime.now(timezone.utc)
    db.commit()

    html = render_template(

    "pages/password_reset_success.html",

    login_url="http://127.0.0.1:8000/login",

    logo_url="")

    return HTMLResponse(content=html)
    
