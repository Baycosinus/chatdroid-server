import json

def parse(j):
    string = json.dumps(j)
    print(string)
    return string

def convert(string):
    j = json.loads(string)
    print(j["username"])


j = {
    "username": "baycosinus",
    "password": "pass"
    }


q = json.dumps("")
print(q)