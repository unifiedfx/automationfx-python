from automationfx import *
import pprint

def getLineId(line):
    "Helper function that returns the line in the format DN/DN-Partition i.e. '50005' (no partition) or '50005-Internal' (partition = 'Internal'). This format can be used as the Id of the line when calling getResource/updateResource/deleteResource"
    return line['pattern'] if line['routePartitionName'] is None else "{0}-{1}".format(line['pattern'], line['routePartitionName']['Value'])

# It is recommended to not list all resources on production systems unless you know that resource type will not return a large number of records (i.e. less that 1000)
# This is not a capcity issue, just good practice to avoid unnecessarily performing large queries frequently on CUCM
# This query only returns Lines that have an extension/pattern that start with '500' with any 'routePartitionName', the '%' character is the wildcard
lines = listResource('Line', search='pattern=500%')

# Print the results, in the format DN/DN-Partition i.e. '50005' (no partition) or '50005-Internal' (partition = 'Internal')
for line in lines:
    print(getLineId(line))

# If at least one line was found then get the full line resource for the first match
if len(lines) > 0:
    line = getResource('Line', getLineId(lines[0]))
    # PrettyPrint the Line object, helpful to understand the data structure
    pprint.pprint(line)
    # Print the Call Forward All Destiantion
    cfaDestination = line['callForwardAll']['destination']
    print("Line {0} Call Forward All: {1}".format(line['pattern'], ("Not set" if cfaDestination is None else cfaDestination)))
    # Update the lines 'callForwardAll/destination', simply update to an empty string '' to clear CallForwardAll
    newCfaDestination = '4000'
    line = updateResource('Line', getLineId(lines[0]), {'callForwardAll':{'destination':newCfaDestination}})

