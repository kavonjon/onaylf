from django.db.models import Prefetch
from rest_framework import serializers, viewsets
from .models import CurrentFair, Category, Performance, Instructor, Student, PerformanceAccessory
from users.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']

class PerformanceSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    category = CategorySerializer()
    grade_range_display = serializers.CharField(source='get_grade_range_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Performance
        fields = ['id', 'user', 'title', 'group', 'category', 'grade_range', 'grade_range_display', 'poster', 'performance_type', 'instructors', 'students', 'accessories', 'instructors_status', 'students_status', 'accessories_status', 'review_status', 'status', 'status_display', 'updated']

class InstructorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Instructor
        fields = ['id', 'user', 'lastname', 'firstname']

class StudentSerializer(serializers.ModelSerializer):
    grade_display = serializers.CharField(source='get_grade_display', read_only=True)
    performance_categories = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['id', 'user', 'lastname', 'firstname', 'tribe', 'grade', 'grade_display', 'hometown', 'state', 'tshirt_size', 'performance_categories']

    def get_performance_categories(self, obj):
        # Get the current fair
        currentFair = CurrentFair.objects.first()

        # Get the performances associated with the student in the current fair
        performances = obj.performance_student.filter(fair=currentFair.fair)

        # Get the categories of these performances
        categories = [performance.category.name for performance in performances]

        return categories

class PosterSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    students = StudentSerializer(many=True)
    grade_range_display = serializers.CharField(source='get_grade_range_display', read_only=True)

    class Meta:
        model = Performance
        fields = ['id', 'user', 'title', 'students', 'grade_range_display']

class PerformanceAccessorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceAccessory
        fields = ['performance', 'accessory', 'count']