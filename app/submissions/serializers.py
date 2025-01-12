from django.db.models import Prefetch
from rest_framework import serializers, viewsets
from .models import CurrentFair, Category, Submission, Instructor, Student, Accessory, SubmissionAccessory, Tribe
from users.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'organization']

class SubmissionSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    category = CategorySerializer()
    grade_range_display = serializers.CharField(source='get_grade_range_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Submission
        fields = ['id', 'user', 'title', 'group', 'category', 'grade_range', 'grade_range_display', 'poster', 'submission_type', 'instructors', 'students', 'accessories', 'instructors_status', 'students_status', 'accessories_status', 'review_status', 'status', 'status_display', 'updated']

class InstructorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Instructor
        fields = ['id', 'user', 'lastname', 'firstname']

class StudentSerializer(serializers.ModelSerializer):
    grade_display = serializers.CharField(source='get_grade_display', read_only=True)
    submission_categories = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['id', 'user', 'lastname', 'firstname', 'tribe', 'grade', 'grade_display', 'hometown', 'state', 'tshirt_size', 'submission_categories']

    def get_submission_categories(self, obj):

        # Get the submissions associated with the student
        submissions = obj.submission_student.all()

        # Get the categories of these submissions
        categories = [submission.category.name for submission in submissions]

        return categories

class TribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tribe
        fields = ['id', 'name']

class AccessorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Accessory
        fields = ['id', 'name']

class SubmissionAccessorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionAccessory
        fields = ['submission', 'accessory', 'count']

class StudentJsonSerializer(StudentSerializer):
    user = UserSerializer()
    tribe = TribeSerializer(many=True)

class SubmissionAccessoryJsonSerializer(SubmissionAccessorySerializer):
    accessory = AccessorySerializer()

class SubmissionJsonSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    category = CategorySerializer()
    instructors = InstructorSerializer(many=True)
    students = StudentJsonSerializer(many=True)
    accessories = SubmissionAccessoryJsonSerializer(source='submissionaccessory_set', many=True)
    grade_range_display = serializers.CharField(source='get_grade_range_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Submission
        fields = ['id', 'user', 'title', 'group', 'category', 'grade_range', 'grade_range_display', 'poster', 'submission_type', 'instructors', 'students', 'accessories', 'status', 'status_display', 'updated', 'modified_by']



class PosterSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    students = StudentSerializer(many=True)
    grade_range_display = serializers.CharField(source='get_grade_range_display', read_only=True)

    class Meta:
        model = Submission
        fields = ['id', 'user', 'title', 'students', 'grade_range_display']

