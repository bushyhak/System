from django import template
from django.urls import resolve


register = template.Library()


@register.simple_tag(takes_context=True)
def is_active(context, url_name):
    request = context["request"]
    resolved_url = resolve(request.path_info)
    if resolved_url.url_name == url_name:
        return "active"
    else:
        return ""
