from rest_framework import serializers
from api.models import User, DONE
from api.utils import username_or_email
import re



class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        if User.objects.filter(email=email).filter(status=DONE).exists():
            data = {
                "status": False,
                "message": "This email is available"
            }
            raise serializers.ValidationError(data)
        
        return email
    

class CodeSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)

    def validate_code(self, code):
        if not re.fullmatch(r"\d{4}", code):
            raise serializers.ValidationError("The code must be a 4-digit number.")
        return code
    

class FullSignUpSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    reset_password = serializers.CharField(required=True)

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("User is available")
        return username
    
    def validate(self, validated_data):
        password = validated_data.get('password')
        reset_password = validated_data.get('reset_password')
        if password != reset_password:
            raise serializers.ValidationError("Passwords don't match")
        return validated_data
    

class LoginSerializer(serializers.Serializer):
    user_input = serializers.CharField(required=True)
    username = serializers.CharField(read_only=True)
    password = serializers.CharField(required=True)

    def validate(self, validated_data):
        user_input = validated_data.get('user_input')
        if username_or_email(user_input):
            user = User.objects.filter(email=user_input).filter(status=DONE).first()
            if user is not None:
                validated_data['username'] = user.username
        else:
            validated_data['username'] = user_input
        return validated_data
    





