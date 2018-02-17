from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from elasticsearch import Elasticsearch


def index(request):

    keyword = ''
    res = None
    is_hits = False
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        esclient = Elasticsearch(['localhost:9200'])
        res = esclient.search(
            index='fs_index',
            body={
                "query": {
                    "match": {
                        "content": keyword
                    }
                },
                "highlight": {
                    "pre_tags": ["<b>"],
                    "post_tags": ["</b>"],
                    "fields": {
                        "content": {}
                    }
                }
            })
        is_hits = len(res['hits']['hits']) > 0



    context = {'keyword': keyword,
               'res': res,
               'is_hits': is_hits }

    template = loader.get_template('search/index.html')
    return HttpResponse(template.render(context, request))
