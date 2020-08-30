from rest_framework.decorators import api_view

from .pagination import StandardResultsSetPagination
from .serializer import ChatMessagesSerializer
from .models import Thread, ChatMessage


@api_view(['GET'])
def message_fetcher(request):
    try:
        q1 = request.GET.get('sender')
        q2 = request.GET.get('receiver')
        try:
            _thread = Thread.objects.get(first__username=q1, second__username=q2)
        except:
            _thread = Thread.objects.get(first__username=q2, second__username=q1)
        messages = ChatMessage.objects.filter(thread=_thread).order_by('-timestamp')
        paginator = StandardResultsSetPagination()
        result_page = paginator.paginate_queryset(messages, request)
        serializer_context = {'request': request}
        serializer = ChatMessagesSerializer(result_page, many=True, context=serializer_context)
        return paginator.get_paginated_response(serializer.data)
    except Thread.DoesNotExist:
        pass
