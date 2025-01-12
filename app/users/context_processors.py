def user_context(request):
    return {
        'moderator': request.user.groups.filter(name='moderator').exists() if request.user.is_authenticated else False
    }