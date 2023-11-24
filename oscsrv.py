# Import needed modules 
from osc4py3.as_eventloop import *
from osc4py3 import oscmethod as osm
import logging
import shutil

# define global variables
loop = 0
finished = False

# Init OSC server verbose logs
logging.basicConfig(format='%(asctime)s - %(threadName)s ø %(name)s - '
    '%(levelname)s - %(message)s')
logger = logging.getLogger("osc")
logger.setLevel(logging.DEBUG)
osc_startup(logger=logger)

# Define OSC patterns handlers

def handlerfunction_next(s):
    # Handler for osc command NEXT
    #Copy next page file to index.html
    global loop
    print('Received next: ',s,)
    if s == 1 :
        loop = loop + 1
        print('Page + '+str(loop))
        src = str(loop)+'.html'
        shutil.copy(src, 'index.html')
    else:
        print('unknown comand: ',s,)
    pass

def handlerfunction_prev(s):
    # Handler for osc command PREV
    #Copy previous page file to index.html
    global loop
    print('Received prev: ',s,)
    if s == 1 :
        loop = loop - 1
        print('---'+str(loop))
        src = str(loop)+'.html'
        #prevent loop to be less than zero
        if loop <= 0:
            loop = 0
            src = 'start.html'
        shutil.copy(src, 'main.html')
    else:
        print('unknown comand: ',s,)
    pass

def handlerfunction_stop(s):
    # Handler for osc command STOP
    # set variable to stop the osc server
    global finished
    print('Received stop: ',s,)
    if s == 1 :
        finished = True
        print('STOP STOP STOP')
    else:
        print('unknown comand: ',s,)
    pass


# -----------------------------------------------------------------------------------
#
# Main body
#
# -----------------------------------------------------------------------------------

# start OSC Server
osc_startup()

# Make server channels to receive packets.
osc_udp_server("10.2.20.54", 5005, "frbousrv")

# Associate Python functions with message address patterns, using default
# argument scheme OSCARG_DATAUNPACK.
osc_method("/test/next*", handlerfunction_next)
osc_method("/test/prev*", handlerfunction_prev)
osc_method("/test/stop*", handlerfunction_stop)
# copy start page to inex.html
shutil.copy('start.html','main.html')
# Periodically call osc4py3 processing method in your event loop.
while not finished:
    # …
    #print('Finished = '+ str(finished))
    osc_process()
    
    # …
# Properly close the system.
osc_terminate()