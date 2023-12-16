from django import forms
from .models import Performance, Category

class CategoryNameWidget(forms.Select):
    def format_value(self, value):
        if value:
            return Category.objects.get(pk=value).name
        return ''

class PerformanceForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Customize the queryset for the category field to fetch only names
    #     self.fields['category'].queryset = Category.objects.values_list('name', flat=True)
    # # category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=CategoryNameWidget)

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
