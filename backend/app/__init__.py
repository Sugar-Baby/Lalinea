from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS

db = SQLAlchemy()
login_manager = LoginManager()

# 必须在db定义后注册user_loader
from .models import User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    
    # 配置CORS - 使用更简单的配置
    CORS(app, 
         origins=["http://localhost:3000"],
         allow_credentials=True,
         supports_credentials=True,
         resources={r"/*": {
             "origins": ["http://localhost:3000"],
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
             "allow_headers": ["Content-Type", "Authorization", "Accept"],
             "expose_headers": ["Content-Type", "Authorization"],
             "supports_credentials": True
         }})
    
    # 配置数据库
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lalinea.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your-secret-key'  # 请更改为安全的密钥
    
    # 初始化扩展
    db.init_app(app)
    login_manager.init_app(app)
    
    # 注册路由
    from .routes import init_all_routes
    init_all_routes(app)
    
    # 创建数据库表
    with app.app_context():
        db.create_all()
    
    return app
