from django import forms
from django.core.validators import RegexValidator

notes = RegexValidator(r'^[a-g]*$', 'Only lowercase a-h characters are allowed.')
class AddCompositionForm(forms.Form):
	order = forms.CharField(validators=[notes])
