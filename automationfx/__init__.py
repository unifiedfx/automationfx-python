from odata import ODataService
from .models.phones import Phone
from .auth import APIKeyAuth
from .settings import Settings
from .actions import *

__all__ =[
    'queryPhone',
    'findPhone',
    'Phone',
    'call',
    'answer',
    'drop',
    'hold',
    'unhold',
    'transfer',
    'conference',
    'sendDigits',
    'sendData',
    'sendUri',
    'pause',
    'macro',
    'sendMessage',
    'sendRawMessage',
    'migrate',
    'listResource',
    'getResource',
    'addResource',
    'updateResource',
    'deleteResource',
    'sqlQuery',
    'sqlUpdate']
