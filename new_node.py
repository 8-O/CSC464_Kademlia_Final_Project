'''
CSC464 UVic Fall 2018

This program bootstraps a new node to the network's starter node. The user can also
choose to set a (key, value) pair or get a value for a given keyself.

Thor Reite V00809409
12/14/2018
'''

import asyncio
from kademlia.network import Server
import logging
import sys
import getopt

STARTER_NODE = ("0.0.0.0", 1111)

def main(argv):
    port_given = False
    key_given = False
    set_key = False
    get_key = False
    try:
        opts, args = getopt.getopt(argv,"p:k:s:g:",["set=","get="])
    except getopt.GetoptError:
        print("python3 new_node.py -p <port> -k <key> -s <set_value> -g <get_key>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-p":
            port_given = True
            port = arg
        elif opt == "-k":
            key_given = True
            key = arg
        elif opt in ("-s", "set="):
            set_key = True
            key_value = arg
        elif opt in ("-g", "get="):
            get_key = True
            gkey = arg

    if port_given is False:
        print("python3 new_node.py -p <port> -k <key> -s <set_value> -g <get_key>")
        sys.exit(1)

    node = Server()
    node.listen(port)

    # Bootstrap the node by connecting to other known nodes, in this case
    # ("0.0.0.0", 1111) is the starting node.
    loop = asyncio.get_event_loop()
    loop.run_until_complete(node.bootstrap([STARTER_NODE]))

    # set a user specified value for the user specified key on the network
    if set_key is True:
        if key_given is True:
            loop.run_until_complete(node.set(key, key_value))
        else:
            print("python3 new_node.py -p <port> -k <key> -s <set_value> -g <get_key>")
            sys.exit(1)

    # get the value associated with the user specified key from the network
    if key_given is True or get_key is True:
        if get_key is True:
            result = loop.run_until_complete(node.get(gkey))
            print(result)
        elif set_key is False:
            result = loop.run_until_complete(node.get(key))
            print(result)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        node.stop()
        loop.close()
        sys.exit(0)

if __name__ == '__main__':
    main(sys.argv[1:])
