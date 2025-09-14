import requests

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0"})

url = f"https://investidor10.com.br/acoes/petr4/"
r = session.get(url)
print(r.text[:2000])
with open(f"testsoup.html", "w", encoding="utf-8") as f:
    f.write(r.text)