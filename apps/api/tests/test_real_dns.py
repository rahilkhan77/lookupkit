import pytest

from app.services.dns_mx import lookup_mx


@pytest.mark.integration
def test_real_dns_mx_for_google():
    found, hosts, error = lookup_mx("google.com", timeout=3.0)
    if error == "timeout":
        pytest.skip("DNS unavailable")
    assert found is True
    assert any("google" in h for h in hosts)
