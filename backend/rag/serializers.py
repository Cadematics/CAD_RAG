from rest_framework import serializers

class QuerySerializer(serializers.Serializer):
    query = serializers.CharField()
    domain = serializers.CharField(required=False, allow_blank=True)
    top_k = serializers.IntegerField(default=5)
    debug = serializers.BooleanField(default=False)
