from collections import defaultdict
from typing import List, Set, Dict, Tuple
from .models import User, Hobby, CompatibilityScore
from . import db
from datetime import datetime

# 学科相关度矩阵
SUBJECT_RELATEDNESS = {
    # 红色框内学科
    'red': {
        '计算机科学': {'计算机科学': 1.0, '软件工程': 0.7, '人工智能': 0.7},
        '软件工程': {'计算机科学': 0.7, '软件工程': 1.0, '人工智能': 0.7},
        '人工智能': {'计算机科学': 0.7, '软件工程': 0.7, '人工智能': 1.0},
    },
    # 橙色框内学科
    'orange': {
        '数学': {'数学': 1.0, '统计学': 0.5, '物理学': 0.5},
        '统计学': {'数学': 0.5, '统计学': 1.0, '物理学': 0.5},
        '物理学': {'数学': 0.5, '统计学': 0.5, '物理学': 1.0},
    },
    # 绿色框内学科
    'green': {
        '化学': {'化学': 1.0, '生物学': 0.3, '医学': 0.3},
        '生物学': {'化学': 0.3, '生物学': 1.0, '医学': 0.3},
        '医学': {'化学': 0.3, '生物学': 0.3, '医学': 1.0},
    }
}

def get_subject_relatedness(subject1: str, subject2: str) -> float:
    """计算两个学科之间的相关度"""
    for group in SUBJECT_RELATEDNESS.values():
        if subject1 in group and subject2 in group:
            return group[subject1][subject2]
    return 0.0

def calculate_hobby_overlap(user1_hobbies: Set[str], user2_hobbies: Set[str]) -> float:
    """计算两个用户爱好重合度"""
    if not user1_hobbies or not user2_hobbies:
        return 0.0
    intersection = len(user1_hobbies.intersection(user2_hobbies))
    union = len(user1_hobbies.union(user2_hobbies))
    return intersection / union

def calculate_subject_relatedness(user1_hobbies: Set[str], user2_hobbies: Set[str]) -> float:
    """计算两个用户学科相关度"""
    max_relatedness = 0.0
    for hobby1 in user1_hobbies:
        for hobby2 in user2_hobbies:
            relatedness = get_subject_relatedness(hobby1, hobby2)
            max_relatedness = max(max_relatedness, relatedness)
    return max_relatedness

def find_shortest_path(user1: User, user2: User) -> int:
    """使用BFS找到两个用户之间的最短路径长度"""
    if user1 == user2:
        return 0
    
    visited = {user1.id}
    queue = [(user1, 0)]  # (user, distance)
    
    while queue:
        current_user, distance = queue.pop(0)
        
        for friend in current_user.friends:
            if friend.id == user2.id:
                return distance + 1
            
            if friend.id not in visited:
                visited.add(friend.id)
                queue.append((friend, distance + 1))
    
    return float('inf')  # 如果没有找到路径

def calculate_compatibility(user1: User, user2: User) -> float:
    """计算两个用户之间的兼容性分数"""
    # 确保user1.id < user2.id
    if user1.id > user2.id:
        user1, user2 = user2, user1
    
    # 计算爱好重合度
    hobby_overlap = calculate_hobby_overlap(
        {h.name for h in user1.hobbies},
        {h.name for h in user2.hobbies}
    )
    
    # 计算学科相关度
    subject_relatedness = calculate_subject_relatedness(
        {h.name for h in user1.hobbies},
        {h.name for h in user2.hobbies}
    )
    
    # 计算关系距离
    distance = find_shortest_path(user1, user2)
    # 显式处理无穷大的情况
    distance_factor = 0.5 / distance if distance != float('inf') else 0
    
    # 计算最终分数
    score = hobby_overlap * 0.25 + subject_relatedness * 0.25 + distance_factor
    
    return score

def update_compatibility_scores(user: User = None):
    """更新兼容性分数
    
    如果提供了user参数，只更新该用户与其他用户的兼容性分数
    否则更新所有用户之间的兼容性分数
    """
    if user:
        # 只更新指定用户的兼容性分数
        other_users = User.query.filter(User.id != user.id).all()
        for other_user in other_users:
            score = calculate_compatibility(user, other_user)
            update_or_create_score(user, other_user, score)
    else:
        # 更新所有用户之间的兼容性分数
        users = User.query.all()
        for i in range(len(users)):
            for j in range(i + 1, len(users)):
                score = calculate_compatibility(users[i], users[j])
                update_or_create_score(users[i], users[j], score)
    
    db.session.commit()

def update_or_create_score(user1: User, user2: User, score: float):
    """更新或创建兼容性分数记录"""
    if user1.id > user2.id:
        user1, user2 = user2, user1
    
    compatibility = CompatibilityScore.query.filter_by(
        user1_id=user1.id,
        user2_id=user2.id
    ).first()
    
    if compatibility:
        compatibility.score = score
        compatibility.last_updated = datetime.utcnow()
    else:
        compatibility = CompatibilityScore(
            user1_id=user1.id,
            user2_id=user2.id,
            score=score
        )
        db.session.add(compatibility) 