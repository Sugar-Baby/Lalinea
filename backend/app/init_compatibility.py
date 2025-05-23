import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.compatibility import update_compatibility_scores

def init_compatibility_scores():
    """初始化所有用户之间的兼容性分数"""
    app = create_app()
    with app.app_context():
        # 更新所有用户之间的兼容性分数
        update_compatibility_scores()
        print("已初始化所有用户之间的兼容性分数")

if __name__ == '__main__':
    init_compatibility_scores() 