from django.shortcuts import render


def check_owner(request, compare_with_user):
    if compare_with_user != request.user:
        raise PermissionDenied


def get_page(request):
    try:
        page = request.query_params.get("page", 1)
        page = int(page)
    except ValueError:
        page = 1
    return page
