from django import forms

from .models import Project, Review

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'github_link', 'report_link', 'demo_link']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['grades', 'comment']
        widgets = {
            'grades': forms.NumberInput({'min': 0, 'max':100})
        }
