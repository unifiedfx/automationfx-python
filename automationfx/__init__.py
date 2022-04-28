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
    'callInfo',
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
    'startMonitor',
    'stopMonitor',
    'migrate',
    'listResource',
    'getResource',
    'addResource',
    'updateResource',
    'deleteResource',
    'sqlQuery',
    'sqlUpdate']
