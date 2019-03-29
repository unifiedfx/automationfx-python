from odata.entity import EntityBase
from odata.entity import declarative_base
from odata.property import IntegerProperty, StringProperty, DatetimeProperty


class Phone(declarative_base()):
    __odata_type__ = 'ProductDataService.Objects.Product'
    __odata_collection__ = 'oData/Phones'

    Name = StringProperty('Name')
    IPAddress = StringProperty('IPAddress')
    DN = StringProperty('DN')
    Description = StringProperty('Description')
    Category = StringProperty('Category')
    User = StringProperty('User')
    DevicePool = StringProperty('DevicePool')
    Location = StringProperty('Location')
    Region = StringProperty('Region')
    CMGroup = StringProperty('CMGroup')
    DeviceCSS = StringProperty('DeviceCSS')
    PhoneLoad = StringProperty('PhoneLoad')
    ButtonTemplate = StringProperty('ButtonTemplate')
    AddonModule = StringProperty('AddonModule')
    EMEnabled = StringProperty('EMEnabled')
    LoginTime = StringProperty('LoginTime')
    Status = StringProperty('Status')
    ActiveServer = StringProperty('ActiveServer')
    Model = StringProperty('Model')
    LastUpdate = StringProperty('LastUpdate')
    LastRefresh = StringProperty('LastRefresh')
    Timestamp = StringProperty('Timestamp')
    LoginTime = StringProperty('LoginTime')
    Firmware = StringProperty('Firmware')
    ClusterGUID = StringProperty('ClusterGUID')
    DeviceState = StringProperty('DeviceState')
    LastActivity = StringProperty('LastActivity')

    def __str__(self):
        return "{0} ({1})".format(self.Name, self.DN)
