
import http.client

conn = http.client.HTTPSConnection("lingua-robot.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "ae653d7afbmsh42516d3cbf4c4f2p1eb68ejsnb4a6f04f31e3",
    'x-rapidapi-host': "lingua-robot.p.rapidapi.com"
}

conn.request("GET", "/language/v1/entries/en/example", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))