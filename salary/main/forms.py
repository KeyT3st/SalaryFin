from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Sanction, Sanctions

class UserForm(forms.Form):
    name = forms.CharField(label="Имя:", initial="Undefined", help_text="Введите своё имя", min_length=2, max_length=12)
    age = forms.IntegerField(label="Возраст", initial=0, help_text="Введите свой возраст", min_value=5, max_value=120)
    comment = forms.CharField(label="Комментарий" ,widget=forms.Textarea, required=False)

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user
	
class add_sanction(forms.Form):
	sanction = forms.ChoiceField(label="Штраф:", choices=Sanction.objects.all(), required=False)
	date = forms.DateField(label="Дата:", required=False)

class add_bonuse(forms.Form):
	reason = forms.CharField(label="Причина", max_length=400)
	date = forms.DateField(label="Дата премии")
	summ = forms.IntegerField(label="Размер премии")