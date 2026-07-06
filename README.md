# 图书管理系统
目的：实现图书的管理，并作为自己实现的项目

## 1.项目目标
实现一个图书管理系统，包含用户认证，书籍管理、用户管理等功能

## 2.技术栈
python3.xx Flask Flask-SQLAlmy（ORM映射） SQLite数据库） pyJWT（用户认证）

## 3.功能开发路径图

### 3.1 环境搭建
    [√] 虚拟环境
    [√] 安装依赖
    [√] 搭建flask框架
    
### 3.2 用户认证功能
    [] 登录功能     GET     /auth/login
    [] 注册功能     POST    /auth/register 
    [] 登出功能     GET    /auth/logout
    [] 个人资料     GET     /auth/me

### 3.3 书籍管理功能
    [] 添加书籍     GET     /books
    [] 修改书籍     PATCH    /books/<id> 
    [] 删除书籍     DELETE    /books/<id> 
    [] 查找单个书籍  GET    /books/<id> 
    [] 查找多个书籍  GET    /books
    
### 3.4 用户管理功能
    [] 添加用户     GET     /users
    [] 修改用户     PATCH    /users/<id> 
    [] 删除用户     DELETE    /users/<id> 
    [] 查找单个用户  GET    /users/<id> 
    [] 查找多个用户  GET    /users
    
### 3.5 借阅订单功能
    [] 添加订单     GET     /orders
    [] 修改订单     PATCH    /orders/<id> 
    [] 删除订单     DELETE    /orders/<id> 
    [] 查找单个订单  GET    /books/<id> 
    [] 查找多个订单  GET    /orders
    

