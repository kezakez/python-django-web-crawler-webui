from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.http import condition
from forms import SearchForm
from django.template import RequestContext
from utils import stream_response


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
                request.POST['search']), mimetype='text/html')

