import yaml
from computenode import ComputeNode


class Cluster(object):
    def init_from_file(self, filename):
        f = file(filename, 'r')
        descriptions = yaml.load_all(f)
        self.nodes = []
        for d in descriptions:
            print d
            self.nodes.append(ComputeNode(d['hostname'], d['capabilities']))
