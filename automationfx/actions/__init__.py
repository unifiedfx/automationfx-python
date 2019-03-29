import time
from ..api.client import Client
from odata import ODataService
from ..models.phones import Phone
from ..auth import APIKeyAuth
from ..settings import Settings

api = None

def getClient():
    global api
    if api is None:
        api = Client()
    return api

def call(source, number):
    """Call number form source"""
    name = source.Name
    print(("Calling {0} from {1}".format(number, name)))
    return getClient().post("cti/calls/{0}/{1}".format(name, number), None)

def answer(source):
    print(("Answering call on {0}".format(source.Name)))
    return operation(source,'Answer')

def drop(source):
    print(("Dropping call on {0}".format(source.Name)))
    return operation(source,'Drop')

def hold(source):
    """Place the active call on the source phone on hold"""
    print(("Holding call on {0}".format(source.Name)))
    return operation(source,'Hold')

def unhold(source):
    print(("Unholding call on {0}".format(source.Name)))
    return operation(source,'UnHold')

def transfer(source):
    print(("Consult Transfer on {0}".format(source.Name)))
    return operation(source,'Transfer')

def conference(source):
    print(("Consult Conference on {0}".format(source.Name)))
    return operation(source,'Conference')

def offhook(source):
    print(("Offhook on {0}".format(source.Name)))
    return operation(source,'OffHook')

def operation(source, op):
    name = source.Name
    return getClient().post("cti/calls/{0}/{1}".format(name,op), None)


def sendDigits(source, digits):
    name = source.Name
    print(("Send Digits '{0}' on {1}".format(digits, name)))
    return getClient().post("cti/calls/{0}/digits/{1}".format(name,digits), None)

def sendData(source, data):
    name = source.Name
    return getClient().post("cti/data/{0}".format(name), data=data)

def sendUri(source, uri):
    name = source.Name
    return getClient().postString("cti/execute/{0}".format(name), uri)

def pause(delay):
    print(("Pausing for {0} seconds".format(delay)))
    time.sleep(delay)

def macro(source, macro):
    name = source.Name
    print(("Sending macro '{0}' to {1}".format(macro, name)))
    return getClient().postString("phones/macro/{0}".format(name),macro)

def sendMessage(message, destination):
    """
    Send Message
    ============
    Send a text/audio message to a group of phone using an existing message and filter defined in the AutomationFX admin interface
    - message (the name of the message to send)
    - destination (the name of the filter to send the message too)
    """
    return getClient().post("messages/{0}/send".format(message), None, params={'filter':destination})

def sendRawMessage(message, source):
    return getClient().post("messages/send", data=message, params={'filter':source})

def listResource(resource, search=None, fields=None):
    params = {'detailed':'true'}
    if search is not None:
        params.update({'search':search})
    if fields is not None:
        params.update({'fields':fields})
    return getClient().get("axl/{0}".format(resource), params=params)

def getResource(resource, id):
    return getClient().get("axl/{0}/{1}".format(resource,id))

def addResource(resource, data):
    return getClient().post("axl/{0}".format(resource), data=data)

def updateResource(resource, id, data):
    return getClient().put("axl/{0}/{1}".format(resource,id),data)

def deleteResource(resource, id):
    return getClient().delete("axl/{0}/{1}".format(resource,id))

def sqlQuery(query):
    return getClient().postString("axl/sql/query", query)

def sqlUpdate(update):
    return getClient().postString("axl/sql/update", update)

def queryPhone():
    settings = Settings()
    Service = ODataService(settings.getUrl('oData'), reflect_entities=False, base=Phone, auth=APIKeyAuth(settings.Apikey))
    return Service.query(Phone)

def findPhone(param):
    settings = Settings()
    Service = ODataService(settings.getUrl('oData'), reflect_entities=False, base=Phone, auth=APIKeyAuth(settings.Apikey))
    return queryPhone().filter(param).first()
