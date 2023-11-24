# Import needed modules from osc4py3
from osc4py3.as_eventloop import *
from osc4py3 import oscmethod as osm
import logging
import shutil

loop = 0
finished = False

logging.basicConfig(format='%(asctime)s - %(threadName)s ø %(name)s - '
    '%(levelname)s - %(message)s')
logger = logging.getLogger("osc")
logger.setLevel(logging.DEBUG)
osc_startup(logger=logger)

def handlerfunction_next(s):
    # Will receive message data unpacked in s
    global loop
    print('Received next: ',s,)
    if s == 1 :
        loop = loop + 1
        print('+++'+str(loop))
        src = str(loop)+'.html'
        shutil.copy(src, 'main.html')
    else:
        print('unknown comand: ',s,)
    pass

def handlerfunction_prev(s):
    # Will receive message data unpacked in s
    global loop
    print('Received prev: ',s,)
    if s == 1 :
        loop = loop - 1
        print('---'+str(loop))
        src = str(loop)+'.html'
        if loop == 0:
            src = 'start.html'
        shutil.copy(src, 'main.html')
    else:
        print('unknown comand: ',s,)
    pass

def handlerfunction_stop(s):
    # Will receive message data unpacked in s
    global finished
    print('Received stop: ',s,)
    if s == 1 :
        finished = True
        print('STOP STOP STOP')
    else:
        print('unknown comand: ',s,)
    pass
    
osc_startup()

# Make server channels to receive packets.
osc_udp_server("10.2.20.54", 5005, "frbousrv")

# Associate Python functions with message address patterns, using default
# argument scheme OSCARG_DATAUNPACK.
osc_method("/test/next*", handlerfunction_next)
osc_method("/test/prev*", handlerfunction_prev)
osc_method("/test/stop*", handlerfunction_stop)

# Periodically call osc4py3 processing method in your event loop.
finished = False
shutil.copy('start.html','main.html')
while not finished:
    # …
    #print('Finished = '+ str(finished))
    osc_process()
    
    # …

# Properly close the system.
osc_terminate()