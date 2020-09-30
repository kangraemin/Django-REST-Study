# https://www.django-rest-framework.org/api-guide/authentication/#custom-authentication
import jwt
from django.conf import settings
from rest_framework import authentication
from rest_framework import exceptions
from users.models import User


# Custom Authentication은 실패했을때 반드시 None을 리턴해야함 위 공식문서 참조
class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        try:
            # print(request.META.get("HTTP_AUTHORIZATION"))
            token = request.META.get("HTTP_AUTHORIZATION")
            if token is None:
                return None
            # header에 X-JWT는 관습적 (convention)으로 붙인다. 다른거 붙여도 됨
            # X-JWT token 의 형태로 보내기로 약속 했다면, space로 구분해서 token을 추출 할 수 있음
            # 만약 안된다면 ( ValueError ) => 잘못 보낸거
            xjwt, jwt_token = token.split(" ")
            # print(xjwt, jwt_token)
            # 올바른 jwt_token이 오지 않았다면, decode 도중에 except를 발생시킴
            decoded = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=["HS256"])
            # print(decoded)
            pk = decoded.get("pk")
            # print(pk)
            user = User.objects.get(pk=pk)
            # 공식문서를 보면 이렇게 return 하라고 나와있음
            return (user, None)
        except (ValueError, User.DoesNotExist):
            return None
        except jwt.exceptions.DecodeError:
            raise exceptions.AuthenticationFailed(detail="JWT Format Invalid")
