from django.db import models
from django import forms


# Create your models here.

class InstanceUrlForm(forms.Form):
    instance_url = forms.CharField(label="Instance Url", max_length=500)
    operation_type = forms.ChoiceField(
        label="",
        label_suffix="",
        widget=forms.RadioSelect,
        choices=[(0,"add"), (1,"remove")]
    )
