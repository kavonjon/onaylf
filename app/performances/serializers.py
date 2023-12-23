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

class InstructorViewSet(viewsets.ModelViewSet):
    serializer_class = InstructorSerializer

    def get_queryset(self):
        queryset = Instructor.objects.all()
        user_id = self.request.query_params.get('user_id', None)
        performance_id = self.request.query_params.get('performance_id', None)
        if user_id is not None:
            queryset = queryset.filter(user__id=user_id)
        if performance_id is not None:
            queryset = queryset.filter(performance__id=performance_id)
        return queryset