from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from cars.models import Cars, Like, Comments
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)
    def validate(self, data):
        return data


# class RegisterSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(
#         required=True, validators=[UniqueValidator(queryset=User.objects.all())]
#     )
#     password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
#     password2 = serializers.CharField(write_only=True, required=True)
#
#     class Meta:
#         model = User
#         fields=('Username','email','password','password2','first_name','last_name')
#         extra_kwargs = {
#             'first_name': {'required': True},
#             'last_name': {'required': True}
#         }
#
#     def validate(self, value):
#         if value['password'] != value['password2']:
#                 raise serializers.ValidationError({'password': 'Password does not match'})
#         return value
#
#     def create(self, validated_data):
#         user = User.objects.create_user(
#             username=validated_data['username'],
#             email=validated_data['email'],
#             first_name=validated_data['first_name'],
#             last_name=validated_data['last_name']
#
#         )
#         user.set_password(validated_data['password'])
#         user.save()
#         return user



class CarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cars
        fields = '__all__'

    # def get_liked(self, obj):
    #     request = self.context.get('request')
    #     if request and request.user.is_authenticated:
    #         return Like.objects.filter(user=request.user, car=obj).exists()
    #     return False

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'