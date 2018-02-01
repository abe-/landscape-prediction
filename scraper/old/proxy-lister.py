import requests

f = open("proxies.txt","w")

r = requests.get("http://gimmeproxy.com/api/getProxy?country=DE,FR,UK,ES")
t = r.json()
string_proxy = t['ip'] + ":" + t['port']
f.write(string_proxy)

f.close()
