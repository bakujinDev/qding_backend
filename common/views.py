from django.shortcuts import render


def check_owner(request, compare_with_user):
    if compare_with_user != request.user:
        raise PermissionDenied
