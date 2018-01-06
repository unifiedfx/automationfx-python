import os
import os.path
import json

class Settings:
    Apikey = ""
    Scheme = "http"
    Host = "127.0.0.1"
    Port = 8181
    UseCloudFX = False
    def __init__(self):
        if not os.path.isfile(self.filename()):
            with open(self.filename(), 'w') as outfile:
                json.dump({
                    'Apikey':self.Apikey,
                    'Scheme':self.Scheme,
                    'Host':self.Host,
                    'Port':self.Port,
                    'UseCloudFX':self.UseCloudFX
                    }, outfile, indent=4, sort_keys=True)
        else:
            json_data=open(self.filename()).read()
            data = json.loads(json_data)
            self.__dict__.update(data)

    def filename(self):
        fn = os.getcwd()
        fn = os.path.join(fn, 'settings.json')
        return fn

    def save(self):
        with open(self.filename(), 'w') as outfile:
            json.dump({
                'Apikey':self.Apikey,
                'Scheme':self.Scheme,
                'Host':self.Host,
                'Port':self.Port,
                'UseCloudFX':self.UseCloudFX
                }, outfile, indent=4, sort_keys=True)

    def getUrl(self, path):
        if self.UseCloudFX:
            return "https://api.unifiedfx.com/" + path
        else:
            url = "{0}://{1}:{2}/AutomationFX/api/{3}"
            url = url.format(self.Scheme,self.Host,self.Port, path)
            return url

