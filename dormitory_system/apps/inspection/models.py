from django.db import models
from django.conf import settings
from apps.dorm.models import Building, Room


class HygieneInspection(models.Model):
    """卫生检查记录"""
    building = models.ForeignKey(Building, on_delete=models.CASCADE, verbose_name='楼栋')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name='房间')
    inspector = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='检查人'
    )
    SCORE_CHOICES = [(i, f'{i}分') for i in range(1, 11)]
    score = models.IntegerField('评分', choices=SCORE_CHOICES, default=8)
    GRADE_CHOICES = (
        ('优秀', '优秀'), ('良好', '良好'), ('合格', '合格'), ('不合格', '不合格'),
    )
    grade = models.CharField('等级', max_length=10, choices=GRADE_CHOICES, default='良好')
    comment = models.TextField('检查评语', blank=True)
    images = models.ImageField('照片', upload_to='inspection/', blank=True)
    check_date = models.DateField('检查日期', auto_now_add=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '卫生检查'
        verbose_name_plural = '卫生检查记录'
        db_table = 'ins_hygiene_inspection'
        ordering = ['-check_date', '-created_at']

    def __str__(self):
        return f'{self.room} {self.check_date} {self.grade}'

    def save(self, *args, **kwargs):
        if self.score >= 9:
            self.grade = '优秀'
        elif self.score >= 7:
            self.grade = '良好'
        elif self.score >= 5:
            self.grade = '合格'
        else:
            self.grade = '不合格'
        super().save(*args, **kwargs)
