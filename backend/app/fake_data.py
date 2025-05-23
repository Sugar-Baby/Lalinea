import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from faker import Faker
import random
from app import create_app, db
from app.models import User, Hobby

fake = Faker('zh_CN')

# 生成爱好
hobby_names = [f"爱好{i}" for i in range(1, 21)]

# 假设有一个Hobby模型和user_hobbies关联表，如果没有可先只生成用户
# 这里只生成用户和hobbies字段（json字符串）

def create_fake_data():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

        # 创建爱好
        hobby_objs = []
        for name in hobby_names:
            hobby = Hobby(name=name)
            db.session.add(hobby)
            hobby_objs.append(hobby)
        db.session.commit()

        # 创建用户
        users = []
        for i in range(200):
            student_id = f"{random.randint(20200000, 20209999)}"
            email = fake.email()
            name = fake.name()
            password = fake.password(length=10)
            contact = fake.phone_number()
            user = User(
                student_id=student_id,
                email=email,
                name=name,
                contact=contact
            )
            user.set_password(password)
            # 随机分配1-4个爱好
            user.hobbies = random.sample(hobby_objs, random.randint(1, 4))
            db.session.add(user)
            users.append(user)
        db.session.commit()

        # 建立用户之间的双向"认识"关系
        for user in users:
            possible_friends = [u for u in users if u != user]
            friends = random.sample(possible_friends, random.randint(2, 5))
            for friend in friends:
                if friend not in user.friends:
                    user.friends.append(friend)
                if user not in friend.friends:
                    friend.friends.append(user)
        db.session.commit()
        print("已生成200个用户、20个爱好和用户之间的关系")

if __name__ == '__main__':
    create_fake_data() 