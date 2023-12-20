from rest_framework import serializers
from .models import Category, Performance, Instructor

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ['id', 'user', 'title', 'group', 'category', 'performance_type', 'instructors', 'students', 'accessories']

class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = ['id', 'user', 'lastname', 'firstname']

