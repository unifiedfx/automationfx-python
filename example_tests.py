
from automationfx import *

def SimpleCallTest(t1, t2, duration = 10):
    """
    Simple Call Test
    ================
    Accepts 2 test phones (t1,t2) as an argument
    Optionally specifiy the duration of the call (default 10 seconds)

    1. Establishes call between t1 and 't2.DN' (The primary line on t2)
    2. Pauses for 'duration' seconds (10 seconds by default)
    10. Drop the call form t1
    """
    call(t1, t2.DN)
    answer(t2)
    pause(duration)
    # Snapshot/Validate
    # Use Assert style for validation
    drop(t1)

def ConsultTransferTest(t1, t2, t3, duration = 10):
    """
    Consult Transfer
    ================
    Accepts 3 test phones (t1,t2,t3) as an argument
    Optionally specifiy the duration of the call (default 10 seconds)

    1. Establishes call between t1 and 't2.DN' (The primary line on t2)
    2. Pauses for 'duration' seconds (10 seconds by default)
    3. Initiaites a consult transfer on t2
    4. Pauses for 1 second
    5. Dials 't3.DN' (The primary line on t3)
    6. Pauses for 3 seconds to allow the call to arrive on t3
    7. Complete the consult transfer on t2
    8. Answer the transfered call on t3
    9. Pauses for 'duration' seconds (10 seconds by default)
    10. Drop the call form t3
    """
    call(t1,t2.DN)
    answer(t2)
    pause(duration)
    # Snapshot/Validate
    transfer(t2)
    pause(1)
    sendDigits(t2,t3.DN)
    pause(3)
    transfer(t2)
    answer(t3)
    # Snapshot/Validate
    pause(duration)
    drop(t3)