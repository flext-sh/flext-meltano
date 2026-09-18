# from flext-meltano/docs/architecture/security-architecture.md:453
from __future__ import annotations


class TLSConfig:
    """TLS configuration for secure communications."""

    def __init__(self):
        self.min_tls_version = "TLSv1.3"
        self.cipher_suites = [
            "TLS_AES_256_GCM_SHA384",
            "TLS_CHACHA20_POLY1305_SHA256",
            "TLS_AES_128_GCM_SHA256",
        ]
        self.certificate_validation = True
        self.client_certificate_required = False

    def get_ssl_context(self) -> ssl.SSLContext:
        """Create SSL context with security settings."""
        context = ssl.create_default_context()
        context.minimum_version = ssl.TLSVersion.TLSv1_3
        context.set_ciphers(":".join(self.cipher_suites))

        # Certificate validation
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED

        return context```
### Data Classification and Handling

