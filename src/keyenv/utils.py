from .constvars import _prefix

# --- util functions to check format ---

def check(service: str) -> str:
    valid = all(c.isalnum() for c in service)
    if not valid:
        raise ValueError(f"Invalid character in {service}. Use alphanumeric only.")
    return service

def check_key(key: str) -> str:
    if "\n" in key:
        raise ValueError("Secret key cannot contain a newline character.")
    return key

# --- util functions to format services ---

def format_mem(service: str) -> str:
    return service.lower()

def format_cache(service: str) -> str:
    return _prefix + service.upper()

def scratch(service: str) -> str:
    return service[len(_prefix):]
