from rest_framework import serializers
from users.serializers import RelatedUserSerializer
from .models import Room


# class RoomSerializer(serializers.ModelSerializer):

#     user = UserSerializer()

#     class Meta:
#         model = Room
#         exclude = ("modified",)
#         # fields = ("pk", "name", "price", "bedrooms", "user")


class RoomSerializer(serializers.ModelSerializer):

    # Create room 할때는 user를 생성 할 필요는 없음
    # 그런데 이렇게 설정하면, room을 create 할때 user가 없어서 create 할 수 없음
    # 따라서 model serializer의 save()를 override해서 사용 할거임
    user = RelatedUserSerializer(read_only=True)
    # https://www.django-rest-framework.org/api-guide/fields/#serializermethodfield
    # dynamic fields
    am_i_sexy = serializers.SerializerMethodField()
    # am_i_sexy = serializers.SerializerMethodField(method_nmae="potato")

    # 누가 dynamic fields (serialize)를 요청 하는지를 알아야 한다.
    # 그래야 제대로 된 처리가 가능함
    # RoomsView가 부르는데, RoomsView에서 어떤 user가 보는지 알려줘야한다. ( request를 통해서 알 수 있다. )

    class Meta:
        model = Room
        exclude = ("modified",)
        # Update 하거나 Create 할 때 User를 validate 하지 않기 위해, read_only로 지정 해줌
        read_only_fields = ("user", "id", "created", "updated")

    def validate(self, data):
        # Create 할때만 적용 되게 할 수 있다.
        if self.instance:
            # default값 부여 가능 ( python의 기능, NOT DRF)
            check_in = data.get("check_in", self.instance.check_in)
            check_out = data.get("check_out", self.instance.check_out)
        else:
            check_in = data.get("check_in")
            check_out = data.get("check_out")
            print(check_in, check_out)
        if check_in == check_out:
            raise serializers.ValidationError("Not enough time between changes")
        return data

    # How do I gives user to this serializer ?
    # Use context !
    # How do I gives context to this serializer ?
    # Already sending by DRF ! ( http://www.cdrf.co/3.9/rest_framework.viewsets/ModelViewSet.html#get_serializer_context )
    def create(self, validated_data):
        # print(self.context.get("request").user)
        # room = Room.objects.create(**validated_data)
        # return room
        request = self.context.get("request")
        room = Room.objects.create(**validated_data, user=request.user)
        return room

    # naming must be get_fields_name
    # or, add method name parameter to SerializerMethodField(method_name=원하는이름)
    # obj -> serializer가 처리하고 있는 애 ( 지금은 room )
    def get_am_i_sexy(self, obj):
        # print(obj)
        # context를 통해서 request를 받고, 이를 통해 user를 받는다.
        request = self.context.get("request")
        # print(request.user)
        if request:
            user = request.user
            if user.is_authenticated:
                return obj in user.favs.all()
        return False

    # def potato(self, obj):
    #     print(obj)
    #     return True


# class ReadRoomSerializer(serializers.ModelSerializer):

#     user = RelatedUserSerializer()

#     class Meta:
#         model = Room
#         exclude = ("modified",)
#         # fields = ("pk", "name", "price", "bedrooms", "user")


# # User를 create에 받을 수 없다면 ModelSerializer를 안쓰고, 그냥 Serializer를 쓴다. ( ModelSerializer 써도 되는데, 그냥 수동으로 해봄)
# class WriteRoomSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Room
#         exclude = (
#             "user",
#             "modified",
#             "created",
#         )

#     def validate(self, data):
#         # Create 할때만 적용 되게 할 수 있다.
#         if self.instance:
#             # default값 부여 가능 ( python의 기능, NOT DRF)
#             check_in = data.get("check_in", self.instance.check_in)
#             check_out = data.get("check_out", self.instance.check_out)
#         else:
#             check_in = data.get("check_in")
#             check_out = data.get("check_out")
#             print(check_in, check_out)
#         if check_in == check_out:
#             raise serializers.ValidationError("Not enough time between changes")
#         return data


# # User를 create에 받을 수 없다면 ModelSerializer를 안쓰고, 그냥 Serializer를 쓴다. ( ModelSerializer 써도 되는데, 그냥 수동으로 해봄)
# class WriteRoomSerializer(serializers.Serializer):

#     name = serializers.CharField(max_length=140)
#     address = serializers.CharField(max_length=140)
#     price = serializers.IntegerField(help_text="USD per night")
#     beds = serializers.IntegerField(default=1)
#     lat = serializers.DecimalField(max_digits=10, decimal_places=6)
#     lng = serializers.DecimalField(max_digits=10, decimal_places=6)
#     bedrooms = serializers.IntegerField(default=1)
#     bathrooms = serializers.IntegerField(default=1)
#     check_in = serializers.TimeField(default="00:00:00")
#     check_out = serializers.TimeField(default="00:00:00")
#     instant_book = serializers.BooleanField(default=False)

#     def create(self, validated_data):
#         print(validated_data)
#         return Room.objects.create(**validated_data)

#     def validate(self, data):
#         # Create 할때만 적용 되게 할 수 있다.
#         if self.instance:
#             # default값 부여 가능 ( python의 기능, NOT DRF)
#             check_in = data.get("check_in", self.instance.check_in)
#             check_out = data.get("check_out", self.instance.check_out)
#         else:
#             check_in = data.get("check_in")
#             check_out = data.get("check_out")
#             print(check_in, check_out)
#         if check_in == check_out:
#             raise serializers.ValidationError("Not enough time between changes")
#         return data

#     def update(self, instance, validated_data):
#         # 모든 데이터를 validated_data로부터 가져오고, 기본 값으로 instance의 값을 사용한다.
#         instance.name = validated_data.get("name", instance.name)
#         instance.address = validated_data.get("address", instance.address)
#         instance.price = validated_data.get("price", instance.price)
#         instance.beds = validated_data.get("beds", instance.beds)
#         instance.lat = validated_data.get("lat", instance.lat)
#         instance.lng = validated_data.get("lng", instance.lng)
#         instance.bedrooms = validated_data.get("bedrooms", instance.bedrooms)
#         instance.bathrooms = validated_data.get("bathrooms", instance.bathrooms)
#         instance.check_in = validated_data.get("check_in", instance.check_in)
#         instance.check_out = validated_data.get("check_out", instance.check_out)
#         instance.instant_book = validated_data.get(
#             "instant_book", instance.instant_book
#         )
#         print(instance, validated_data)
#         instance.save()
#         return instance

# # Django에서의 clean과 비슷함
# def validate_beds(self, beds):
#     if beds < 5:
#         raise serializers.ValidationError("Your house is too small")
#     else:
#         return beds


# class BigRoomSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Room
#         fields = "__all__"
#         exclude = ()

# name = serializers.CharField(max_length=140)
# price = serializers.IntegerField()
# bedrooms = serializers.IntegerField()
# instant_book = serializers.BooleanField()
