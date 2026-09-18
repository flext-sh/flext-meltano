# from flext-meltano/docs/architecture/security-architecture.md:606
from __future__ import annotations


class APIGatewaySecurity:
    """API Gateway security controls."""

    def __init__(self):
        self.waf_rules = self._load_waf_rules()
        self.rate_limits = self._load_rate_limits()
        self.ip_whitelist = self._load_ip_whitelist()

    def validate_request(self, request: HTTPRequest) -> SecurityDecision:
        """Validate incoming request against security rules."""
        # IP whitelisting
        if not self._is_ip_allowed(request.client_ip):
            return SecurityDecision(block=True, reason="IP not whitelisted")

        # Rate limiting
        if self._is_rate_limit_exceeded(request.client_ip, request.endpoint):
            return SecurityDecision(block=True, reason="Rate limit exceeded")

        # WAF rules
        waf_result = self._check_waf_rules(request)
        if not waf_result.allowed:
            return SecurityDecision(block=True, reason=f"WAF: {waf_result.rule}")

        # JWT validation
        if not self._validate_jwt_token(request.authorization):
            return SecurityDecision(block=True, reason="Invalid JWT token")

        return SecurityDecision(block=False, reason="Request allowed")

    def _is_ip_allowed(self, ip_address: str) -> bool:
        """Check if IP address is in whitelist."""
        return ip_address in self.ip_whitelist

    def _is_rate_limit_exceeded(self, ip: str, endpoint: str) -> bool:
        """Check if rate limit is exceeded."""
        key = f"ratelimit:{ip}:{endpoint}"
        current_count = self.redis.incr(key)

        # Reset counter every minute
        self.redis.expire(key, 60)

        return current_count > self.rate_limits.get(endpoint, 100)```
#### Service Mesh Security

