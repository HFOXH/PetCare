import urllib.request
import json
try:
    url = 'http://localhost:8000/api/v1/health'
    with urllib.request.urlopen(url, timeout=5) as resp:
        data = json.load(resp)
        print('SUCCESS:', data)
except Exception as e:
    print('ERROR:', type(e).__name__, str(e)[:200])