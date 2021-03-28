# Binary directed circular complete Graph. Where every node contains one nplet
from itertools import product


class AnalysisEntity:
    rising_key = "up"
    falling_key = "down"
    total_key = "total"

    def __init__(self, key):
        self.key = key
        self.forecast_count = {self.rising_key: 0., self.falling_key: 0., self.total_key: 0.}

    def trigger(self, delta):
        if delta < 0:
            self.inc_falling_count()
        else:
            self.inc_rising_count()

    def inc_rising_count(self):
        self.forecast_count[self.rising_key] += 1
        self.inc_total()

    def inc_falling_count(self):
        self.forecast_count[self.falling_key] += 1
        self.inc_total()

    def inc_total(self):
        self.forecast_count[self.total_key] += 1

    def get_rising_count(self):
        return self.forecast_count[self.rising_key]

    def get_falling_count(self):
        return self.forecast_count[self.falling_key]

    def get_triggered(self):
        return self.forecast_count[self.total_key]

    def get_rising_probability(self):
        return self.get_rising_count() / self.get_triggered() if self.get_triggered() > 0 else 0

    def get_falling_probability(self):
        return self.get_falling_count() / self.get_triggered() if self.get_triggered() > 0 else 0

    def get_key(self):
        return self.key

    def __repr__(self):
        return 'AnalysisEntity(key={}; forecast_count={})'.format(self.get_key(), self.forecast_count)


class BiDirectionalNode:
    rising_key = 1
    falling_key = 0

    def __init__(self, entity):
        self.entity = entity
        self.accessors = {}

    def set_rising_accessor(self, node):
        self.accessors[self.rising_key] = node

    def set_falling_accessor(self, node):
        self.accessors[self.falling_key] = node

    def get_rising_accessor(self):
        return self.accessors[self.rising_key]

    def get_falling_accessor(self):
        return self.accessors[self.falling_key]

    def get_entity(self):
        return self.entity

    def __repr__(self):
        return 'BiDirectionalNode(entity={})'.format(self.get_entity())


class Graph:
    rising_key = "1"
    falling_key = "0"

    def __init__(self, N):
        self.N = N
        self.nodes = {}
        self._initialize_graph()
        self.current = None
        self.triggered = 0.

    def trigger(self, delta):
        self.triggered += 1
        self.current.get_entity().trigger(delta)
        if delta < 0:
            self.move_falling()
        else:
            self.move_rising()

    def move_rising(self):
        self.current = self.current.get_rising_accessor()

    def move_falling(self):
        self.current = self.current.get_falling_accessor()

    def set_current(self, key):
        self.current = self.nodes[key]

    def get_current(self):
        return self.current

    def _initialize_graph(self):
        self._create_nodes()
        self._link_nodes()

    def _add_node(self, key, node):
        self.nodes[key] = node

    def _create_nodes(self):
        for nplet_key_tuple in product(Graph.rising_key + Graph.falling_key, repeat=self.N):
            key = ''.join(nplet_key_tuple)
            node = BiDirectionalNode(AnalysisEntity(key))
            self._add_node(key, node)

    def _link_nodes(self):
        for node in self.nodes.values():
            key = node.get_entity().get_key()
            node.set_rising_accessor(self.nodes[Graph.create_next_rising_key(key)])
            node.set_falling_accessor(self.nodes[Graph.create_next_falling_key(key)])

    def __repr__(self):
        return 'Graph(node_count={}; graph_triggered={} current={}\n {}\n)' \
            .format(len(self.nodes),
                    self.triggered,
                    str(self.current),
                    ';\n '.join([ '{}; frequency={}'.format(str(node),
                                                             node.get_entity().get_triggered()/self.triggered * len(self.nodes)
                                                             if node.get_entity().get_triggered() > 0 else 0) for node in self.nodes.values()]))

    def length(self):
        return len(self.nodes)

    @staticmethod
    def create_next_rising_key(prev):
        return (prev + Graph.rising_key)[1:]

    @staticmethod
    def create_next_falling_key(prev):
        return (prev + Graph.falling_key)[1:]

    @staticmethod
    def create_key_for_sequence(lst):
        return ''.join([Graph.falling_key if value < 0 else Graph.rising_key for value in lst])
