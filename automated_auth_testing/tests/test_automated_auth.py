from django.test import client
from django.urls import URLPattern

from automated_auth_testing.tests.enums import HttpMethod
from automated_auth_testing.tests.helpers import reverse_url

PUBLIC_ENDPOINTS: dict[str, tuple] = {
    "admin": HttpMethod.safe_methods(),
}

ACCEPTABLE_PUBLIC_ENDPOINT_STATUSES: set[int] = {
    200,
    400,
    404,
    405,
}
ACCEPTABLE_AUTHENTICATED_ENDPOINT_STATUSES: set[int] = {401}


def test_all_url_patterns_for_authentication(url_pattern: URLPattern, http_method: HttpMethod):
    http_client = client.Client()
    pattern_name = url_pattern.pattern.name
    url = reverse_url(url_pattern)
    http_method_to_call = getattr(http_client, http_method.value.lower())
    response = http_method_to_call(url)
    public_http_methods = PUBLIC_ENDPOINTS.get(pattern_name)
    if public_http_methods and http_method in public_http_methods:
        assert response.status_code in ACCEPTABLE_PUBLIC_ENDPOINT_STATUSES, (
            f"The automated authentication endpoint test failed for endpoint name, {pattern_name}, HTTP method"
            f" {http_method} and url {url}. The test thinks that this endpoint is public. It is not returning an"
            f" acceptable status such as, {ACCEPTABLE_PUBLIC_ENDPOINT_STATUSES}."
        )
    else:
        assert response.status_code in ACCEPTABLE_AUTHENTICATED_ENDPOINT_STATUSES, (
            f"The automated authentication endpoint test failed for endpoint name, {pattern_name}, HTTP method"
            f" {http_method} and url {url}. The test thinks that this endpoint is private, and it is not returning an"
            f" acceptable status such as, {ACCEPTABLE_AUTHENTICATED_ENDPOINT_STATUSES}."
        )
