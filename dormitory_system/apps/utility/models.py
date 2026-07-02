from django.db import models
from apps.dorm.models import Room, Building


class UtilityBill(models.Model):
    """水电账单"""
    building = models.ForeignKey(Building, on_delete=models.CASCADE, verbose_name='楼栋')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name='房间', related_name='utility_bills')
    year = models.IntegerField('年份')
    month = models.IntegerField('月份')
    UTILITY_TYPE = (
        ('electricity', '电费'),
        ('water', '水费'),
    )
    utility_type = models.CharField('费用类型', max_length=15, choices=UTILITY_TYPE)
    previous_reading = models.DecimalField('上次读数', max_digits=10, decimal_places=2, default=0)
    current_reading = models.DecimalField('本次读数', max_digits=10, decimal_places=2, default=0)
    usage = models.DecimalField('用量', max_digits=10, decimal_places=2, default=0,
                                help_text='电量(kWh)或水量(吨)')
    unit_price = models.DecimalField('单价', max_digits=8, decimal_places=4, default=0.55)
    amount = models.DecimalField('金额', max_digits=10, decimal_places=2, default=0)
    STATUS_CHOICES = (
        ('未缴纳', '未缴纳'),
        ('已缴纳', '已缴纳'),
        ('已减免', '已减免'),
    )
    status = models.CharField('状态', max_length=10, choices=STATUS_CHOICES, default='未缴纳')
    remark = models.TextField('备注', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '水电账单'
        verbose_name_plural = '水电账单管理'
        db_table = 'util_utility_bill'
        unique_together = ('room', 'year', 'month', 'utility_type')
        ordering = ['-year', '-month', 'room__room_number']

    def __str__(self):
        return f'{self.room} {self.year}年{self.month}月{self.get_utility_type_display()}'

    def save(self, *args, **kwargs):
        self.usage = self.current_reading - self.previous_reading
        self.amount = self.usage * self.unit_price
        super().save(*args, **kwargs)
