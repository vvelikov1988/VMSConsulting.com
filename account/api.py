from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import UnicodeUsernameValidator
from django.core.exceptions import ValidationError

from account.models import Account

from rest_framework.decorators import api_view

from chat.pagination import StandardResultsSetPagination
from .serializers import AccountSerializer
from .models import Account


@api_view(['GET'])
def get_users(request):
    try:
        users = Account.objects.all()
        paginator = StandardResultsSetPagination()
        result_page = paginator.paginate_queryset(users, request)
        serializer_context = {'request': request}
        serializer = AccountSerializer(result_page, many=True, context=serializer_context)
        return paginator.get_paginated_response(serializer.data)
    except Account.DoesNotExist:
        pass


def check_username_existing(request):
    username_validator = UnicodeUsernameValidator()
    try:
        user = get_object_or_404(Account, username=request.GET['picked_username'])
    except:
        user = None
    try:
        valid = username_validator(request.GET['picked_username'])
        valid = True
    except ValidationError:
        valid = None

    context = {
        'is_used': True if user else False,
        'is_valid': True if valid else False,
    }

    return JsonResponse(context, status=200)


def get_all_user(request):
    return JsonResponse(context, status=200)
