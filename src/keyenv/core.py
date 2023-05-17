import logging
import json
import os

from dotenv import load_dotenv

from .constvars import _keyring_dir, _prefix
from .utils import check, check_key, format_cache, format_mem, scratch

# --- private variables ---

_keyring = {}


# --- public interface ---

def store(filepath: str = _keyring_dir, *args, **kwargs) -> None:
    """Store secret keys to cache. Call me like this:
    - store(openai="sk-...") # any number of services
    - store("path/to/secretkeys.json") # only one file 
    """
    # TODO: should check that service does not exist yet.
    # TODO: option #2: have a flag to force overwrite (better!)
    update(filepath, *args, **kwargs)


def update(filepath: str = _keyring_dir, *args, **kwargs) -> None:
    """Store secret keys to cache. Call me like this:
    - store(openai="sk-...") # any number of services
    - store("path/to/secretkeys.json") # only one file 
    """

    if args and len(args) > 1 and not isinstance(args[0], str):
        raise ValueError("Only one positional argument (str) is allowed for filepath.")

    # load secret keys from a json filepath
    elif args and len(args) == 1 and isinstance(args[0], str):
        keypath = args[0]
        if not os.path.exists(keypath):
            raise ValueError(f"Filepath to keys {keypath} does not exist.")
        elif keypath.endswith(".json"):
            with open(keypath) as f:
                _update_keys_memory(json.load(f))
        else:
            raise ValueError(f"File type of {keypath} is not supported (only .json)")

    # load api keys from keyword arguments
    elif kwargs:
        _update_keys_memory(kwargs)

    else:
        raise ValueError("No arguments provided.")

    # save everything to cache and sync 
    _save_keys_to_cache(filepath)


def list() -> list:
    """List API keys from the live memory."""
    return [key for key in _keyring.keys()]


def get(service) -> str:
    """Get secret key from the live memory."""
    return _keyring.get(format_mem(check(service)))


def delete() -> None:
    """Delete cache from disk and reset live memory."""
    _keyring.clear()
    os.remove(_keyring_dir)


# --- private related to key management ---

def _verify_keys(keyring: dict) -> None:
    """Verify that all keys are well-formed."""
    _ = [check(key) for key in keyring.keys()]


def _update_keys_memory(kwargs: dict) -> None:
    """Update the keyring live memory."""
    keyring = {format_mem(k): v for k, v in kwargs.items()}
    _verify_keys(keyring) # check if keys are all well-formed
    _keyring.update(keyring) # then save to live memory


# --- private related to key cache i/o ---

def _autoload(filepath: str = _keyring_dir) -> int:
    """Load secret keys from the disk cache automatically."""
    load_dotenv(filepath) # from cache to os environment
    num_keys = _load_keys_from_env() # load keys from os env
    logging.debug(f"Loaded {num_keys} secret keys from cache" \
      if num_keys else "Cache is empty or does not exist yet.")


def _load_keys_from_env() -> int:
    """Load secret keys from os environment."""
    keys_from_cache = {
        format_mem(scratch(key)): os.environ.get(key)
        for key in os.environ.keys()
        if key.startswith(_prefix)
    }
    _update_keys_memory(keys_from_cache)
    return len(keys_from_cache)


def _save_keys_to_cache(filepath: str = _keyring_dir) -> None:
    """Save secret keys to the disk cache."""
    _verify_keys(_keyring) # sanity check before going on disk
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        for service, key in _keyring.items():
            f.write(f"{format_cache(service)}=\"{check_key(key)}\"\n")

