# AutomationFX SDK for Python

A Python library for the AutomationFX REST API. AutomationFX is an integration platform from [UnifiedFX](https://www.unifiedfx.com) that exposes Cisco Unified Communication Manager (CUCM) complex and varied interfaces via a simple unified REST API. AutomationFX enables a number of scenarios with minimal effort/complexity:

* Automate/Script [PhoneView](https://www.unifiedfx.com/products/unifiedfx-phoneview) Macros
* CTI Screen Pop-up
* Mass notificaiton/messaging to Cisco IP Phones ([Sample](https://github.com/unifiedfx/automationfx-python/blob/master/example_sendmessage.py))
* CUCM Provisioning
* Cloud enable Cisco Unified Communications Manager (CUCM) API's
* Automated Testing
    * [Example 1](https://github.com/unifiedfx/automationfx-python/blob/master/example_testcall1.py) - Call SimpleCallTest from [Example Tests](https://github.com/unifiedfx/automationfx-python/blob/master/example_tests.py)
    * [Example 2](https://github.com/unifiedfx/automationfx-python/blob/master/example_testcall2.py) - Call ConsultTransferTest from [Example Tests](https://github.com/unifiedfx/automationfx-python/blob/master/example_tests.py)
    
For an overview of AutomationFX and additional resources please visit [Awesome-AutomationFX](https://github.com/unifiedfx/awesome-automationfx)

# Requirements

* Python 2.7 (or greater) [Download](https://www.python.org/downloads/)
* AutomationFX - included as part of the PhoneFX feature in [PhoneView Lab Edition](https://www.unifiedfx.com/unifiedfx-free-software/phoneview-free-lab-edition)  ([Download PhoneView 6.1+](https://download.unifiedfx.com/PhoneView/alpha))
* Cisco Unified Communications Manager (CUCM) 8.0 (or above)

*Note: PhoneView and AutomationFX require Windows 7/Windows Server 2008 R2 (or newer including Windows 10 and Windows Server 2016) however the AutomationFX Python SDK can run on Mac/Linux/Windows*

# Installation

Install using pip:

```
pip install automationfx
```

*Note: On Windows the 'pip' command may not be included in the PATH, to call directly use:*

```
\Python27\Scripts\pip install automationfx
```

# Setup

Once the 'automationfx' Python module is installed simply run 'automaitonfx' from a command prompt to setup and test connectivity to AutomationFX/CUCM. You will be prompted for an Apikey to connect to AutomationFX and the host details for your AutomationFX instance. These details are saved to a 'settings.json' file in the directory where you ran the 'automationfx' command:

```
automationfx
```

*Note: On Windows the 'scripts' folder may not be included in the PATH, to call directly use:*

```
\Python27\Scripts\automationfx
```

```
automationfx
Set Apikey? [Y/n] y
Apikey: 12345
Use CloudFX? [Y/n] n
Change AutomationFX Host (127.0.0.1)? [Y/n] y
AutomationFX Host: 10.10.11.178
Change AutomationFX Port (8181)? [Y/n] n
Change AutomationFX Scheme (http)? [Y/n] n
AutomationFX Setup:
	Apikey: 12345
	Use CloudFX: False
	Host: 10.10.11.178
	Port: 8181
	Scheme: http
Save Settings? [Y/n] y
AFX>
```

Note: To obtain an Apikey open the Apps page on the AutomationFX admin interface (i.e. http://127.0.0.1:8181/#/app/api/apps), create an App then copy the Apikey

# Usage

## API
Within a python script/file simply import the automationfx module 'import automationfx', from there you can call any of the [actions](https://github.com/unifiedfx/automationfx-python/blob/master/automationfx/actions/__init__.py) availble from the AutomationFX API:

* queryPhone
* findPhone
* call
* answer
* drop
* hold
* unhold
* transfer
* conference
* sendDigits
* sendData
* sendUri
* pause
* macro
* sendMessage
* sendRawMessage
* listResource
* getResource
* addResource
* updateResource
* deleteResource
* sqlQuery
* sqlUpdate

### Send Message

Send a text/audio message 'Message1' to multiple phones (filter 'TestPhones'):

```
import automationfx
sendMessage("Message1", "TestPhones")
```

*Note: To create/update a message open the Messages page on AutomationFX (http://127.0.0.1:8181/#/app/message)*

*Note: To create/update a filter open the Phones page on AutomationFX (http://127.0.0.1:8181/#/app/phonelist) then check the relevant criteria in the filter panel on the bottom of the left hand menu sidebar*

### SQL Query

SQL Query CUCM database:

```
import automationfx
print(sqlQuery("SELECT name, description FROM device"))
```

Note: The following Example shows how to export the results to a CSV file: [example_sqlquery.py](https://github.com/unifiedfx/automationfx-python/blob/master/example_sqlquery.py)

### Make a Call

Place a call from a Cisco Phone (Primary DN = '50005') to '1234':

```
import automationfx
p1 = findPhone(Phone.DN == '50005')
call(p1, '1234')
```

### Answer a Call

Answer a call on a Cisco Phone (Primary DN = '50005'):

```
import automationfx
p1 = findPhone(Phone.DN == '50005')
answer(p1)
```

### Hangup a Call

Hangup all calls on a Cisco Phone (Primary DN = '50005'):

```
import automationfx
p1 = findPhone(Phone.DN == '50005')
drop(p1)
```

### Establish a call between two phones

Establish a call between extension '50005' and '10136', wait for 10 seconds then hangup

```
import automationfx
p1 = findPhone(Phone.DN == '50005')
p2 = findPhone(Phone.DN == '10136')
call(p1, p2.DN)
answer(p2)
pause(10)
drop(p1)
```

## Phones

A number of the API actions require a phone object to perfom the relevant action on. The API includes the 'queryPhone' and 'findPhone' functions to provide a simple and flexible way to obtain the relevant phone(s) to perform actions against.

The AutomationFX REST API includes an [oData](http://www.odata.org/getting-started/basic-tutorial/) endpoint for all the phones availble on the system. This provides a flexible way to query for phones using a number of [Phone](https://github.com/unifiedfx/automationfx-python/blob/master/automationfx/models/phones.py) object properties such as DN, Description, DevicePool, IPAddress, User, Model, Location, Region

* The 'findPhone' function returns a single Phone instance, if there are multiple matches it will be the first found
* The 'queryPhone' function returns an array of Phone instances

### Find Phones

Find a single phone based on DN = '50005':

```
import automationfx
p1 = findPhone(Phone.DN == '50005')
```

Find a single phone based on Device Name = 'SEP2834A282E799':

```
import automationfx
p1 = findPhone(Phone.Name == 'SEP2834A282E799')
```

Find a single/first phone with 'demo' contained in the description:

```
import automationfx
p1 = findPhone(Phone.Description.contains('demo'))
```

## Query Phones

The AutomationFX module includes an [oData client](https://github.com/tuomur/python-odata) that exposes a query object to build an oData query with.
The [query object](https://github.com/unifiedfx/automationfx-python/blob/master/automationfx/odata/query.py) exposes a 'filter' function that accepts filter statements to convert to the relevant oData request when applied.

List the first 10 registered phones ordered by Primary Extension/DN

```
import automationfx
registered = queryPhone().filter(Phone.Status == 'Registered').order_by(Phone.DN.asc()).limit(10).all()
```
*Note: The 'all()' function call on the end triggers the filter statement to be executed and return an array, by omitting the 'all()' function call an enumberable will be returned. Only when iterating through the enumberable will the call to the oData endpoint by made.*

## CLI

In addition to the API actions the 'automationfx' module includes it's own Command Line Interface (CLI) that exposes a number of the actions above in a simple interactive interface that is perfect for testing/exploring what the actions do:

### Setup

Note: If you have not previously setup the connection to the system running AutomationFX you will be prompted for the Apikey and host details. This information is saved to a local 'settings.json' and will be used antomatically the next time the 'automationfx' cli is started from that same location. If you wish to change the settings you can either edit the 'settings.json' file directly or use the 'setup' cli command

```
automationfx
AFX> setup
Set Apikey? [Y/n] y
Apikey: 12345
Use CloudFX? [Y/n] n
Change AutomationFX Host (127.0.0.1)? [Y/n] y
AutomationFX Host: 10.10.11.178
Change AutomationFX Port (8181)? [Y/n] n
Change AutomationFX Scheme (http)? [Y/n] n
AutomationFX Setup:
	Apikey: 12345
	Use CloudFX: False
	Host: 10.10.11.178
	Port: 8181
	Scheme: http
Save Settings? [Y/n] y
AFX>
```

### Opening the CLI

To start the CLI simply run 'automationfx' from a command prompt:

```
automationfx
Welcome to the AutomationFX cli. Type help or ? to list commands.
AFX>
```

### Usage

Get available commands:

```
AFX> ?
Documented commands (type help <topic>):
========================================
answer  cd          connect  drop  hold   offhook  setup     unhold
call    conference  digits   help  macro  run      transfer  uri
```

Get Help:

```
AFX> help call
Place a call from a source phone extension to any number "call 50005 10134"
```

There are two ways to use actions that work against phones:

1. From the root prompt 'AFX>' pass the source phone extension as the fist argument i.e. 'call 50005 10134' to call 10134 from the phone with extension 50005
2. Set the context to the phone to perfom actions on and omit the fist argument using the 'cd' Choose Device command

Using the root prompt:

```
AFX> call 50005 10134
```

Setting the phone context to a particular phone extension/DN using the 'cd' command (Choose Device)

```
AFX> cd 50005
AFX/50005> call 10134
```

*Note: The prompt will update to indicate the current context by including the device extension/DN*

To change context to a different extension:

```
AFX/50005> cd 10136
AFX/10136>
```

Place a call from 50005 to 10136:
```
AFX> cd 50005
AFX/50005>call 10136
Calling 10136 from SEP2834A282E799
AFX/50005>
```

Answer a call on 10136:

```
AFX/50005>cd 10136
AFX/10136>answer
Answering call on SEP382056192034
AFX/10136>
```

Hangup/Drop call:
```
AFX/10136>drop
Dropping call on SEP382056192034
```

