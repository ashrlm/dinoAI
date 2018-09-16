"""
__main__
    This is the main script for the dino game, with the game logig/graphics
    being handled by game.py

__outputs__
    There are 2 Outputs:
        Jump: 0
        Duck: 1
"""

import random
import game
import math

class Network():

    def __init__(self, layers, connections, neurons, n_outputs):
        self.connections = connections
        self.neurons = neurons
        self.layers = layers
        self.output_neurons = neurons[-n_outputs:]
        self.fitness = -1
        self.mutation_rate = random.uniform(.2, .5)

    def activate(self):
        for neuron in self.neurons:
            neuron.activate

        confidence = 0
        output = None

        for neuron in self.output_neurons:
            if neuron.output > confidence:
                confidence = neuron.output
                output = neuron

        return output

    def fitness(self):
        results = game.play()
        self.fitness = results['fitness']

    def mutate_connection(self):
        if random.random() <= self.mutation_rate:

            avaliable_neurons = self.neurons

            neuron_0 = self.neurons[0]
            neuron_1 = self.neurons[1]

            while neuron_0.layer < neuron_1.layer and Connection((neuron_0, neuron_1)) not in self.connections:

                neuron_0 = avalable_neurons[random.randint(0, len(avalable_neurons) - 1)]
                avaliable_neurons.remove(neuron_0)

                neuron_1 = avalable_neurons[random.randint(0, len(avalable_neurons) - 1)]
                avaliable_neurons.remove(neuron_1)

            self.connections.append(Connection(
                (neuron_0,
                neuron_1)
            ))

class Neuron():

    gin = {}

    def __init__(self, inputs, output=None):
        self.inputs = inputs #Dict: {Neuron: Weight}
        self.output = output
        self.layer = layer

    def activate(self):
        weighted_input = 0
        for input in self.inputs:
            weighted_input += input.out * self.inputs[input]
        self.output = max(0, weighted_input)

class NeuronLayer():

    layers = {}

    def __init__(self, neurons):
        self.neurons = neurons
        self.layer_count[neurons] = max(list(count.values()))+1


class Connection():

    gin = {}

    def __init__(self, neurons):
        self.neurons = neurons
        self.activated = True
        self.weight = random.absolute(-1, 1)

        if self.neurons in Connection.gin or self.neurons[::-1] in Connection.gin:
            self.gin = Connection.gin[self.neurons]
        else:
            Connection.gin[self.neurons] = max(list(Connection.gin.values()))+1

def compatibility(c1, c2, c3, network1, network2, threshold):
    neurons_larger = max(len(network_1.neurons), len(network_2.neurons))

    excess = (max(len(network_1.connections), len(network_2.connections)) -
              min(len(network_1.connections), len(network_2.connections)))

    weight_diff_matching = []
    disjoint = 0

    for i in range(max(len(network_1.connections), len(network_2.connections))):
        if network_1.connections[i].gin == network_2.connections[i].gin:
            weight_diff_matching.append(math.abs(
                network_1.connections[i].gin - network_2.connections[i].gin
            ))

        else:
            disjoint += 1

    avg_w_diff = sum(weight_diff_matching) / len(weight_diff_matching)

    compatibility = (
        ((c1 * excess) / neurons_larger) +
        ((c2 * disjoint) / neurons_larger) +
        (c3 * avg_w_diff)
    )

    if compatibility <= threshold:
        return True
    return False