import os

# Useful os variables
_base_dir = os.path.join(os.path.expanduser('~'), ".python-keyenv")
_keyring_dir = os.path.join(_base_dir, ".keyring.env")
_config_dir = os.path.join(_base_dir, "config")

# Lib convention
_prefix = "KV_"
