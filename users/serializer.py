from rest_framework import serializers
from .models import Account
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions

class AccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['username','email','password']
        
    def validate(self, data):
        user = Account(**data)
        password = data.get('password')
        try:
            validate_password(password, user)
        except exceptions.ValidationError as e:
            serializer_errors = serializers.as_serializer_error(e)
            raise exceptions.ValidationError(
                {'password': serializer_errors['non_field_errors']}
            )
        return data
    
    def create(self,validated_data):
        return Account.objects.create_user(**validated_data)
    
class AccountSerializer(serializers.ModelSerializer):
    total_posts = serializers.SerializerMethodField()

    def get_total_posts(self, obj):
        return obj.posts.filter(is_deleted=False).count()

    class Meta:
        model = Account
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'profile_pic',
                  'last_login', 'is_admin', 'is_staff', 'is_active', 'is_superuser', 'total_posts']
        








        