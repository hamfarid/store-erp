import json, urllib.request, urllib.error

BASE = 'http://127.0.0.1:5002/api/auth/login'

def post(payload):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(BASE, data=data, headers={'Content-Type':'application/json'}, method='POST')
    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode('utf-8', 'ignore')
            print('STATUS', resp.status)
            print(body)
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', 'ignore')
        print('STATUS', e.code)
        print(body)

print('--- empty payload {} ---')
post({})
print('\n--- wrong creds ---')
post({'username':'admin','password':'wrong'})

