<<<<<<< HEAD
from django.shortcuts import render

# Create your views here.
=======
# import json
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from rooms.models import Room

def list_rooms(request):
    # rooms = Room.objects.all()
    # rooms_json = [] django queryset을 json으로 바로 변환 할 수 없음 ( serializer 사용 )
    # for room in rooms:
    #     rooms_json.append(json.dumps(room))
    data = serializers.serialize("json", Room.objects.all())
    response = HttpResponse(content=data)
    return response
