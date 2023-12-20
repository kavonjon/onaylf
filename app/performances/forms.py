from django import forms
from .models import Performance, Category, Instructor

class CategoryNameWidget(forms.Select):
    def format_value(self, value):
        if value:
            return Category.objects.get(pk=value).name
        return ''

class PerformanceForm(forms.ModelForm):
    class Meta:
        model = Performance
        prefix = 'performance'
        fields = ['title',
                  'group',
                  'languoid',
                  'category',
                  'grade_range',
                  'performance_type']
        # widgets = {
        # #     'languoid': forms.SelectMultiple(),
        #     'category': CategoryNameWidget()
        # }

class InstructorForm(forms.ModelForm):
    class Meta:
        model = Instructor
        prefix = 'instructor'
        fields = ['firstname',
                  'lastname',]