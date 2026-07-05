from fastapi import Depends, APIRouter, status, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schema import UserCreate, UserResponse
from app import models
from app.utils import hash
from app.services.email.email import send_verification_email
from app import oauth2
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from app.services.email.email_template import render_template
router = APIRouter(
    tags=['User']
)

@router.post('/user', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def CreateUser(data: UserCreate, db: Session = Depends(get_db)):
    
    # 1. Check if email already exists
    user_with_email = db.query(models.UserModel).filter(models.UserModel.email == data.email).first()

    if user_with_email :
        if user_with_email.is_verified:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Email Already Exists'
            )
        else:
            db.delete(user_with_email)
            db.commit()


    # 2. Hash password and update payload
    hashed_password = hash(data.password)
    user_dict = data.model_dump()
    user_dict["password"] = hashed_password
    
    # 3. Initialize DB Model
    created_user = models.UserModel(**user_dict)
    db.add(created_user)
    db.commit()
    db.refresh(created_user)

    # 4. Try sending the verification email
    try:
        verification_token, _ = oauth2.create_email_verify_token(user_id= created_user.id)
        await send_verification_email(created_user.email, verification_token,username=created_user.name)
    except Exception as e:
        # If the email fails, roll back the user creation so they can try again
        db.delete(created_user)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send verification email. Please try again. Error: {str(e)}"
        )

    return created_user


@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    payload = oauth2.verify_email_token(token)

    user = db.query(models.UserModel).filter(models.UserModel.id == payload.user_id).first()
    if not user:        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user.is_verified:
        # Redirect directly to your new login page even if already verified
        html = render_template(
                            "pages/verified_email.html",
                            username=user.name,)

        return HTMLResponse(content=html)
    
    user.is_verified = True
    db.commit()

    # Smooth Frontend Handoff: Redirect straight to the success page!
    html = render_template(
                            "pages/verified_email.html",
                            username=user.name,)

    return HTMLResponse(content=html)
    


@router.get('/users', response_model=List[UserResponse])
def getusers(db: Session = Depends(get_db)):
    return db.query(models.UserModel).all()


@router.get('/users/{id}', response_model=UserResponse)
def getuser(id: int, db: Session = Depends(get_db)):
    user = db.query(models.UserModel).filter(models.UserModel.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not Found'
        )
    return user
