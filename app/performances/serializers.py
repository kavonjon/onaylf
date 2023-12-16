from rest_framework import serializers
from .models import Category, Performance

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class PerformanceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ['id', 'user', 'title', 'group', 'category', 'performance_type']
