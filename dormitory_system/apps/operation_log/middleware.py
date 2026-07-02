from django.utils import timezone
from .models import OperationLog


class OperationLogMiddleware:
    """
    操作日志中间件 — 记录所有POST/PUT/DELETE请求（敏感操作）。
    在 settings.MIDDLEWARE 中已注册。
    """
    EXEMPT_PATHS = ['/admin/', '/accounts/login/', '/accounts/logout/']

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # 只记录已认证用户的修改操作
        if (request.user.is_authenticated
                and request.method in ('POST', 'PUT', 'PATCH', 'DELETE')
                and not any(request.path.startswith(p) for p in self.EXEMPT_PATHS)):
            try:
                # 构建操作描述
                action_map = {
                    'POST': '新增/提交',
                    'PUT': '更新',
                    'PATCH': '部分更新',
                    'DELETE': '删除',
                }
                action = f'{action_map.get(request.method, request.method)} #{request.path}'
                # 从request中获取模块名（URL第一个path段）
                path_parts = request.path.strip('/').split('/')
                module = path_parts[0] if path_parts else ''

                OperationLog.objects.create(
                    user=request.user,
                    username=request.user.username,
                    action=action,
                    module=module,
                    ip_address=self.get_client_ip(request),
                    request_method=request.method,
                    request_path=request.path,
                    detail=request.POST.get('reason', '') or request.POST.get('handler_note', '') or '',
                )
            except Exception:
                pass  # 日志记录偶发失败不影响主流程

        return response

    @staticmethod
    def get_client_ip(request):
        xff = request.META.get('HTTP_X_FORWARDED_FOR')
        if xff:
            return xff.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')
