import click
from werkzeug.security import generate_password_hash
from datetime import datetime

from app.extensions import db
from app.models import User,Book,Profile

@click.command('init-db')
def init_db_command():
    """清空数据库，重建表结构并插入测试数据。"""
    click.echo(" 正在删除旧表...")
    db.drop_all()
    click.echo(" 正在创建新表...")
    db.create_all()

    # ---- 插入测试数据 ----
    # 1. 创建管理员
    admin = User(
        username='admin',
        password_hash=generate_password_hash('admin123'),
        role='admin',
        is_active=True
    )

    # 3. 为 admin 创建 Profile
    admin.profile = Profile(
        real_name='管理员',
        phone='13800138000',
        employee_id='EMP001',
    )
    db.session.add(admin)
    
    # 2. 创建普通用户
    zhangsan = User(
        username='zhangsan',
        password_hash=generate_password_hash('zhangsan123'),
        role='customer',
        is_active=True
    )
    
    zhangsan.profile = Profile(
        real_name='张三',
        phone='13800138001',
        employee_id='EMP002',
    )
    
    db.session.add(zhangsan)

 
    # 4. 添加几个书籍
    book1 = Book(book_name='斗罗大陆', price=58.0, book_count=20,description='唐家三少经典玄幻小说',)
    book2 = Book(book_name='斗破苍穹', price=68.0, book_count=15, description='天蚕土豆代表作',)
    book3 = Book(book_name='元尊', price=28.0, book_count=30,description='天蚕土豆新作',)
    book4 =Book(book_name='仙逆', price=18.0, book_count=50,description='耳根经典修真小说',)
   
    db.session.add_all([book1, book2, book3, book4])

    # 提交所有数据
    db.session.commit()

# ---------- 注册命令到 Flask 应用 ----------
def init_app(app):
    """将自定义命令添加到 Flask CLI 中。"""
    app.cli.add_command(init_db_command)