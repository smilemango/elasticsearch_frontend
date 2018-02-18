from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from elasticsearch import Elasticsearch


def index(request):
    RESULT_SIZE = 1

    keyword = ''
    res = None
    is_hits = False
    start_from = 0
    has_next = False
    next_from = 0
    before_from = 0

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if 'from' in request.GET:
            start_from = int(request.GET['from'])
        else:
            start_from = 0

        esclient = Elasticsearch(['localhost:9200'])
        res = esclient.search(
            index='fs_index',
            body={
                "from":start_from, "size":RESULT_SIZE,
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
        cur_len = len(res['hits']['hits'])
        is_hits = cur_len > 0
        next_from = start_from + cur_len
        before_from = start_from - RESULT_SIZE

        #전체 사이즈
        total = res['hits']['total']
        #현재 가져온 것의 사이즈
        cur_total = start_from + cur_len
        if total > cur_total:
            has_next = True




    context = {'keyword': keyword,
               'res': res,
               'is_hits': is_hits,
               'has_next' : has_next,
               'next_from': next_from,
               'start_from': start_from,
               'before_from': before_from
               }

    template = loader.get_template('search/index.html')
    return HttpResponse(template.render(context, request))
