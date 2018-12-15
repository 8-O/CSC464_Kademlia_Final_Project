'''
CSC464 UVic Fall 2018

This program prepares a node for the network that other nodes can bootstrap to.

Thor Reite V00809409
12/14/2018

https://kademlia.readthedocs.io/en/latest/intro.html
'''

import logging
import asyncio
import sys

from kademlia.network import Server

def main():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    log = logging.getLogger('kademlia')
    log.addHandler(handler)
    log.setLevel(logging.DEBUG)

    server = Server()
    server.listen(1111)

    loop = asyncio.get_event_loop()
    loop.set_debug(True)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()
        loop.close()
        sys.exit(0)

if __name__ == '__main__':
    main()
