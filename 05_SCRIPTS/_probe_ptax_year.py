import json
import urllib.request

url = (
    "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
    "CotacaoDolarPeriodo(dataInicial=@di,dataFinalCotacao=@df)"
    "?@di='01-01-2025'&@df='12-31-2025'&$format=json&$orderby=dataHoraCotacao%20asc"
)
with urllib.request.urlopen(url, timeout=60) as r:
    d = json.loads(r.read().decode())
v = d.get("value", [])
print("rows", len(v))
if v:
    print("first", v[0]["dataHoraCotacao"])
    print("last", v[-1]["dataHoraCotacao"])
