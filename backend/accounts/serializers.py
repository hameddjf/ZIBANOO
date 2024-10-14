from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'phone_number', 'address', 'postal_code', 'note', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'username': {'required': True},
        }

    def create(self, validated_data):
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])  # Set the password correctly
        user.save()
        return user

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("کاربری با این ایمیل وجود دارد.")
        return value

    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("کاربری با این نام کاربری وجود دارد.")
        return value

    def validate_phone_number(self, value):
        if CustomUser.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("کاربری با این شماره تلفن وجود دارد.")
        return value


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("نام کاربری یا رمز عبور اشتباه است.")

        if not user.check_password(password):
            raise serializers.ValidationError("نام کاربری یا رمز عبور اشتباه است.")

        attrs['user'] = user
        return attrs


class CustomUserChangeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)
    username = serializers.CharField(required=False)

    old_password = serializers.CharField(write_only=True, required=False)
    new_password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)

    def validate(self, attrs):

        if 'old_password' in attrs and ('new_password' not in attrs or 'confirm_password' not in attrs):
            raise serializers.ValidationError({"new_password": "New password and confirmation are required."})

        if 'new_password' in attrs and attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"new_password": "New passwords must match."})

        return attrs

    def update(self, instance, validated_data):

        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.username = validated_data.get('username', instance.username)

        if 'new_password' in validated_data:
            instance.set_password(validated_data['new_password'])

        instance.save()
        return instance
