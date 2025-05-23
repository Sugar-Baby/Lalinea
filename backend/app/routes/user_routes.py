from flask import request, jsonify
from flask_login import login_user, login_required, current_user
from .. import db
from ..models import User, Hobby, CompatibilityScore
from ..compatibility import update_compatibility_scores

def init_user_routes(app):
    # 注册接口
    @app.route('/register', methods=['POST'])
    def register():
        data = request.get_json()
        required = ['student_id', 'email', 'name', 'password']
        if not all(data.get(f) for f in required):
            return jsonify({'error': '缺少必填字段'}), 400

        # 检查学号或邮箱是否已存在
        if User.query.filter_by(student_id=data['student_id']).first():
            return jsonify({'error': '学号已存在'}), 400
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': '邮箱已存在'}), 400

        user = User(
            student_id=data['student_id'],
            email=data['email'],
            name=data['name'],
            contact=data.get('contact', '')
        )
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': '注册成功'})

    # 登录接口
    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        student_id = data.get('student_id')
        password = data.get('password')
        user = User.query.filter_by(student_id=student_id).first()
        if user and user.check_password(password):
            login_user(user)
            return jsonify({'message': '登录成功', 'name': user.name})
        return jsonify({'error': '学号或密码错误'}), 401

    # 测试保护接口
    @app.route('/protected')
    @login_required  # 确保用户已登录
    def protected():
        return jsonify({'message': '您已登录'}) 

    # 获取用户信息
    @app.route('/api/user/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        user = User.query.get_or_404(user_id)
        return jsonify({
            'id': user.id,
            'username': user.username,
            'school': user.school
            # 不返回密码等敏感信息
        })

    # 更新用户信息
    @app.route('/api/user/<int:user_id>', methods=['PUT'])
    def update_user(user_id):
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        
        if 'username' in data:
            user.username = data['username']
        
        db.session.commit()
        return jsonify({'message': '更新成功'})

    # 获取所有爱好及其拥有用户数量
    @app.route('/api/hobbies', methods=['GET'])
    def get_hobbies():
        hobbies = Hobby.query.all()
        data = [
            {
                'id': h.id,
                'name': h.name,
                'user_count': len(h.users)
            } for h in hobbies
        ]
        return jsonify(data)

    # 获取当前用户信息
    @app.route('/api/user/me', methods=['GET'])
    @login_required
    def get_me():
        user = current_user
        return jsonify({
            'student_id': user.student_id,
            'email': user.email,
            'name': user.name,
            'contact': user.contact,
            'hobbies': [h.name for h in user.hobbies]
        })

    # 更新当前用户信息（除账号外）
    @app.route('/api/user/me', methods=['PUT'])
    @login_required
    def update_me():
        user = current_user
        data = request.get_json()
        if 'email' in data:
            user.email = data['email']
        if 'name' in data:
            user.name = data['name']
        if 'contact' in data:
            user.contact = data['contact']
        db.session.commit()
        return jsonify({'message': '更新成功'})

    # 搜索用户
    @app.route('/api/users/search')
    def search_users():
        q = request.args.get('q', '')
        current_user = current_user if current_user.is_authenticated else None
        
        # 搜索用户名、学号或联系方式
        users = User.query.filter(
            (User.name.like(f'%{q}%')) |
            (User.student_id.like(f'%{q}%')) |
            (User.contact.like(f'%{q}%'))
        ).all()
        
        results = []
        for user in users:
            if current_user and user.id == current_user.id:
                continue
                
            user_data = {
                'id': user.id,
                'name': user.name,
                'student_id': user.student_id,
                'contact': user.contact if user.contact else None,
            }
            
            # 如果用户已登录，添加兼容性分数和好友关系
            if current_user:
                # 获取兼容性分数
                compatibility = CompatibilityScore.query.filter(
                    ((CompatibilityScore.user1_id == current_user.id) & 
                     (CompatibilityScore.user2_id == user.id)) |
                    ((CompatibilityScore.user1_id == user.id) & 
                     (CompatibilityScore.user2_id == current_user.id))
                ).first()
                
                # 检查是否是好友关系
                is_friend = user in current_user.friends
                
                user_data.update({
                    'compatibility_score': compatibility.score if compatibility else 0,
                    'is_friend': is_friend
                })
            
            results.append(user_data)
        
        # 如果用户已登录，按兼容性分数降序排序
        if current_user:
            results.sort(key=lambda x: x.get('compatibility_score', 0), reverse=True)
        
        return jsonify(results)

    # 模糊搜索标签
    @app.route('/api/hobbies/search')
    def search_hobbies():
        q = request.args.get('q', '')
        hobbies = Hobby.query.filter(Hobby.name.like(f'%{q}%')).all()
        return jsonify([{
            'id': h.id, 
            'name': h.name,
            'user_count': len(h.users)
        } for h in hobbies])

    # 添加新标签
    @app.route('/api/hobbies', methods=['POST'])
    @login_required
    def add_hobby():
        data = request.get_json()
        name = data.get('name')
        if not name:
            return jsonify({'error': '标签名不能为空'}), 400
        hobby = Hobby.query.filter_by(name=name).first()
        if not hobby:
            hobby = Hobby(name=name)
            db.session.add(hobby)
            db.session.commit()
        return jsonify({'id': hobby.id, 'name': hobby.name})

    # 设置/删除用户标签
    @app.route('/api/user/me/hobbies', methods=['PUT'])
    @login_required
    def set_user_hobbies():
        user = current_user
        data = request.get_json()
        hobby_names = data.get('hobbies', [])
        hobbies = Hobby.query.filter(Hobby.name.in_(hobby_names)).all()
        user.hobbies = hobbies
        db.session.commit()
        # 更新该用户的兼容性分数
        update_compatibility_scores(user)
        return jsonify({'message': '标签已更新'})

    # 添加好友关系
    @app.route('/api/user/me/friends/<int:friend_id>', methods=['POST'])
    @login_required
    def add_friend(friend_id):
        user = current_user
        friend = User.query.get_or_404(friend_id)
        
        if friend in user.friends:
            return jsonify({'message': '已经是好友关系'})
        
        user.friends.append(friend)
        friend.friends.append(user)
        db.session.commit()
        
        # 更新相关用户的兼容性分数
        update_compatibility_scores(user)
        update_compatibility_scores(friend)
        
        return jsonify({'message': '好友关系已建立'})

    # 删除好友关系
    @app.route('/api/user/me/friends/<int:friend_id>', methods=['DELETE'])
    @login_required
    def remove_friend(friend_id):
        user = current_user
        friend = User.query.get_or_404(friend_id)
        
        if friend not in user.friends:
            return jsonify({'message': '不是好友关系'})
        
        user.friends.remove(friend)
        friend.friends.remove(user)
        db.session.commit()
        
        # 更新相关用户的兼容性分数
        update_compatibility_scores(user)
        update_compatibility_scores(friend)
        
        return jsonify({'message': '好友关系已删除'})

    # 获取用户兼容性分数
    @app.route('/api/user/me/compatibility', methods=['GET'])
    @login_required
    def get_compatibility_scores():
        user = current_user
        scores = []
        
        # 获取作为user1的分数
        for score in user.compatibility_scores_as_user1:
            scores.append({
                'user_id': score.user2_id,
                'score': score.score,
                'last_updated': score.last_updated.isoformat()
            })
        
        # 获取作为user2的分数
        for score in user.compatibility_scores_as_user2:
            scores.append({
                'user_id': score.user1_id,
                'score': score.score,
                'last_updated': score.last_updated.isoformat()
            })
        
        return jsonify(scores)

    # 获取圈子信息
    @app.route('/api/circle/<int:hobby_id>', methods=['GET'])
    @login_required
    def get_circle(hobby_id):
        print(f"Fetching circle for hobby_id: {hobby_id}")  # 调试日志
        hobby = Hobby.query.get_or_404(hobby_id)
        print(f"Found hobby: {hobby.name}, ID: {hobby.id}")  # 调试日志
        
        user = current_user
        print(f"Current user: {user.name} (ID: {user.id})")  # 调试日志
        print(f"Current user's hobbies: {[h.name for h in user.hobbies]}")  # 调试日志
        
        # 获取所有拥有该标签的用户
        users = hobby.users
        print(f"Number of users with this hobby: {len(users)}")  # 调试日志
        print("Users with this hobby:")
        for u in users:
            print(f"- {u.name} (ID: {u.id})")
        
        # 更新当前用户与这些用户的兼容性分数
        for other_user in users:
            if other_user.id != user.id:
                update_compatibility_scores(other_user)
        
        # 获取所有用户的兼容性分数
        scores = []
        for other_user in users:
            if other_user.id == user.id:
                print(f"Skipping current user: {other_user.name}")  # 调试日志
                continue
                
            # 获取兼容性分数
            compatibility = CompatibilityScore.query.filter(
                ((CompatibilityScore.user1_id == user.id) & 
                 (CompatibilityScore.user2_id == other_user.id)) |
                ((CompatibilityScore.user1_id == other_user.id) & 
                 (CompatibilityScore.user2_id == user.id))
            ).first()
            
            # 检查是否是好友关系
            is_friend = other_user in user.friends
            
            user_data = {
                'id': other_user.id,
                'name': other_user.name,
                'student_id': other_user.student_id,
                'contact': other_user.contact if other_user.contact else None,
                'compatibility_score': compatibility.score if compatibility else 0,
                'is_friend': is_friend
            }
            scores.append(user_data)
        
        # 按兼容性分数降序排序
        scores.sort(key=lambda x: x['compatibility_score'], reverse=True)
        print(f"Returning {len(scores)} users")  # 调试日志
        
        response_data = {
            'hobby_name': hobby.name,
            'users': scores
        }
        print(f"Response data: {response_data}")  # 调试日志
        return jsonify(response_data) 