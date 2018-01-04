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
        # import os.path
        fn = os.getcwd()
        # fn = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        fn = os.path.join(fn, 'settings.json')
        # TODO: If 'settings.json' does not exist then create with default values and tell user to edit the file
        # Alternatively prompt for APIKey etc.
        # fn = os.path.join(os.path.dirname(__file__), 'settings.json')
        if not os.path.isfile(fn):
            with open(fn, 'w') as outfile:
                json.dump({
                    'Apikey':self.Apikey,
                    'Scheme':self.Scheme,
                    'Host':self.Host,
                    'Port':self.Port,
                    'UseCloudFX':self.UseCloudFX
                    }, outfile, indent=4, sort_keys=True)
        else:
            json_data=open(fn).read()
            data = json.loads(json_data)
            self.__dict__.update(data)

    def getUrl(self, path):
        if self.UseCloudFX:
            return "https://api.unifiedfx.com/" + path
        else:
            url = "{0}://{1}:{2}/AutomationFX/api/{3}"
            url = url.format(self.Scheme,self.Host,self.Port, path)
            return url

