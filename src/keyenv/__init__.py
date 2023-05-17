import os

from .core import _autoload, _keyring
from .core import store, update, list, get, delete
from .constvars import _config_dir, _keyring_dir

# load from cache immediately
_autoload(_keyring_dir)

__all__ = ["store", "update", "list", "get", "delete", "__version__", "_keyring"]
