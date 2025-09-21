from django import forms
from .models import Ticket, Review
from django.contrib.auth import get_user_model

User = get_user_model()


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "required": True,
                    "autocomplete": "off",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": 3,
                    "required": True,
                }
            ),
            "image": forms.ClearableFileInput(attrs={}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["headline", "body", "rating"]


class FollowForm(forms.Form):
    username = forms.CharField(max_length=150)
