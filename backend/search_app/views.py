
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import SearchRequestSerializer
from backend.services.search_service import search_decisions_service


@api_view(["POST"])
def search_decisions(request):
    serializer = SearchRequestSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    query = serializer.validated_data["query"]
    top_k = serializer.validated_data["top_k"]

    result = search_decisions_service(query, top_k)
    #serializer a kontrol ettirdik veriler doğruysa search_service.py ye gönderir.
    return Response(result, status=status.HTTP_200_OK)
