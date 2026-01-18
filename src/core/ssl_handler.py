"""
Robust SSL Certificate Handling for Corporate Environments.
Patches both 'requests' and 'httpx' (used by LangChain) to ignore SSL errors.
"""

import os
import ssl
import warnings
import logging

# Configure logging
logger = logging.getLogger(__name__)

def configure_ssl_handling():
    """
    Configures SSL handling based on environment variables.
    If SSL_VERIFY=False, it aggressively patches libraries to ignore SSL errors.
    """
    ssl_verify = os.getenv("SSL_VERIFY", "True").lower() == "true"
    
    if ssl_verify:
        logger.info("🔐 SSL verification ENABLED (default)")
        return

    # --- SSL Bypass Mode ---
    # print("\n" + "!"*60)
    # print("WARNING: DISABLING SSL VERIFICATION (Corporate Proxy Mode)")
    # print("!"*60 + "\n")
    # logger.warning("🔓 SSL verification DISABLED - Patching libraries...")

    # 1. Suppress Warnings
    warnings.filterwarnings('ignore', message='Unverified HTTPS request')
    
    # 2. Patch standard ssl module (for some lower-level sockets)
    try:
        _create_unverified_https_context = ssl._create_unverified_context
        ssl._create_default_https_context = _create_unverified_https_context
    except AttributeError:
        pass

    # 3. Patch Requests
    try:
        import requests
        import urllib3
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry

        try:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        except AttributeError: pass

        try:
            urllib3.disable_warnings(urllib3.exceptions.SubjectAltNameWarning)
        except AttributeError: pass

        # Monkeypatch Session object to deafult to verify=False
        original_request = requests.Session.request

        def patched_request(self, method, url, *args, **kwargs):
            if 'verify' not in kwargs:
                kwargs['verify'] = False
            return original_request(self, method, url, *args, **kwargs)

        requests.Session.request = patched_request
        logger.info("  ✓ Patched 'requests' library")

    except ImportError:
        pass

    # 4. Patch HTTPX (Used by LangChain Async)
    try:
        import httpx
        
        # Monkeypatch the Client init to default to verify=False
        original_client_init = httpx.Client.__init__
        original_async_client_init = httpx.AsyncClient.__init__

        def patched_client_init(self, *args, **kwargs):
            if 'verify' not in kwargs:
                kwargs['verify'] = False
            return original_client_init(self, *args, **kwargs)

        def patched_async_client_init(self, *args, **kwargs):
            if 'verify' not in kwargs:
                kwargs['verify'] = False
            return original_async_client_init(self, *args, **kwargs)

        httpx.Client.__init__ = patched_client_init
        httpx.AsyncClient.__init__ = patched_async_client_init
        logger.info("  ✓ Patched 'httpx' library")

    except ImportError:
        pass

# Run configuration immediately on import if env is set
configure_ssl_handling()
