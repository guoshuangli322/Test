def current_user(request):
    """传递当前用户信息到所有模板"""
    if request.user.is_authenticated:
        return {
            'current_role': request.user.get_role_display(),
            'is_super_admin': request.user.is_super_admin(),
            'is_manager': request.user.is_manager(),
            'is_student_user': request.user.is_student(),
        }
    return {}
