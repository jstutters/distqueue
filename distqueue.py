#!/usr/bin/env python

from cluster import Cluster
from time import sleep


def main():
    cluster = Cluster()
    cluster.init_from_file('nodes.yaml')

    for n in cluster.nodes:
        n.execute('hostname; sleep 4')

    while any((n.is_busy() for n in cluster.nodes)):
        print 'waiting'
        sleep(0.5)

    for n in cluster.nodes:
        print n.last_result

if __name__ == '__main__':
    main()
