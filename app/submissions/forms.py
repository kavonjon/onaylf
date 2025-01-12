from django import forms
from .models import Submission, Category, Instructor, Student, Languoid

class CategoryNameWidget(forms.Select):
    def format_value(self, value):
        if value:
            return Category.objects.get(pk=value).name
        return ''

class SubmissionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        selected_category = kwargs.pop('selected_category', None)
        current_fair = kwargs.pop('current_fair', None)
        super(SubmissionForm, self).__init__(*args, **kwargs)

        # Filter the category queryset by fair
        self.fields['category'].queryset = Category.objects.filter(fair=current_fair)
        
        # Filter the languoids queryset by fair
        self.fields['languoids'].queryset = Languoid.objects.filter(fair=current_fair)

        # Only set initial category if we don't have an instance
        if selected_category and not self.instance.pk:
            try:
                category_instance = Category.objects.get(
                    name=selected_category,
                    fair=current_fair
                )
                self.fields['category'].initial = category_instance
            except Category.DoesNotExist:
                pass

        # Make the 'title' field optional in Django's server-side validation
        self.fields['title'].required = False

        # Make the override_submission_type field optional in Django's server-side validation
        self.fields['override_submission_type'].required = False

        # Change the category field label
        self.fields['category'].label = "Category"

    class Meta:
        model = Submission
        prefix = 'submission'
        fields = ['title',
                  'group',
                  'languoids',
                  'other_languoid',
                  'category',
                  'grade_range',
                  'submission_type',
                  'override_submission_type',
                  'comments',]
        # widgets = {
        # #     'languoid': forms.SelectMultiple(),
        #     'category': CategoryNameWidget()
        # }

class SubmissionCommentsForm(forms.ModelForm):
    class Meta:
        model = Submission
        prefix = 'submission'
        fields = ['comments']

class PosterForm(forms.ModelForm):
    class Meta:
        model = Submission
        prefix = 'submission'
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
