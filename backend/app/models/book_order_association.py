from ..extensions import db

book_order_table = db.Table(
    'book_order',
    db.Column('book_id',db.Integer,db.ForeignKey("books.id"),primary_key=True),
    db.Column('order_id',db.Integer,db.ForeignKey("orders.id"),primary_key=True)

)