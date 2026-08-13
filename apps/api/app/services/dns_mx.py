import dns.exception
import dns.resolver


def lookup_mx(domain: str, timeout: float = 2.5) -> tuple[bool, list[str], str | None]:
    """Real DNS MX lookup. Returns (found, hosts, error)."""
    resolver = dns.resolver.Resolver()
    resolver.lifetime = timeout
    resolver.timeout = timeout
    try:
        answers = resolver.resolve(domain, "MX")
        hosts = sorted(
            {str(rdata.exchange).rstrip(".").lower() for rdata in answers if rdata.exchange},
        )
        return (len(hosts) > 0, hosts, None)
    except dns.resolver.NXDOMAIN:
        return False, [], "nxdomain"
    except dns.resolver.NoAnswer:
        return False, [], "no_answer"
    except dns.resolver.NoNameservers:
        return False, [], "no_nameservers"
    except dns.exception.Timeout:
        return False, [], "timeout"
    except dns.exception.DNSException as exc:
        return False, [], type(exc).__name__
