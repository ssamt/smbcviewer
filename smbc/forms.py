from django import forms

from .models import scores

class EvalComic(forms.Form):
    score = forms.ChoiceField(choices=scores)
    hide = forms.BooleanField(label='Hide', required=False)
