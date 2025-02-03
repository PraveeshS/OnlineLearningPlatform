from django import forms
from .models import Course,Tag,Content, URLContent


class CourseForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False
    )

    class Meta:
        model = Course
        fields = ['title', 'description', 'price', 'subject', 'tags', 'start_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter course title',
                'class': 'form-control form-control-lg',  
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Enter course description',
                'class': 'form-control',
                'rows': 4,  
            }),
            'price': forms.NumberInput(attrs={
                'placeholder': 'Enter course price',
                'class': 'form-control',
            }),
            'subject': forms.TextInput(attrs={
                'placeholder': 'Enter course subject',
                'class': 'form-control',
            }),
            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
            }),
        }

    def __init__(self, *args, **kwargs):
        instructor = kwargs.pop('instructor', None)
        super(CourseForm, self).__init__(*args, **kwargs)
        if instructor and self.instance.pk is None:  
            self.instance.instructor = instructor

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price

    def save(self, commit=True):
        course = super(CourseForm, self).save(commit=False)
        if commit:
            course.save()
        return course
    
from django import forms
from .models import Content

class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['title', 'description']  
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Content title'}),
            'description': forms.Textarea(attrs={'placeholder': 'Content description'}),
        }
class URLContentForm(forms.ModelForm):
    class Meta:
        model = URLContent   
        fields = ['title', 'content_type', 'url', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Content title'}),
            'content_type': forms.Select(choices=[('link', 'Link'), ('file', 'File')]),
            'url': forms.URLInput(attrs={'placeholder': 'Enter the URL'}),
            'file': forms.ClearableFileInput(attrs={'placeholder': 'Upload a file'}),
        }
