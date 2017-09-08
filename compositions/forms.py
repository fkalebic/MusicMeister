from django import forms
from django.core.validators import RegexValidator

notes = RegexValidator(r'^[a-g]*$', 'Only lowercase a-g characters are allowed.')
class AddCompositionForm(forms.Form):
	order = forms.CharField(validators=[notes])

class GradeCompositionForm(forms.Form):
	grade = forms.ChoiceField(
        choices=[(x, x) for x in range(1, 6)]
    )
	comment = forms.CharField()
		