import ipaddress
from urllib.parse import urlparse

# List of common URL shortener domain names
URL_SHORTENERS = [
    'bit.ly', 'tinyurl.com', 't.co', 'is.gd', 'ow.ly',
    'goo.gl', 'rebrand.ly', 'tiny.cc', 'shorte.st', 'cutt.ly'
]

# List of common suspicious keywords used in phishing URLs
SUSPICIOUS_KEYWORDS = [
    'login', 'verify', 'update', 'secure', 'account',
    'banking', 'paypal', 'signin', 'webscr', 'ebayisapi'
]

def is_ip_address(hostname):
    """Check if the given hostname is an IPv4 or IPv6 address."""
    if not hostname:
        return False
    try:
        ipaddress.ip_address(hostname)
        return True
    except ValueError:
        return False

def count_subdomains(hostname):
    """Calculate the number of subdomains in a given hostname."""
    if not hostname or is_ip_address(hostname):
        return 0

    parts = hostname.split('.')
    # Standard domain (e.g., example.com) has 2 parts; subdomains exceed 2 parts
    if len(parts) > 2:
        return len(parts) - 2
    return 0

def extract_url_features(url):
    """
    Extract lexical and structural features from a target URL string.
    Returns a dictionary containing raw/display features and ML values.
    """
    if not url:
        return {}

    # Ensure URL includes scheme for standard parsing
    url_str = url.strip()
    if not (url_str.startswith('http://') or url_str.startswith('https://')):
        parsed_url = urlparse('http://' + url_str)
    else:
        parsed_url = urlparse(url_str)

    hostname = parsed_url.hostname or ''

    # 1. URL Length
    url_length = len(url_str)

    # 2. HTTPS Availability
    uses_https = 1 if parsed_url.scheme == 'https' else 0

    # 3. IP Address Usage
    uses_ip = 1 if is_ip_address(hostname) else 0

    # 4. Number of Dots
    dot_count = url_str.count('.')

    # 5. Number of Subdomains
    subdomain_count = count_subdomains(hostname)

    # 6. Presence of '@' Symbol
    has_at_symbol = 1 if '@' in url_str else 0

    # 7. Presence of Hyphen in Domain
    has_hyphen_domain = 1 if '-' in hostname else 0

    # 8. URL Shortener Detection
    uses_shortener = 1 if hostname.lower() in URL_SHORTENERS else 0

    # 9. Suspicious Keywords Check
    url_lower = url_str.lower()
    matched_keywords = [kw for kw in SUSPICIOUS_KEYWORDS if kw in url_lower]
    suspicious_keyword_count = len(matched_keywords)

    return {
        'url': url_str,
        'url_length': url_length,
        'uses_https': 'Yes' if uses_https else 'No',
        'uses_ip': 'Yes' if uses_ip else 'No',
        'dot_count': dot_count,
        'subdomain_count': subdomain_count,
        'has_at_symbol': 'Yes' if has_at_symbol else 'No',
        'has_hyphen_domain': 'Yes' if has_hyphen_domain else 'No',
        'uses_shortener': 'Yes' if uses_shortener else 'No',
        'suspicious_keyword_count': suspicious_keyword_count,
        'matched_keywords': matched_keywords,
        # Numerical feature vector for Machine Learning classifier
        'ml_features': [
            url_length,
            uses_https,
            uses_ip,
            dot_count,
            subdomain_count,
            has_at_symbol,
            has_hyphen_domain,
            uses_shortener,
            suspicious_keyword_count
        ]
    }
