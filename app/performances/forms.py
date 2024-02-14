from django import forms
from .models import Performance, Category, Instructor, Student

class CategoryNameWidget(forms.Select):
    def format_value(self, value):
        if value:
            return Category.objects.get(pk=value).name
        return ''

class PerformanceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        selected_category = kwargs.pop('selected_category', None)
        super(PerformanceForm, self).__init__(*args, **kwargs)
        if selected_category:
            try:
                category_instance = Category.objects.get(name=selected_category)
                self.fields['category'].initial = category_instance
            except Category.DoesNotExist:
                pass  # Just don't change the form if the category does not exist

        # Make the 'title' field optional in Django's server-side validation
        self.fields['title'].required = False


    class Meta:
        model = Performance
        prefix = 'performance'
        fields = ['title',
                  'group',
                  'languoids',
                  'other_languoid',
                  'category',
                  'grade_range',
                  'performance_type',
                  'comments',]
        # widgets = {
        # #     'languoid': forms.SelectMultiple(),
        #     'category': CategoryNameWidget()
        # }

class PerformanceCommentsForm(forms.ModelForm):
    class Meta:
        model = Performance
        prefix = 'performance'
        fields = ['comments']

class PosterForm(forms.ModelForm):
    class Meta:
        model = Performance
        prefix = 'performance'
        fields = ['title',
                  'languoids',
                  'other_languoid',
                  'grade_range',
                  'instructors',
                  'students',]

class InstructorForm(forms.ModelForm):
    class Meta:
        model = Instructor
        prefix = 'instructor'
        fields = ['firstname',
                  'lastname',]

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        prefix = 'student'
        fields = ['firstname',
                  'lastname',
                  'tribe',
                  'grade',
                  'hometown',
                  'state',
                  'tshirt_size',]
