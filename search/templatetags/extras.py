from django import template
from django.utils import timezone
from datetime import datetime
import dateutil.parser


register = template.Library()

register = template.Library()

@register.filter()
def get_filename(d):
    return d['_source']['file']['filename']


@register.filter()
def get_file_modified_at(d):
    time_str= d['_source']['file']['last_modified']
    return dateutil.parser.parse(time_str)


@register.filter()
def get_filesize(d):
    return d['_source']['file']['filesize']


@register.filter()
def get_fileurl(d):
    return d['_source']['file']['url']

@register.filter()
def get_fileurl_link(d):
    return  str(d['_source']['file']['url'])

@register.filter()
def get_highlight(d):
    return  str(d['highlight']['content'][0]).replace('\\n',' ')