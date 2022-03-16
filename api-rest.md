# Buscar el Primer elemento en una factura
```  
import requests
response = requests.get("http://127.0.0.1")
print(response)
```  

# Buscar productos
``` 
import requests
print("begin")
url = "https://fakestoreapi.com/products"
payload={}
headers = {}
response = requests.request("GET", url, headers=headers, data=payload)
json = response.json()
for i in json:
    print(i["title"])
    print("====")
```  
