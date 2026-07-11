from typing import Optional

VALID_DOMAINS = {"DSA", "DBMS", "FullStack", "Aptitude", "Coding", "Academic", "Technical"}

def normalize_domain(category: str) -> Optional[str]:
    """
    Normalizes subject category input to match backend database values.
    Example: 'Full Stack', 'fullstack', 'full-stack', 'FULLSTACK' -> 'FullStack'
    """
    if not category:
        return None
        
    cleaned = category.strip().replace(" ", "").replace("-", "").lower()
    
    # Check normalization map
    norm_map = {
        "dsa": "DSA",
        "dbms": "DBMS",
        "fullstack": "FullStack",
        "aptitude": "Aptitude",
        "coding": "Coding",
        "academic": "Academic",
        "academics": "Academic",
        "technical": "Technical"
    }
    
    normalized = norm_map.get(cleaned)
    if normalized in VALID_DOMAINS:
        return normalized
    return None

def is_valid_domain(category: str) -> bool:
    """Checks if the given category string (after normalization) is valid."""
    return normalize_domain(category) is not None
