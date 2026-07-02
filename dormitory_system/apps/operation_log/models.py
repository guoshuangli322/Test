from django.db import models
from django.conf import settings


class OperationLog(models.Model):
    """操作日志"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        verbose_name='操作人', blank=True
    )
    username = models.CharField('用户名', max_length=150, blank=True)
    action = models.CharField('操作', max_length=200, help_text='描述用户执行的操作')
    module = models.CharField('功能模块', max_length=50, blank=True)
    ip_address = models.GenericIPAddressField('IP地址', blank=True, null=True)
    request_method = models.CharField('请求方法', max_length=10, blank=True)
    request_path = models.CharField('请求路径', max_length=500, blank=True)
    detail = models.TextField('详情', blank=True)
    created_at = models.DateTimeField('操作时间', auto_now_add=True)

    class Meta:
        verbose_name = '操作日志'
        verbose_name_plural = '操作日志'
        db_table = 'log_operation'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.username} - {self.action} - {self.created_at}'
