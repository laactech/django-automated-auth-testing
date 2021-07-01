import pytest
from django.urls import URLPattern

from config.urls import urlpatterns

from .enums import HttpMethod
from .helpers import flatten_urlpatterns

flat_url_patterns = list(flatten_urlpatterns(urlpatterns))


@pytest.fixture(scope="session", params=flat_url_patterns)
def url_pattern(request) -> URLPattern:
    return request.param


@pytest.fixture(scope="session", params=HttpMethod.all_methods())
def http_method(request) -> HttpMethod:
    return request.param
