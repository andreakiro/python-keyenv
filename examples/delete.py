import keyenv as kv

print(kv._keyring)
kv.delete()
print(kv._keyring)
