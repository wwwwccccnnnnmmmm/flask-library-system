import os

class Config:
    
    # 密钥
    SECRET_KEY = os.environ.get("SECRET_KEY","dev-secret-key")
    
    # sqlite数据库名
    DB_NAME = os.environ.get("DB_NAME","app.db")
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL",f"sqlite:///{DB_NAME}")
    
    # 关闭数据对象修改追踪
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT令牌时效
    JWT_EXPIRATION_HOURS = 24
    
    