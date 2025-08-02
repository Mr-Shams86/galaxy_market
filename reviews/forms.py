from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['product', 'text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
            'rating': forms.Select(choices=[(i, f"{i} ⭐") for i in range(1, 6)]),
        }
