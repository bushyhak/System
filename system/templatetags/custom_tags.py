import hashlib
from django import template
from django.urls import resolve
from urllib.parse import urlencode
from django.utils.safestring import mark_safe


register = template.Library()


@register.simple_tag(takes_context=True)
def is_active(context, url_name):
    request = context["request"]
    resolved_url = resolve(request.path_info)
    if resolved_url.url_name == url_name:
        return "active"
    else:
        return ""


@register.filter
def gravatar_url(email: str, size=40):
    """return only the URL of the gravatar

    TEMPLATE USE:  {{ email|gravatar_url:150 }}
    """
    # mp | identicon | monsterid | wavatar | retro | robohash | blank
    default = "identicon"
    hash = hashlib.md5(email.lower().encode()).hexdigest()
    params = urlencode({"d": default, "s": str(size)})

    return "https://www.gravatar.com/avatar/%s?%s" % (hash, params)


@register.filter
def gravatar(email: str, size=40, **kwargs):
    """return an image tag with the gravatar

    TEMPLATE USE:  {{ email|gravatar:150 }}
    """
    classname = kwargs.get("classname", "gravatar-img")
    alt = kwargs.get("alt", " ")
    url = gravatar_url(email, size)

    img_tag = '<img src="%s" height="%d" width="%d" class="%s" alt="%s">' % (
        url,
        size,
        size,
        classname,
        alt,
    )
    return mark_safe(img_tag)


@register.simple_tag(takes_context=True)
def gravatar_tag(context, **kwargs):
    """return an html img tag with a gravatar url

    TEMPLATE USE:  {% gravatar_tag size=80 classname='d-block border' alt='My image' %}
    """
    user = context["request"].user
    email = "None"
    if user.is_authenticated:
        email = user.email
    size = kwargs.get("size", 40)
    classname = kwargs.get("classname", "gravatar-img")
    alt = kwargs.get("alt", " ")
    url = gravatar_url(email, size)

    img_tag = '<img src="%s" height="%d" width="%d" class="%s" alt="%s">' % (
        url,
        size,
        size,
        classname,
        alt,
    )
    return mark_safe(img_tag)
