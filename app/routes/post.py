from app.database import get_db
from app.schema import CreatePost,PostResponse,UpdatePost
from app import models,oauth2,schema
from sqlalchemy.orm import Session
from fastapi import Depends,APIRouter,status,HTTPException,Response,Query
from typing import Optional,List
from datetime import datetime,timezone



router = APIRouter(
    prefix='/posts',
    tags=['Post']
)

# Posts Functions 

# create Post
@router.post('',status_code = status.HTTP_201_CREATED,response_model=PostResponse)
def Createpost(data:CreatePost , db:Session = Depends(get_db),current_user_id: models.UserModel = Depends(oauth2.get_current_user)):
     
     "tradational routerroach"
    #  conn = get_connection()
    #  cursor = conn.cursor()

    #  cursor.execute("""INSERT INTO posts (title, content , published ) VALUES (%s,%s,%s) returning *""",
    #                 (data.title,data.content,data.published))
    #  Created_post = cursor.fetchone()
    #  conn.commit()
    #  cursor.close()
    #  conn.close()

     "SQLALchemy"
     Created_post = models.PostModel(
         user_id = current_user_id.id,
         title = data.title,
         content = data.content,
         published = data.published
     )
     # similar to above
    #  Created_post = models.PostModel(**data.dict())
     
     db.add(Created_post)
     db.commit()
     db.refresh(Created_post)

     return Created_post
     


# Get all Posts  
@router.get('',response_model=List[PostResponse])
def getposts(db:Session = Depends(get_db)):
    'Code with Tradational routerraoch'
    # conn = get_connection()
    # cursor = conn.cursor()

    # cursor.execute('SELECT * FROM posts')
    # data = cursor.fetchall()
    # cursor.close()
    # conn.close()

    'code with SQlalchemy'
    data = db.query(models.PostModel).all()
    return data 


# search Posts 
@router.post('/search')
def search(user_id:Optional[int]=Query(None,description='Filter Users By Id') ,
           title:Optional[str] = Query('',min_length=1,description='filter by Post Title') ,
           limit:Optional[int] =Query(None,le=100,description = 'Number of Posts retreived'),
           db:Session = Depends(get_db)):
    
    query = db.query(models.PostModel)

    if user_id is not None:
        query = query.filter(models.PostModel.user_id == user_id)
    
    if title :
        query = query.filter(models.PostModel.title.contains(title))
    
    if limit is not None:
        query = query.limit(limit)
    
    data = query.all()
    return data





# get Only Posts OF Particular user
@router.get('/{user_id}',response_model=List[PostResponse])
def getposts(user_id:int ,db:Session = Depends(get_db),current_user_id: models.UserModel = Depends(oauth2.get_current_user)):

    'code with Tradational routerraoch'
    # conn = get_connection()
    # cursor = conn.cursor()

    # cursor.execute('SELECT * FROM posts WHERE id = %s ',(str(id),))
    # post = cursor.fetchall()

    "code with SQLalchemy"
    posts = db.query(models.PostModel).filter(models.PostModel.user_id == user_id).all()
    
    if not posts :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Post Not FOund')
    return posts


# delete Post
@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def deletepost(id:int,db:Session = Depends(get_db),get_current_user : models.UserModel = Depends(oauth2.get_current_user)):
    # deleting Post

    "Tradational routerroach"
    # conn = get_connection()
    # cursor = conn.cursor()

    # cursor.execute('DELETE FROM posts WHERE id = %s returning *',(str(id),))
    # deleted_post = cursor.fetchone()

    # conn.commit()
    # cursor.close()
    # conn.close()


    "SqlAlchemy"
    deleted_post = db.query(models.PostModel).filter(models.PostModel.id == id).first()
    if deleted_post ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No Any Post Exist.')
    if deleted_post.user_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='You are Not Authorized to do this Request')
    db.delete(deleted_post)
    db.commit()

    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
        
    
   

# update Posts
@router.put('/{id}',response_model=PostResponse)
def update_post(id:int , data:UpdatePost,db:Session = Depends(get_db),get_current_user : models.UserModel = Depends(oauth2.get_current_user)):
     current_time = datetime.now(timezone.utc)
    #  conn = get_connection()
    #  cursor = conn.cursor()
    
    #  cursor.execute("""UPDATE posts SET 
    #                   title=%s,
    #                   content = %s,
    #                   published = %s,
    #                   updated_at = %s 
    #                   WHERE id = %s returning *""",(data.title,data.content,data.published,datetime.now(timezone.utc),str(id)))
    #  updated_post = cursor.fetchone()

    #  conn.commit()
    #  cursor.close()
    #  conn.close()
     post = db.query(models.PostModel).filter(models.PostModel.id==id)
     required_post = post.first()
     if required_post == None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No Any Post Exist.')
     if required_post.user_id != get_current_user.id:
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='You are Not Authorized to do this Request')
     data.updated_at = datetime.now(timezone.utc)
     
     post.update(data.model_dump(),synchronize_session=False)
     db.commit()
     db.refresh(required_post)
     return required_post