from authors.models import Author
from authors.serializers import SignUpSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny


class SignUpAuthorView(CreateAPIView):
    """
    POST: Create a new Author
    required data: username, password
    """
    queryset = Author.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer
