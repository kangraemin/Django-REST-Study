from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import User
from .serializers import RelatedUserSerializer, ReadUserSerializer, WriteUserSerializer


class MeView(APIView):

    # Permission classes 를 통해 접근 가능한지 안한지를 알아서 체크 해줌
    # 클래스 전체 메소드에 영향을 줌
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # if request.user.is_authenticated:
        #     return Response(ReadUserSerializer(request.user).data)
        return Response(ReadUserSerializer(request.user).data)

    def put(self, request):
        serializer = WriteUserSerializer(request.user, data=request.data, partial=True)
        print(serializer.is_valid())
        if serializer.is_valid():
            serializer.save()
            return Response()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def user_detail(self, pk):
    try:
        user = User.objects.get(pk=pk)
        return Response(ReadUserSerializer(user).data)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
