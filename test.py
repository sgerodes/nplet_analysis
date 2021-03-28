from graph import *



def craete_key():
    print(Graph.create_key_for_sequence([1,2,-1,-32]))


def run_graph():
    N = 2
    graph = Graph(N)
    graph.set_current("00")
    print(graph)
    graph.trigger(123)
    print (graph)
    graph.trigger(-123)
    print (graph)
    graph.trigger(-23)
    print (graph)



if __name__ == '__main__':
    craete_key()