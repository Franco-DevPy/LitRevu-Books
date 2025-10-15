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
        widgets = {
            "rating": forms.NumberInput(attrs={"min": 1, "max": 5, "step": 1}),
            "headline": forms.TextInput(attrs={"required": True}),
            "body": forms.Textarea(attrs={"rows": 4}),
        }


class FollowForm(forms.Form):
    username = forms.CharField(
        label="Nom d'utilisateur",
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "Utilisateur à suivre"}),
    )
