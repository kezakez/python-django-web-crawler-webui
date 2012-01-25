from django.http import HttpResponse
from django import forms
import crawl

class SearchForm(forms.Form):
	url = forms.CharField()
	depth = forms.CharField()
	search = forms.CharField()

def search(request):
	if request.method == 'POST':
		form = SearchForm(request.POST)
		if form.is_valid():
			url = form.cleaned_data['url']
			depth = int(form.cleaned_data['depth'])
			search = form.cleaned_data['search']
			
			crawl.searchURL(url, depth, search)
			return HttpResponse("woo" + url)
	else:
		form = SearchForm()
		
	return render_to_response('index.html', { 'form': form })
