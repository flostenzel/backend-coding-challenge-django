import json

from authors.models import Author
from django_webtest import WebTest
from django_webtest.response import DjangoWebtestResponse
from model_bakery import baker
from rest_framework.authtoken.models import Token

# pylint: disable=keyword-arg-before-vararg, dangerous-default-value


class APIViewTest(WebTest):
    csrf_checks = False
    auth = True

    def setUp(self):
        if self.auth:
            self.auth_user = baker.make(Author)
            self.token = Token.objects.get(user=self.auth_user)

    def post(self, url, data=[], auth=None, headers={}, *args, **kwargs) -> DjangoWebtestResponse:
        auth = auth if auth is not None else self.auth
        if auth:
            return self.app.post(
                url=url,
                params=json.dumps(data),
                headers={"Authorization": f"Token {self.token.key}", **headers},
                user=self.auth_user,
                content_type="application/json",
                *args,
                **kwargs,
            )
        return self.app.post(
            url=url,
            params=json.dumps(data),
            content_type="application/json",
            headers=headers,
            *args,
            **kwargs,
        )

    def delete(self, url, auth=None, headers={}, *args, **kwargs) -> DjangoWebtestResponse:
        auth = auth if auth is not None else self.auth
        if auth:
            return self.app.delete(
                url=url,
                headers={"Authorization": f"Token {self.token.key}", **headers},
                user=self.auth_user,
                *args,
                **kwargs,
            )
        return self.app.delete(url=url, headers=headers, *args, **kwargs)

    def patch(self, url, data, auth=None, headers={}, *args, **kwargs):
        auth = auth if auth is not None else self.auth
        if auth:
            return self.app.patch(
                url=url,
                params=json.dumps(data),
                headers={"Authorization": f"Token {self.token.key}", **headers},
                user=self.auth_user,
                content_type="application/json",
                *args,
                **kwargs,
            )
        return self.app.patch(
            url=url,
            params=json.dumps(data),
            content_type="application/json",
            headers=headers,
            *args,
            **kwargs,
        )

    def get(self, url, auth=None, headers={}, *args, **kwargs):
        auth = auth if auth is not None else self.auth
        if auth:
            return self.app.get(
                url=url,
                headers={"Authorization": f"Token {self.token.key}", **headers},
                user=self.auth_user,
                *args,
                **kwargs,
            )
        return self.app.get(url=url, headers=headers, *args, **kwargs)
