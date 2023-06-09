# python-keyenv: Your local, safe keyring 🕵️‍♂️

<!-- ![Tests](https://github.com/andreakiro/python-keyenv/actions/workflows/tests.yml/badge.svg) -->

Go-to solution for effortless secret keys management. This lib/tool allows you to securley store (once for all!) and swiftly load secret key-value pairs from a local cache using dotenv file logic. Now, accessing your favorite API keys across all your projects is as simple as saying hello.

## Usage

### Save your keys and interact with cache

Run this anywhere in your computer to safely store a key on disk
```bash
$ keyenv -n {service name} -sk {secret key}
```

You can of course update a service's key anytime, or list all services
```bash
$ keyenv update -n {service name} -sk {new secret key}
$ keyenv list # this will list all service names
```

You can also provide path to a `json` file to store/update commands
```bash
$ keyenv store -p {path/to/json}
$ keyenv update -p {path/to/json}
```

You could also perform same actions from a Python script if needed
```python
import keyenv as kv
kv.store(service="secret")
kv.update(service="secret")
kv.store("path/to/json/keys")
print(kv.list())
```

### Load your keys across your Python projects

You can then access all of your keys with `keyenv.get(service)` in your Python code 🥳

```python
import langchain.llms as llms
import keyenv as kv

os.environ["OPENAI_API_KEY"] = kv.get("openai")

llm = llms.OpenAI()
llm_chain = LLMChain(prompt="Hi my name is", llm=llm)
llm_chain.run()
```

## Installation

🚨 To install `keyenv`, use pip: ```pip install keyenv```.
