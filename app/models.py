from sqlalchemy import Column
from sqlalchemy import Integer,Boolean,ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from app.database import Base
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

class UserModel(Base):
    __tablename__ = 'Users'

    id = Column(Integer,primary_key=True,nullable=False)
    name = Column(String,nullable=False)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    is_verified = Column(Boolean,server_default='FALSE',nullable=False)
    password_changed_at =Column(TIMESTAMP(timezone=True),nullable=True)
    role_id = Column(Integer,ForeignKey("roles.id"),nullable=False,    server_default="3")

    post = relationship('PostModel')
    role = relationship("Roles")

class Roles(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)

    name = Column(String, unique=True, nullable=False)

    description = Column(String)



class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True)

    name = Column(String, unique=True)

    description = Column(String)


class RolePermission(Base):

    __tablename__ = "role_permissions"

    role_id = Column(Integer,ForeignKey("roles.id"), primary_key=True)

    permission_id = Column(Integer,ForeignKey("permissions.id"),primary_key=True)

    
class PostModel(Base):
    __tablename__='post'
    
    user_id = Column(Integer,ForeignKey('Users.id',ondelete='CASCADE'),nullable=False)
    id = Column(Integer,primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean,server_default='TRUE')
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

    



class RefreshToken(Base):
     __tablename__ ='refresh_token'

     id = Column(Integer,primary_key=True,nullable=False)
     user_id = Column(Integer,ForeignKey('Users.id',ondelete='CASCADE'),nullable=False)
     jwid = Column(UUID(as_uuid=True),nullable=False,index = True)
     revoked = Column(Boolean,default=False,nullable=False)
     expires_at = Column(TIMESTAMP(timezone=True),nullable=False)
     created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
     last_used_at = Column(TIMESTAMP(timezone=True),nullable=True )
     user_agent = Column(String,nullable=True)
