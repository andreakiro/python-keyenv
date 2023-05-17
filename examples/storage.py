import keyenv as kv

kv.store(openai="this-is-a-secret-key")
print("store first;", kv._keyring)

kv.update(openai="this-is-the-correct-secret-key")
print("update first;", kv._keyring)

kv.store(anthropic="this-is-rather-cool")
print("store second;", kv._keyring)

print("getting openai; ", kv.get("openai"))
print("list all services; ", kv.list())
