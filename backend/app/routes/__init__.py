from .user_routes import init_user_routes

def init_all_routes(app):
    """初始化所有路由"""
    init_user_routes(app) 