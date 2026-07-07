from flask import Blueprint,request
from werkzeug.security import generate_password_hash,check_password_hash
from ...models import User
from ...extensions import db

auth_bp = Blueprint('auth',__name__)

@auth_bp.route("/login",methods=["POST"])
def login():
    data = request.get_json()
    
    if not data:
        return {"error":"请求体必须为json格式"},400
    
    username = data.get("username","").strip()
    password = data.get("password","").strip()
    
    if not username or not password:
        return {"error":"用户名和密码不能为空"},400

    user = User.query.filter_by(username=username).first()
    
    if not user or not check_password_hash(user.password_hash,password):
        return {"error":"用户名或密码错误"},401
    
    return {
        "token":"token",
        "token_type":"Bearer",
        "user":user.to_dict()
        
        },200
    
@auth_bp.route("/register",methods=["POST"])
def register():
    data = request.get_json() 

    if not data:
        return {"error":"请求体必须为json格式"},400
    username = data.get("username","").strip()
    password = data.get("password","").strip()
    
    if not username or not password:
        return {"error":"用户名和密码为必填字段"},400
    
    if len(username)<3:
        return {"error":"用户名字符小于6位"},422
    if len(password)<6:
        return {"error":"密码长度小于6"},422
    
    existing = User.query.filter_by(username=username).first()
    
    if existing:
        return {"error":"用户名已被占用"},409
    
    hash_password=generate_password_hash(password)
    
    try:
        user = User(username=username,password_hash=hash_password)
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {"error":"服务器内部错误"},500
    
    return user.to_dict(),201

@auth_bp.route("/logout",methods=["POST"])
def logout():
    return "",200

