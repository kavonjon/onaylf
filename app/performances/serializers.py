from rest_framework import serializers, viewsets
from .models import Category, Performance, Instructor
from users.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

class PerformanceSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Performance
        fields = ['id', 'user', 'title', 'group', 'category', 'performance_type', 'instructors', 'students', 'accessories']

class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = ['id', 'user', 'lastname', 'firstname']

