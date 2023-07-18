from authors.models import Author
from rest_framework import serializers


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"
