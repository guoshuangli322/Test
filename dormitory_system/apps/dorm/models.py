from django.db import models
from django.conf import settings


class Building(models.Model):
    """楼栋"""
    name = models.CharField('楼栋名称', max_length=50, unique=True)
    code = models.CharField('楼栋编号', max_length=10, unique=True, help_text='例如 A1, B2')
    floors = models.IntegerField('楼层数', default=6)
    GENDER_CHOICES = (('male', '男生楼'), ('female', '女生楼'), ('mixed', '混合楼'))
    gender_type = models.CharField('类型', max_length=10, choices=GENDER_CHOICES, default='male')
    address = models.CharField('地址', max_length=200, blank=True)
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='宿管', limit_choices_to={'role': 'manager'}
    )
    description = models.TextField('备注', blank=True)
    is_active = models.BooleanField('启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '楼栋'
        verbose_name_plural = '楼栋管理'
        db_table = 'dorm_building'
        ordering = ['code']

    def __str__(self):
        return f'{self.name}({self.code})'


class Room(models.Model):
    """房间"""
    building = models.ForeignKey(Building, on_delete=models.CASCADE, verbose_name='所属楼栋', related_name='rooms')
    room_number = models.CharField('房间号', max_length=20)
    ROOM_TYPE_CHOICES = (
        ('四人寝', '四人寝'), ('六人寝', '六人寝'), ('八人寝', '八人寝'), ('二人寝', '二人寝'),
    )
    room_type = models.CharField('房型', max_length=10, choices=ROOM_TYPE_CHOICES, default='四人寝')
    bed_count = models.IntegerField('床位总数', default=4)
    floor = models.IntegerField('所在楼层')
    is_active = models.BooleanField('启用', default=True)
    remark = models.CharField('备注', max_length=200, blank=True)

    class Meta:
        verbose_name = '房间'
        verbose_name_plural = '房间管理'
        db_table = 'dorm_room'
        unique_together = ('building', 'room_number')
        ordering = ['building__code', 'floor', 'room_number']

    def __str__(self):
        return f'{self.building.code}-{self.room_number}'

    def occupied_bed_count(self):
        """已入住床位数"""
        return self.beds.filter(status='已入住').count()

    def available_bed_count(self):
        """空闲床位数"""
        return self.beds.filter(status='空闲').count()

    def is_full(self):
        """是否已住满"""
        return self.occupied_bed_count() >= self.bed_count


class Bed(models.Model):
    """床位"""
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name='所属房间', related_name='beds')
    bed_number = models.CharField('床位号', max_length=10, help_text='例如 1号床, A床')
    BED_STATUS = (
        ('空闲', '空闲'), ('已入住', '已入住'), ('维修中', '维修中'),
    )
    status = models.CharField('状态', max_length=10, choices=BED_STATUS, default='空闲')

    class Meta:
        verbose_name = '床位'
        verbose_name_plural = '床位管理'
        db_table = 'dorm_bed'
        unique_together = ('room', 'bed_number')
        ordering = ['room', 'bed_number']

    def __str__(self):
        return f'{self.room}-{self.bed_number}'
