from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    自定义用户模型，支持三种角色：
    - admin     超级管理员
    - manager   宿管
    - student   学生
    """
    ROLE_CHOICES = (
        ('admin', '超级管理员'),
        ('manager', '宿管'),
        ('student', '学生'),
    )
    role = models.CharField('角色', max_length=10, choices=ROLE_CHOICES, default='student')
    phone = models.CharField('手机号', max_length=11, blank=True)
    real_name = models.CharField('真实姓名', max_length=50, blank=True)
    avatar = models.ImageField('头像', upload_to='avatars/', blank=True)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户管理'
        db_table = 'sys_user'

    def __str__(self):
        return f'{self.get_role_display()} - {self.get_display_name()}'

    def get_display_name(self):
        return self.real_name or self.username

    def is_super_admin(self):
        return self.role == 'admin' or self.is_superuser

    def is_manager(self):
        return self.role == 'manager'

    def is_student(self):
        return self.role == 'student'
