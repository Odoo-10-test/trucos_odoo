```  
import requests

url = 'https://eu102.chat-api.com/instance99645/sendMessage?token=iwu09tzu212lk'

params = {
    "phone": "79912422",
    "body": "WhatsApp API on chat-api.com works good"
}

response = requests.post(url, params=params)

response.json()
```  
