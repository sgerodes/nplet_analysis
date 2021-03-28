import math


N = 5
take_top_decisions = 0.20
min_probability = 0.55
warm_up_time = 250
deltas = []
for i in range(1, len(closing_prices)):
    deltas.append(closing_prices[i] - closing_prices[i-1])

graph = Graph(N)
graph.set_current(Graph.create_key_for_sequence(deltas[:N]))
deltas = deltas[N:]

correct = 0
incorrect = 0

len_nodes = graph.length()
top_index = len_nodes - math.ceil(len_nodes * take_top_decisions)

i = 0
# warm up
while i < warm_up_time:
    graph.trigger(deltas[i])
    i += 1
print("warmup completed", len(deltas))

# analize
while i < len(deltas)-2:
    i += 1
    if graph.get_current().get_entity().get_rising_probability() > min_probability:
        if deltas[i+1] > 0:
            correct += 1
        else:
            incorrect += 1
    elif graph.get_current().get_entity().get_falling_probability() > min_probability:
        if deltas[i+1] < 0:
            correct += 1
        else:
            incorrect += 1
    graph.trigger(deltas[i])

decisions_count = correct + incorrect
print('Taking top {} from {}'.format(len_nodes-top_index, len_nodes))
print('decisions_count={}; correct={}%; incorrect={}%'.format(decisions_count, correct/decisions_count*100, incorrect/decisions_count*100))
print('correct={}; incorrect={}'.format(correct, incorrect))
print('\n', graph)
