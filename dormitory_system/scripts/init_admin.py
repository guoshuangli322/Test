"""初始化管理员账户（在 Railway Shell 中运行）"""
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dormitory.settings")
django.setup()

from apps.accounts.models import User

# 创建超级管理员
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser(
        username="admin",
        email="admin@dormitory.com",
        password="admin123",
        role="admin",
        real_name="系统管理员",
    )
    print("✓ 超级管理员: admin / admin123")
else:
    print("→ admin 已存在")

# 创建宿管
if not User.objects.filter(username="manager1").exists():
    User.objects.create_user(
        username="manager1",
        password="123456",
        role="manager",
        real_name="张宿管",
        phone="13800001111",
    )
    print("✓ 宿管账户: manager1 / 123456")
else:
    print("→ manager1 已存在")

# 创建学生
if not User.objects.filter(username="student1").exists():
    User.objects.create_user(
        username="student1",
        password="123456",
        role="student",
        real_name="李学生",
        phone="13800002222",
    )
    print("✓ 学生账户: student1 / 123456")
else:
    print("→ student1 已存在")

print("\n初始化完成！")