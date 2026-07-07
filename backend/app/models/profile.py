from ..extensions import db
from datetime import datetime

class Profile(db.Model):
    __tablename__='profiles'
    id = db.Column(db.Integer,primary_key=True,nullable=False,autoincrement=True)
    
    real_name = db.Column(db.String(20),nullable=True)
    description=db.Column(db.String(255),nullable=True)
    phone=db.Column(db.String(20),unique=True)
    email=db.Column(db.String(20),unique=True)
    avatar_url = db.Column(db.String(255),nullable=True)
    employee_id = db.Column(db.String(20),unique=True,nullable=True)
    
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
    
    # 外键
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"),unique=True)
    user = db.relationship("User",back_populates="profile",uselist=False)
    
    def __repr__(self):
        return f"<Profile:{self.real_name}>"
    
    def to_dict(self):
        return {
            "id":self.id,
            "real_name":self.real_name,
            "phone":self.phone,
            "email":self.email,
            "description":self.description,
            "avatar_url":self.avatar_url,
            "employee_id":self.employee_id,
            "created_at":self.created_at.isoformat() if self.updated_at else None,
            "updated_at":self.updated_at.isoformat() if self.updated_at else None
        }