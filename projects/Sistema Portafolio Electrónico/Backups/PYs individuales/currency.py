import requests
import locale # obtiene el request de la url
from bs4 import BeautifulSoup as BS

locale.setlocale(locale.LC_ALL, 'en_US') # no hay es-MX pero se ve igual

# data = requests.get("http://data.fixer.io/api/latest?access_key=e00756b97a440e709fb5c10a517860a5&symbols=USD,MXN&format=1").json()
#
# rates = data["rates"]
#
# print(int(input(":"))/rates['USD']*rates['MXN'])

dollahs = input("Num:")

url = "https://www.google.com/search?q="
url += dollahs
url += "+usd+to+mxn"

# obtiene el request de la url
data = requests.get(url)
soup = BS(data.text, 'html.parser')

# # TESTING
# with open('util/htmlcode.html', 'w') as doc:
#     doc.write(data.text)
#
# # FIN TESTING

with o

ans = soup.find(attrs={"class": "BNeawe iBp4i AP7Wnd"}).text
print(ans)

price = ans.split()[0]
price_sin_formato = locale.atof(price)

costo_total = locale.currency(price_sin_formato, grouping=True)


print(price_sin_formato)
print(type(price_sin_formato))
