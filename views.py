from django.http import HttpResponse
from django.shortcuts import render_to_response
from subprocess import Popen, PIPE, STDOUT
from django.views.decorators.http import condition
import re
from forms import SearchForm
from django.template import RequestContext



def index(request):
    return render_to_response('index.html', context_instance=RequestContext(request))  


@condition(etag_func=None)
def search(request):
	if request.method == 'POST':
		form = SearchForm(request.POST)
		if form.is_valid():
			return HttpResponse(stream_response(
                                            request.POST['url'], 
                                            request.POST['depth'], 
                                            request.POST['search']),mimetype='text/html')
		
	
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
