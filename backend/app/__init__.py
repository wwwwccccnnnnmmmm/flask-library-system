from flask import Flask
from .config import Config
from .extensions import db

def create_app():
    
    # 核心实例
    app = Flask(__name__)
    
    # config类
    app.config.from_object(Config)
    
    # db实例绑定app实例
    db.init_app(app)    
    
    # 蓝图注册
    
    # JWT设置
    
    # 数据库初始化
    
    return app

    