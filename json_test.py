import json,db

def parse(j):
    string = json.dumps(j)
    print(string)
    return string

def convert(string):
    j = json.loads(string)
    print(j["username"])


j = {
    "id": "3",
    "username": "baycosinus",
    "password": "pass"
    }


print(json.dumps(RESPONSE)["online_users"])
