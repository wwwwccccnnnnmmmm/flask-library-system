from flask import Flask
from .config import Config
from .extensions import db
from .cli import init_app as init_cli
from .api.v1 import user_bp,order_bp,book_bp,auth_bp

def create_app():
    
    # 核心实例
    app = Flask(__name__)
    
    # config类
    app.config.from_object(Config)
    
    # db实例绑定app实例
    db.init_app(app)    
    
    # 蓝图注册
    app.register_blueprint(auth_bp,url_prefix='/api/v1/auth')
    app.register_blueprint(order_bp,url_prefix='/api/v1/orders')
    app.register_blueprint(user_bp,url_prefix='/api/v1/users')
    app.register_blueprint(book_bp,url_prefix='/api/v1/books')
    
    # JWT设置
    
    # 数据库初始化
    init_cli(app)
    
    return app

    