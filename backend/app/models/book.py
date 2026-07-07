from ..extensions import db
from datetime import datetime
from .book_order_association import book_order_table

class Book(db.Model):
    __tablename__ ='books'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    book_name=db.Column(db.String(100),unique=True,nullable=False)
    price=db.Column(db.Numeric(10, 2),nullable=False,default=0.0)
    
    book_count = db.Column(db.Integer,nullable=True, default=0)
    
    description=db.Column(db.Text,nullable=False)
    book_img =db.Column(db.String(255),nullable=False,default="")
    
    is_listing=db.Column(db.Boolean,default=True)

    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
    
    # 外键
    orders = db.relationship('Order',secondary=book_order_table,back_populates='books')
    
    def __repr__(self):
        return f"<Book:{self.book_name}>"
    
    def to_dict(self):
        return {
            "id":self.id,
            "book_name":self.book_name,
            "book_count":self.book_count,
            "price":str(self.price) if self.price else "0.00",
            "description":self.description,
            "book_img":self.book_img,
            "created_at":self.created_at.isoformat() if self.created_at else None,
            "updated_at":self.updated_at.isoformat() if self.updated_at else None,
        }