from automationfx import *
from example_tests import SimpleCallTest, ConsultTransferTest

# Query for the first 10 Registered phones ordered by DN
registered = queryPhone().filter(Phone.Status == 'Registered').order_by(Phone.DN.asc()).limit(10).all()

p1 = registered[0]
p2 = registered[1]
p3 = registered[2]

print(p1)
print(p2)
print(p3)

ConsultTransferTest(p1, p2, p3, 5)
