from ..extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username=db.Column(db.String(20),unique=True,nullable=False)
    password_hash=db.Column(db.String(255),nullable=False)
    role = db.Column(db.String(20),default='borrower')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
    
    # 外键
    profile = db.relationship("Profile",back_populates="user",uselist=False)
    
    orders = db.relationship("Order",back_populates="user",lazy='select')
    
    def __repr__(self):
        return f"<User:{self.username}>"
    
    def to_dict(self):
        return {
            "id":self.id,
            "username":self.username,
            "is_active":self.is_active,
            "created_at":self.created_at.isoformat() if self.created_at else None,
            "updated_at":self.updated_at.isoformat() if self.updated_at else None,
            "profile":{
                "real_name":self.profile.real_name,
                "phone":self.profile.phone,
                "email":self.profile.email,
                "avatar_url":self.profile.avatar_url,
                "employee_id":self.profile.employee_id,
                "description":self.profile.description
            } if self.profile else None
        }