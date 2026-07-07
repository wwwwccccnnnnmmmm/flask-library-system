from flask import Blueprint,request
from werkzeug.security import generate_password_hash,check_password_hash
from ...models import User,Profile
from ...extensions import db

user_bp = Blueprint('user',__name__)

@user_bp.route("",methods=["POST"])
def create_user():
    data = request.get_json()
    
    if not data:
        return {"error":"请求体必须为json格式"},400
    
    username = data.get("username","").strip()
    password = data.get("password","").strip()
    
    if not username or not password:
        return {"error":"用户名和密码不能为空"},400

    if len(username)<3:
        return {"error":"用户名字符少于三位"},422
    if len(password)<6:
        return {"error":"密码长度不得小于6"},422
    
    existing = User.query.filter_by(username=username).first()
    if existing:
        return {"error":"该用户名已被注册"},409
    hash_password = generate_password_hash(password)

    try:
        user = User(username=username,password_hash=hash_password,is_active=True)
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {"error":"服务器内部错误"},500
    
    return user.to_dict(),201


@user_bp.route("/<int:user_id>",methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return {"error":"资源不存在"},404
    
    try:
        db.session.delete(user)
        db.session.commit()
    
    except Exception as e:
        db.session.rollback()
        return {"error":"服务器内部错误"},500
    
    return "",204

@user_bp.route("/<int:user_id>",methods=["PATCH"])
def update_user(user_id):
    user = User.query.get(user_id)
     
    if not user:
        return {"error":"资源不存在"},404
    
    data = request.get_json()
    
    if 'username' in data:
        new_name = data["username"].strip()
        existing = User.query.filter(User.username==new_name,User.id!=user_id).first()
        if existing:
            return {"error":"该用户名已存在"},409
        user.username=new_name
    
    if 'password' in data:
        new_password =data["password"].strip()
        
        if len(new_password)<6:
            return {"error":"密码长度不得小于6位"},422
        is_same = check_password_hash(user.password_hash,new_password)
        
        if is_same:
            return {"error":"修改密码与原密码相同"},409
        user.password_hash = generate_password_hash(new_password)

    if 'role' in data:
        new_role = data["role"].strip()
        user.role = new_role
        
    if 'real_name' in data or 'email' in data or 'phone' in data or 'description' in data:
        
        if not user.profile:
           user.profile = Profile()
        
        if 'real_name' in data:
            new_real_name = data["real_name"].strip()
            is_same = Profile.query.filter(Profile.real_name==new_real_name,Profile.user_id!=user_id).first()
            
            if is_same:
                return {"error":"该用户名已存在"},409
            user.profile.real_name = new_real_name
        
        if 'email' in data:
            new_email = data["email"].strip()
            is_same = Profile.query.filter(Profile.email==new_email,Profile.user_id!=user_id).first()
            
            if is_same:
                return {"error":"该邮箱已存在"},409
            user.profile.email = new_email
        
        if 'phone' in data:
            new_phone = data["phone"].strip()
            is_same = Profile.query.filter(Profile.phone==new_phone,Profile.user_id!=user_id).first()
            
            if is_same:
                return {"error":"该手机号已存在"},409
            user.profile.phone = new_phone
        if 'description' in data:
            new_description = data["description"].strip()
            
            user.profile.description = new_description

    try:
        db.session.commit()
    except Exception as e:
        return {"error":"服务器内部错误"},500
    
    return user.to_dict(),200
    
@user_bp.route("/<int:user_id>",methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id) 
    if not user:
        
        return {"error":"资源不存在"},404
    return user.to_dict(),200

@user_bp.route("",methods=["GET"])
def get_users():
    
    page = request.args.get("page",1,type=int)
    per_page = request.args.get("per_page",10,type=int)
    
    keyword = request.args.get("keyword","").strip()
    role = request.args.get("role","").strip()
    is_active_str = request.args.get("is_active")
    
    query = User.query
    if keyword:
        query = query.filter(User.username.contains(keyword))
    
    if is_active_str is not None:
        is_active = is_active_str.lower() in ('true',"1")
        query = query.filter_by(is_active=is_active)
    
    if role:
        query = query.filter_by(role=role)
    
    paginated = query.order_by(User.id.desc()).paginate(page=page,per_page=per_page,error_out=False)
    
    return {
        "items":[user.to_dict() for user in paginated.items],
        "total":paginated.total,
        "page":page,
        "per_page":per_page,
        "pages":paginated.pages,
        "has_next":paginated.has_next,
        "has_prev":paginated.has_prev
    }
    
