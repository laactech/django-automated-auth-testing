import pytest
from django.urls import URLPattern

from automated_auth_testing.config.urls import urlpatterns
from automated_auth_testing.tests.enums import HttpMethod
from automated_auth_testing.tests.helpers import flatten_urlpatterns

flat_url_patterns = list(flatten_urlpatterns(urlpatterns))


@pytest.fixture(scope="session", params=flat_url_patterns)
def url_pattern(request) -> URLPattern:
    return request.param


@pytest.fixture(scope="session", params=HttpMethod.all_methods())
def http_method(request) -> HttpMethod:
    return request.param
