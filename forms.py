from django import forms

class SearchForm(forms.Form):
	url = forms.URLField()
	depth = forms.IntegerField()
	search = forms.CharField()

