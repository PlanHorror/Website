from django import template
from django.urls import resolve, reverse, translate_url
register = template.Library()

@register.simple_tag(takes_context=True)
def translate_urls(context, language):
    url = translate_url(context['request'].get_full_path(), language)
    return url
