def user_def(request):
    user = request.user
    ctx = {
        "user": user,
    }
    return ctx