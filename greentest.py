from threading import Thread
from time import sleep


class Node():
    def __init__(self, n):
        self.name = n
        self.t = None

    def do_work(self, st):
        self.t = Thread(target=self.test_func, args=(st,))
        self.t.start()

    def test_func(self, st):
        sleep(st)
        print self.name, st, 'done'

    def is_free(self):
        if not self.t:
            return True
        else:
            return not self.t.is_alive()


def main():
    nodes = [Node('foo'), Node('bar'), Node('bob')]
    jobs = range(1, 10)
    while jobs:
        for n in nodes:
            if n.is_free():
                n.do_work(jobs.pop())
        sleep(0.5)

if __name__ == '__main__':
    main()
