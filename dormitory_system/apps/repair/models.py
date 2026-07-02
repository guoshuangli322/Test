from django.db import models
from django.conf import settings
from apps.dorm.models import Building, Room


class RepairCategory(models.Model):
    """报修分类"""
    name = models.CharField('分类名称', max_length=50, unique=True)
    sort_order = models.IntegerField('排序', default=0)

    class Meta:
        verbose_name = '报修分类'
        verbose_name_plural = '报修分类'
        db_table = 'repair_category'
        ordering = ['sort_order']

    def __str__(self):
        return self.name


class RepairOrder(models.Model):
    """报修工单"""
    order_no = models.CharField('工单编号', max_length=30, unique=True, editable=False)
    title = models.CharField('报修标题', max_length=200)
    category = models.ForeignKey(RepairCategory, on_delete=models.SET_NULL, null=True, verbose_name='分类')
    building = models.ForeignKey(Building, on_delete=models.SET_NULL, null=True, verbose_name='楼栋')
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, verbose_name='房间')
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        verbose_name='报修人', related_name='repair_orders'
    )
    description = models.TextField('问题描述')
    images = models.ImageField('图片', upload_to='repair/', blank=True)
    contact_phone = models.CharField('联系电话', max_length=11, blank=True)

    STATUS_CHOICES = (
        ('待处理', '待处理'),
        ('处理中', '处理中'),
        ('已完成', '已完成'),
        ('已关闭', '已关闭'),
    )
    status = models.CharField('状态', max_length=10, choices=STATUS_CHOICES, default='待处理')

    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='指派人', related_name='assigned_repairs'
    )
    handler_note = models.TextField('处理意见', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    completed_at = models.DateTimeField('完成时间', null=True, blank=True)

    class Meta:
        verbose_name = '报修工单'
        verbose_name_plural = '报修工单'
        db_table = 'repair_order'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.order_no} - {self.title}'

    def save(self, *args, **kwargs):
        if not self.order_no:
            import datetime
            prefix = f'BX{datetime.date.today().strftime("%Y%m%d")}'
            last = RepairOrder.objects.filter(order_no__startswith=prefix).order_by('-id').first()
            seq = (last.id + 1) if last else 1
            self.order_no = f'{prefix}{seq:04d}'
        super().save(*args, **kwargs)
