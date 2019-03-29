import json
import requests
from ..settings import Settings

class Client:
    settings = Settings()
    def __init__(self,session=None):
        if session is None:
            self.session = requests.Session()
        else:
            self.session = session
        self.session.headers.update({'apikey':self.settings.Apikey})

    def get(self, path, params=None):
        url = self.settings.getUrl(path)
        response = self.session.get(url, params=params)
        return response.json()
    
    def post(self, path, data, params=None):
        url = self.settings.getUrl(path)
        headers = {
            'Content-Type': 'application/json',
        }
        data = json.dumps(data)
        response = self.session.post(url, data=data, headers=headers, params=params)
        return response.json()

    def postString(self, path, data, params=None):
        url = self.settings.getUrl(path)
        headers = {
            'Content-Type': 'text/plain',
        }
        response = self.session.post(url, data=data, headers=headers, params=params)
        try:
            jdata = response.json() 
        except (ValueError, e):
            return
        return jdata
    
    def put(self, path, data, params=None):
        url = self.settings.getUrl(path)
        headers = {
            'Content-Type': 'application/json',
        }
        data = json.dumps(data)
        response = self.session.put(url, data=data, headers=headers, params=params)
        return response.json()
    
    def delete(self, path, params=None):
        url = self.settings.getUrl(path)
        response = self.session.delete(url, params=params)
        return response.json()