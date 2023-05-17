import keyenv as kv

# loading from cache on the fly ;)
print(kv.get("openai"))
print(kv.get("anthropic"))
