from flask import Blueprint,request
from ...extensions import db
from ...models import Book

book_bp = Blueprint('book',__name__)

@book_bp.route("",methods=["POST"])
def create_book():
    data = request.get_json()
    
    if not data:
        return {"error":"请求体必须为json格式"},400
    
    book_name = data.get("book_name","").strip()
    price_str = data.get("price")
    description=data.get("description","").strip()
    book_img = data.get("book_img","").strip()

    if not book_name or price_str is None:
        return {"error":"请输入书籍名和价格"},400
    
    existing = Book.query.filter_by(book_name=book_name).first()
    
    if existing:
        return {"error":"书籍已存在"},409
    
    try:
        price = float(price_str)
    except ValueError:
        return {"error":"价格必须是数字"},422
    
    try:
        book = Book(book_name=book_name,price=price,description=description,book_img=book_img)
        db.session.add(book)
        db.session.commit()
    except Exception as e:
        return {"error":"服务器内部错误"},500

    return book.to_dict(),201

@book_bp.route("/<int:book_id>",methods=["DELETE"])
def delete_book(book_id):
     book = Book.query.get(book_id)
     if not book:
         return {"error":"资源不存在"},404
     
     return "",204
 
@book_bp.route("/<int:book_id>",methods=["PATCH"])
def update_book(book_id):
    
    book = Book.query.get(book_id) 
    if not book:
        return {"error":"资源不存在"},404
    
    data = request.get_json()
    if not data:
        return {"error":"请求体必须为json格式"},400
    
    if 'book_name' in data:
        new_book_name = data["book_name"].strip()
        existing = Book.query.filter(Book.book_name==new_book_name,Book.id !=book_id).first()
        if existing:
            return {"error":"该书籍名已被其他书籍使用"},409
        book.book_name = new_book_name
    
    if "price" in data:
        price_str = data["price"]
        
        try:
            price = float(price_str)
        except Exception as e:
            return {"error":"价格格式错误"},422
        if price <0:
            return {"error":"价格不能小于0"},422
        book.price = price
    
    if 'description' in data:
        new_description = data["description"].strip()
        book.description = new_description
        
    if 'book_img' in data:
        new_book_img = data["book_img"].strip()
        book.book_img = new_book_img
    if 'is_listing' in data:
        new_is_listing = data["is_listing"].lower() in ('true','1')
        book.is_listing = new_is_listing
    
    return book.to_dict(),200

@book_bp.route("/<int:book_id>",methods=["GET"])
def get_book(book_id):
    book = Book.query.get(book_id) 
    if not book:
        return {"error":"资源不存在"},404
    return book.to_dict(),200

@book_bp.route("",methods=["GET"])
def get_books():
    page = request.args.get("page",1,type=int)
    per_page = request.args.get("per_page",10,type=int)
    
    keyword=request.args.get("keyword","").strip()
    is_listing_str =request.args.get("is_listing")
    
    
    query = Book.query
    if keyword:
        query = query.filter(Book.book_name.contains(keyword))
    if is_listing_str is not None:
        try:
            is_listing = is_listing_str.lower() in ('true','1')
        
        except Exception as e:
            return {"error":"状态格式错误"},422
    
        query = query.filter_by(is_listing=is_listing)
    
    paginated = query.order_by(Book.id.desc()).paginate(page=page,per_page=per_page,error_out=False)
    
    return {
        "item":[book.to_dict() for book in paginated.items],
        "total":paginated.total,
        "page":page,
        "per_page":per_page,
        "pages":paginated.pages,
        "has_next":paginated.has_next,
        "has_prev":paginated.has_prev
        },200