
from rest_framework import serializers


class SearchRequestSerializer(serializers.Serializer):
    # Kullanıcının aramak istediği metin
    query = serializers.CharField(
        min_length=10,
        max_length=5000
    )

    # Kaç tane emsal karar getirileceği
    top_k = serializers.IntegerField(
        default=5,
        min_value=1,
        max_value=20
    )
