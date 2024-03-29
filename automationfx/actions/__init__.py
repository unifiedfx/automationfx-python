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

def call(source, number,line='1'):
    """Call number form source"""
    name = source.Name
    print(("Calling {0} from {1}".format(number, name)))
    return getClient().post("cti/calls/{0}/{1}".format(name, number), None, {'address': line})

def answer(source):
    print(("Answering call on {0}".format(source.Name)))
    return operation(source,'Answer')

def drop(source):
    print(("Dropping call on {0}".format(source.Name)))
    return operation(source,'Drop')

def callInfo(source):
    print(("Getting call info on {0}".format(source.Name)))
    return getClient().get("cti/calls/legacy/{0}".format(source.Name))

def startMonitor(source, supervisor):
    """Start a Call Monitoring session on source phone and send media to supervisor phone"""
    name = source.Name
    supervisorName = supervisor.Name
    print(("Monitoring call on {0} from {1}".format(name, supervisorName)))
    return getClient().post("cti/calls/{0}/monitor/{1}".format(name, supervisorName), None)

def stopMonitor(source):
    """Stop the Call Monitoring Session on source phone"""
    name = source.Name
    print(("Stopping call monitoring session on {0}".format(name)))
    return getClient().delete("cti/calls/{0}/monitor".format(name), None)

def hold(source):
    """Place the active call on the source phone on hold"""
    print(("Holding call on {0}".format(source.Name)))
    return operation(source,'Hold')

def unhold(source):
    print(("Unholding call on {0}".format(source.Name)))
    return operation(source,'UnHold')

def transfer(source, number = None):
    if number is not None:
        print(("Direct Transfer from {0} to {1}".format(source.Name, number)))
        return getClient().post("cti/calls/{0}/transfer/{1}".format(source.Name,number), None)
    else:
        print(("Consult Transfer on {0}".format(source.Name)))
        return operation(source,'Transfer')

def conference(source, number= None):
    if number is not None:
        print(("Direct Conference from {0} to {1} ".format(source.Name, number)))
        return getClient().post("cti/calls/{0}/conference/{1}".format(source.Name,number), None)
    else:
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

def migrate(oldphone, newphone, newmodel, newprotolcol = "SIP", enableactivationcode = False):
    """
    Initiate a Phone Migration
    ============
    Intiates a phone migration in CUCM 
    - oldphone(string) : Name of the old phone to migrate from (required).
    - newphone(string) : Name of the new phone, if not provided a random name will be generated.
    - newmodel(string) : New phone Model, This is not required if new name (newphone) is provided and the new phone exist in CUCM with the correct model. 
    - newprotocol(string) - New phones protocol (if not provided defaults to SIP)
    - enableactivationcode(boolean) - Generates an Activation Code. Requires UCM 12.5+ and Device Default 'Onboarding Method' for model should be configured to 'Activation Code'     
    """
    model = {'oldName': oldphone, 'newName': newphone, 'newModel': newmodel, 'newProtocol': newprotolcol, 'createActivationCode' :enableactivationcode}
    return getClient().post("migrate", data=model)

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
