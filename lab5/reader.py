import pipes
import os
import sys
import logging
import time
import thread

node, next_node, previous_node = '', '', ''
default_priority = '255'

def node_1():
    global node, next_node, previous_node
    node, next_node, previous_node = '1', '2', '3'

def node_2():
    global node, next_node, previous_node
    node, next_node, previous_node = '2', '3', '1'

def node_3():
    global node, next_node, previous_node
    node, next_node, previous_node = '3', '1', '2'

options = {
    1 : node_1,
    2 : node_2,
    3 : node_3
}

if len(sys.argv) != 2:
    print 'Usage: python reader.py node_number'
    sys.exit()
else:
    node = int(sys.argv[1])
    if node > 0 and node < 4:
        options[node]()

logging.basicConfig(filename='info.log',level=logging.INFO)
logger = logging.getLogger("Node " + node)

messages = []
num_messages = 0
send_queue = []

def processing(message):
    global send_queue
    dst, priority, line = message.split(':')
    if dst == node:
        print line
    else:
        send_queue.append(message)

def read_from_pipe():
    global messages
    global num_messages
    global send_queue
    while 1:
        message = open('pipefile_' + previous_node + '_' + node, 'r').read().rstrip('\n')
        if message:
            if message == 'marker':
                time.sleep(3)
                open('pipefile_' + previous_node + '_' + node, 'w').write('')
                if send_queue:
                    send_queue.sort()
                    send_queue.reverse()
                    msg = send_queue.pop()
                    open('pipefile_' + node + '_' + next_node, 'w').write(msg)
                    logger.info("Redirected message: " + msg + " to next node")
                else:
                    open('pipefile_' + node + '_' + next_node, 'w').write('marker')
                    logger.info("Send marker to next node")
            else:
                open('pipefile_' + previous_node + '_' + node, 'w').write('')
                #print message
                messages.insert(0,[str(message.split(':')[1]), str(num_messages), message])
                logger.info("Received message: " + str(message.split(':')[-1]))
                messages.sort()
                messages.reverse()
                num_messages += 1
                processing(message)

                if send_queue:
                    send_queue.sort()
                    send_queue.reverse()
                    msg = send_queue.pop()
                    open('pipefile_' + node + '_' + next_node, 'w').write(msg)
                    logger.info("Redirected message: " + msg + " to next node")
                else:
                    open('pipefile_' + node + '_' + next_node, 'w').write('marker')
                    logger.info("Send marker to next node")
                #print messages

def messages_processing():
    global messages
    while 1:
        if messages:
            message = messages.pop()
            #print message[-1]
            processing(str(message[-1]))
        #time.sleep(3)

thread.start_new_thread( read_from_pipe, () )
#thread.start_new_thread( messages_processing, () )

while 1:
   pass
