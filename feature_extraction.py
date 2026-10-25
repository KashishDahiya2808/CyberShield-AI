import re
from urllib.parse import urlparse


SUSPICIOUS_WORDS = [
    "login", "signin", "verify", "verification",
    "account", "secure", "update", "confirm",
    "password", "bank", "payment", "wallet",
    "free", "bonus", "claim", "gift", "reward"
]


def extract_features(url):
    """Extract basic security-related URL features."""

    url = str(url).strip()
    full_url = url.lower()

    if not full_url.startswith(("http://", "https://")):
        url_for_parse = "http://" + url
    else:
        url_for_parse = url

    parsed = urlparse(url_for_parse)
    domain = (parsed.hostname or "").lower()
    path = (parsed.path or "").lower()

    try:
        is_ip = int(
            bool(re.fullmatch(r"(?:\d{1,3}\.){3}\d{1,3}", domain))
        )
    except ValueError:
        is_ip = 0

    features = {
        "url_length": len(url),
        "domain_length": len(domain),
        "path_length": len(path),
        "dot_count": url.count("."),
        "hyphen_count": url.count("-"),
        "at_count": url.count("@"),
        "question_count": url.count("?"),
        "equal_count": url.count("="),
        "slash_count": url.count("/"),
        "digit_count": sum(c.isdigit() for c in url),
        "has_https": int(parsed.scheme.lower() == "https"),
        "has_ip": is_ip,
        "suspicious_word_count": sum(
            word in full_url for word in SUSPICIOUS_WORDS
        ),
        "subdomain_count": max(0, domain.count(".") - 1),
    }

    return features


if __name__ == "__main__":
    test_url = "https://example.com/login"

    result = extract_features(test_url)

    print("\nCyberShield AI - URL Feature Extraction")
    print("-" * 45)

    for feature, value in result.items():
        print(f"{feature}: {value}")
