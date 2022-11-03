import http.client
import mimetypes
conn = http.client.HTTPSConnection("api.domain.com.au")
payload = ''

#use your own api key
headers = {
  'X-API-Key': 'key_fbb1b284698703e6b3d9476a3fd5a2d4',
  'key_eb41b05e4e54b4868a50cc3cef5954d9': ''
}
conn.request("GET", "/v2/demographics/NSW/Redfern/2016", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))