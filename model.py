from django.http import HttpResponse
from django import forms
from subprocess import Popen, PIPE, STDOUT
from django.views.decorators.http import condition
import re

class SearchForm(forms.Form):
	url = forms.CharField()
	depth = forms.CharField()
	search = forms.CharField()

@condition(etag_func=None)
def search(request):
	if (request.method == 'POST'):
		form = SearchForm(request.POST)
		if (form.is_valid()):
			url = form.cleaned_data['url']
			depth = int(form.cleaned_data['depth'])
			search = form.cleaned_data['search']

			return HttpResponse(stream_response(url, depth, search), mimetype='text/html')
	else:
		form = SearchForm()
		
	return render_to_response('index.html', { 'form': form })
	
def stream_response(url, depth, search):
	cmd = 'python ../python-web-crawler/crawl.py {} {} {}'.format(url, depth, search)
	p = Popen(cmd, stdout = PIPE, stderr = STDOUT, shell = True)

	yield "<html><body>\n"
	while True:
		line = p.stdout.readline()

		m = re.findall(' at (.*)', line)
		if len(m) > 0:
			for href in m:
				yield '<div>Found {} at <a href="{}">{}</a></div>\n'.format(search, href, href)
		else:
			yield "<div>%s</div>\n" % line
			
		if not line: break
	yield "</body></html>\n"
