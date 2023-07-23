from rest_framework import serializers


class SMSRequestSerializer(serializers.Serializer):
    to_number = serializers.CharField(max_length=15)
    message = serializers.CharField(max_length=160)
