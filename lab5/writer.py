import pipes
import os
import sys
import logging
import time
import thread
import re

line = ''

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
    print 'Usage: python writer.py node_number'
    sys.exit()
else:
    node = int(sys.argv[1])
    if node > 0 and node < 4:
        options[node]()

logging.basicConfig(filename='info.log',level=logging.INFO)
logger = logging.getLogger("Node " + node)

while 1:
    line = sys.stdin.readline()
    if not line:
      break
    if re.match('\d+:\d+:\w+', line) is None:
        line = next_node + ':' + default_priority + ':' + line

    while 1:
        message = open('pipefile_' + previous_node + '_' + node, 'r').read().rstrip('\n')
        if message == 'marker':
            open('pipefile_' + previous_node + '_' + node, 'w').write('')
            open('pipefile_' + node + '_' + next_node, 'w').write(line)
            break

    logger.info("Sended message: " + line)
