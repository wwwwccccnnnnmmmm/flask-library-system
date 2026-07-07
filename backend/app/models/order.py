from ..extensions import db
from datetime import datetime
from .book_order_association import book_order_table



class Order(db.Model):
    __tablename__='orders'
    id = db.Column(db.Integer,primary_key=True,nullable=False,autoincrement=True)
    order_number=db.Column(db.String(20),unique=True,nullable=False)
    is_finished = db.Column(db.Boolean,nullable=True)
    
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
    
    # 外键
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    user = db.relationship("User",back_populates="orders")
    
    books = db.relationship('Book',secondary=book_order_table,back_populates='orders')
    
    def __repr__(self):
        return f"<Order:{self.order_number}>"
    
    def to_dict(self):
        return {
            "id":self.id,
            "order_number":self.order_number,
            "created_at":self.created_at.isoformat() if self.created_at else None,
            "updated_at":self.updated_at.isoformat() if self.updated_at else None,
            "books":[book.to_dict() for book in self.books] if self.books else None
        }