from flask import Blueprint,request
from ...extensions import db
from ...models import Order,Book
from datetime import datetime
import random

order_bp = Blueprint('order',__name__)

def generate_order_number() -> str:
    """
    生成订单编号
    例：202607070123
    """
    date_part = datetime.now().strftime("%Y%m%d")
    random_part = str(random.randint(1000,9999))
    
    return f"{date_part}{random_part}"
    
    
@order_bp.route("",methods=["POST"])
def create_order():
    
    order_number = generate_order_number()
    data = request.get_json()
    
    if not data:
        return {"error":"请求体必须是json格式"},400
    
    order = Order(order_number=order_number)
    
    book_data = data.get("books",[])
    
    if not book_data or not isinstance(book_data,list):
        return {"error":"请提供有效的书籍列表"},400
    
    book_obj = []
    for item in book_data:
        book_name = item.get("book_name","").strip()
        price_str = item.get("price")
        borrow_count_str = item.get("count")
        if not book_name or not price_str or borrow_count_str is None:
            return {"error":"每个书籍必须包含书籍名和价格及借阅书籍数量"},400
        try:
            price = float(price_str)
        except Exception as e:
            return {"error":"价格必须是数字"},422
        try:
            borrow_count = int(borrow_count_str)
        except Exception as e:
            return {"error":"数量必须是数字"},422
        book = Book.query.filter_by(book_name=book_name).first()
        
        if not book:
            return {"error":"资源不存在"},404
        
        if book.book_count<borrow_count:
            return {"error":f"书籍{book_name}库存不足(仅剩{book.book_count}本)"},400
        if borrow_count <= 0:
            return {"error": "借阅数量必须大于0"}, 400
        
        book.book_count-=borrow_count
        book_obj.append(book)
        
    order.books.extend(book_obj)
    
    try:
        db.session.add(order)
        db.session.commit()
    except Exception as e:
        return {"error":"服务器内部错误"},500
    
    return order.to_dict(),201
    

@order_bp.route("/<int:order_id>",methods=["DELETE"])
def delete_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return {"error":"资源不存在"} ,404
    return "",204

@order_bp.route("/<int:order_id>",methods=["PATCH"])
def update_order(order_id):
    order = Order.query.get(order_id)
    
    if not order:
        return {"error":"资源不存在"},404
    data = request.get_json()
    if not data:
        return {"error":"请求体必须是json格式"},400
    
    if 'is_finished' in data:
        
        is_finished_str = data["is_finished"]
        
        is_finish = is_finished_str.lower() in ("true","1")
        order.is_finished = is_finish
    
    if "books" in data:
        
        return {"error": "订单书籍列表不可直接修改，请取消订单后重新下单"}, 400

@order_bp.route("/<int:order_id>",methods=["GET"])
def get_order(order_id):
    order = Order.query.get(order_id) 
    if not order:
        return {"error":"资源不存在"},404
    return order.to_dict(),200

@order_bp.route("",methods=["GET"])
def get_orders():
    
    page = request.args.get("page",1,type=int)
    per_page = request.args.get("per_page",10,type=int)
    
    keyword = request.args.get("keyword","").strip()
    is_finished_str=request.args.get("is_finished")
    
    query = Order.query
    if keyword:
        query = query.filter(Order.order_number.contains(keyword))
    if is_finished_str is not None:
        is_finished = is_finished_str.lower() in ('true','1')
        query = query.filter_by(is_finished=is_finished)
    paginated = query.order_by(Order.id.desc()).paginate(page=page,per_page=per_page,error_out=False)
    
    return {
        "items":[order.to_dict() for order in paginated.items],
        "page":page,
        "per_page":per_page,
        "total":paginated.total,
        "pages":paginated.pages,
        "has_next":paginated.has_next,
        "has_prev":paginated.has_prev
    }
        