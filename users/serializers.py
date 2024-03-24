from rest_framework import serializers
from datetime import datetime
from .models import User

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'name', 'dob', 'password')
        extra_kwargs = {'password':{'write_only':True}}
    
    def create(self, validated_data):
        date_object = datetime.strptime(str(validated_data['dob']), "%Y-%m-%d").date()
        user_obj = User.objects.create(email=validated_data['email'],name=validated_data['name'],dob=str(date_object))
        user_obj.set_password(validated_data['password'])
        user_obj.save()
        return user_obj
    
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=50,write_only=True, required=True)
    password = serializers.CharField(max_length=50,read_only=True)

    class Meta:
        model = User
        fields = ['email','password']

