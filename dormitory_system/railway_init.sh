#!/bin/bash
# ============================================================
# Railway 初始化脚本
# 在 Railway 首次部署后执行：创建超级管理员、导入初始数据
# 用法: railway run bash railway_init.sh
# ============================================================

set -e

echo "=== 1. 数据库迁移 ==="
python manage.py migrate --noinput

echo ""
echo "=== 2. 收集静态文件 ==="
python manage.py collectstatic --noinput --clear

echo ""
echo "=== 3. 创建超级管理员（如果不存在） ==="
python manage.py shell -c "
from apps.accounts.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@dormitory.com',
        password='admin123',
        role='admin',
        real_name='系统管理员'
    )
    print('✓ 超级管理员已创建: admin / admin123')
else:
    print('→ admin 用户已存在，跳过')
"

echo ""
echo "=== 4. 创建初始报修分类（如果不存在） ==="
python manage.py shell -c "
from apps.repair.models import RepairCategory
categories = ['水暖维修', '电力维修', '门窗维修', '空调维修', '网络故障', '其他']
for i, cat in enumerate(categories):
    _, created = RepairCategory.objects.get_or_create(
        name=cat, defaults={'sort_order': i + 1}
    )
    if created:
        print(f'  ✓ 创建分类: {cat}')
print('→ 报修分类初始化完成')
"

echo ""
echo "=== 5. 创建示例宿管账户（如果不存在） ==="
python manage.py shell -c "
from apps.accounts.models import User
if not User.objects.filter(username='manager1').exists():
    User.objects.create_user(
        username='manager1',
        password='123456',
        role='manager',
        real_name='张宿管',
        phone='13800001111'
    )
    print('✓ 宿管已创建: manager1 / 123456')
"

echo ""
echo "=== 6. 创建示例学生账户（如果不存在） ==="
python manage.py shell -c "
from apps.accounts.models import User
if not User.objects.filter(username='student1').exists():
    User.objects.create_user(
        username='student1',
        password='123456',
        role='student',
        real_name='李学生',
        phone='13800002222'
    )
    print('✓ 学生已创建: student1 / 123456')
"

echo ""
echo "============================================"
echo "  🎉 Railway 初始化完成！"
echo "============================================"
echo "  管理员: admin / admin123"
echo "  宿管:   manager1 / 123456"
echo "  学生:   student1 / 123456"
echo "============================================"
