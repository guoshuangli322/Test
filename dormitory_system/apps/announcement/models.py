from django.db import models
from django.conf import settings


class Announcement(models.Model):
    """公告"""
    title = models.CharField('标题', max_length=200)
    content = models.TextField('内容')
    CATEGORY_CHOICES = (
        ('system', '系统通知'),
        ('dorm', '宿舍通知'),
        ('repair', '维修通知'),
        ('other', '其他'),
    )
    category = models.CharField('分类', max_length=10, choices=CATEGORY_CHOICES, default='dorm')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='发布人'
    )
    is_pinned = models.BooleanField('置顶', default=False)
    is_active = models.BooleanField('发布', default=True)
    views = models.IntegerField('浏览次数', default=0)
    created_at = models.DateTimeField('发布时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '公告'
        verbose_name_plural = '公告管理'
        db_table = 'announcement'
        ordering = ['-is_pinned', '-created_at']

    def __str__(self):
        return self.title
