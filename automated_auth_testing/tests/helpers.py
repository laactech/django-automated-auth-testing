from typing import Generator, Optional

from django.urls import URLPattern, URLResolver, reverse


def flatten_urlpatterns(url_patterns: list, app_name: Optional[str] = None) -> Generator:
    """
    This function produces a generator that flattens the urlpatterns list. Some of the
    objects in the root urlpatterns are URLResolvers which have their own sub
    url_patterns. It also adds the app_name of the previous URLResolver so that each pattern
    is reversible
    """
    for obj in url_patterns:
        if isinstance(obj, URLResolver):
            # There's a case where there's two nested URLResolvers where the first one has the correct app_name, but
            # the nested one doesn't. In this case the top level app_name is correct
            if app_name and not obj.app_name:
                actual_app_name = app_name
            else:
                actual_app_name = obj.app_name
            yield from flatten_urlpatterns(obj.url_patterns, app_name=actual_app_name)
        else:
            if app_name:
                obj.app_name = app_name
            yield obj


def reverse_url(url_pattern: URLPattern) -> str:
    try:
        # Try to create the URL with the app name that is added when flattening the urlpatterns. If it doesn't have one
        # then we can just use the pattern name
        reversible_url = f"{url_pattern.app_name}:{url_pattern.pattern.name}"
    except AttributeError:
        reversible_url = url_pattern.pattern.name
    url_regex = url_pattern.pattern.regex
    # Check the regex to see if the url pattern requires any kwargs and use it to build the kwargs dict for reversing
    kwargs = {}
    if url_regex.groups > 0:
        for regex_key in url_regex.groupindex.keys():
            kwargs[regex_key] = 1
    return reverse(reversible_url, kwargs=kwargs)
