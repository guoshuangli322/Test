from django.db import models
from django.conf import settings
from apps.dorm.models import Bed, Room, Building


class Student(models.Model):
    """学生基本信息（扩展自User，一对一关联）"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        verbose_name='关联账户', related_name='student_profile'
    )
    student_id = models.CharField('学号', max_length=20, unique=True)
    real_name = models.CharField('姓名', max_length=50)
    gender = models.CharField('性别', max_length=4, choices=(('男', '男'), ('女', '女')))
    class_name = models.CharField('班级', max_length=100, blank=True)
    college = models.CharField('学院', max_length=100, blank=True)
    phone = models.CharField('手机号', max_length=11, blank=True)
    parent_phone = models.CharField('家长电话', max_length=11, blank=True)
    STATUS_CHOICES = (
        ('在校', '在校'), ('毕业', '毕业'), ('退学', '退学'), ('离校', '离校'),
    )
    status = models.CharField('状态', max_length=10, choices=STATUS_CHOICES, default='在校')
    enroll_date = models.DateField('入学日期', null=True, blank=True)
    remark = models.TextField('备注', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '学生'
        verbose_name_plural = '学生管理'
        db_table = 'stu_student'
        ordering = ['student_id']

    def __str__(self):
        return f'{self.real_name}({self.student_id})'

    def get_current_bed(self):
        """获取当前床位"""
        record = self.dorm_records.filter(status='入住中').first()
        return record.bed if record else None

    def get_current_room(self):
        """获取当前房间"""
        bed = self.get_current_bed()
        return bed.room if bed else None


class DormitoryRecord(models.Model):
    """住宿记录（入住/调宿/退宿）"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='学生', related_name='dorm_records')
    bed = models.ForeignKey(Bed, on_delete=models.CASCADE, verbose_name='床位', related_name='records')
    STATUS_CHOICES = (
        ('入住中', '入住中'),
        ('已调宿', '已调宿'),
        ('已退宿', '已退宿'),
    )
    status = models.CharField('状态', max_length=10, choices=STATUS_CHOICES, default='入住中')
    checkin_date = models.DateTimeField('入住时间', auto_now_add=True)
    checkout_date = models.DateTimeField('退宿时间', null=True, blank=True)
    OPERATION_CHOICES = (
        ('入住', '入住'),
        ('调宿', '调宿'),
        ('退宿', '退宿'),
    )
    operation_type = models.CharField('操作类型', max_length=10, choices=OPERATION_CHOICES, default='入住')
    operator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        verbose_name='操作人', related_name='dorm_operations'
    )
    reason = models.TextField('原因/备注', blank=True)

    class Meta:
        verbose_name = '住宿记录'
        verbose_name_plural = '住宿记录'
        db_table = 'stu_dormitory_record'
        ordering = ['-checkin_date']

    def __str__(self):
        return f'{self.student.real_name} - {self.bed} - {self.status}'
