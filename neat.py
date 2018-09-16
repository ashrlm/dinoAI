"""
__main__
    This is the main script for the dino game, with the game logic/graphics
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

    def __init__(self, connections, neurons, n_outputs):
        self.connections = connections
        self.neurons = neurons
        self.output_neurons = neurons[-n_outputs:]
        self.weight_mutate_weight = 0.8
        self.add_connection_rate = 0.05
        self.add_node_rate = 0.03
        self.fitness = self.fitness()
        self.adjusted_fitness = -1

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

    def mutate_connection_add(self):
        if random.random() < self.add_connection_rate:

            avaliable_neurons = self.neurons

            neuron_0 = self.neurons[0]
            neuron_1 = self.neurons[1]

            while neuron_0.layer != neuron_1.layer:

                neuron_0 = avalable_neurons[random.randint(0, len(avalable_neurons) - 1)]
                avaliable_neurons.remove(neuron_0)

                neuron_1 = avalable_neurons[random.randint(0, len(avalable_neurons) - 1)]
                avaliable_neurons.remove(neuron_1)

            self.connections.append(Connection(
                (neuron_0,
                neuron_1)
            ))
        
        def mutate_connection_edit(self):
            if random.random < self.mutate_connection_edit:
                mutated = random.choice(self.connections)
                mutated.weight = random.absolute(-1, 1)
        
        def mutate_node_add(self):
            pass
        
        def adjusted_fitness(self):
            return self.fitness / len(self.species.population)
        
        def speciate(self):
            for species in Species.species:
                if compatibility(self, species.representative):
                    species.add(self)
                    return None
            Species.species.append(Species(self))
            

class Neuron():

    gin = {}

    def __init__(self, inputs, layer, output=None):
        self.inputs = inputs #Dict: {Neuron: Weight}
        self.output = output
        self.layer = layer

    def activate(self):
        weighted_input = 0
        for input in self.inputs:
            weighted_input += input.out * self.inputs[input]
        self.output = max(0, weighted_input)

class Connection():

    gin = {}

    def __init__(self, neurons):
        self.neurons = neurons
        self.activated = True
        self.weight = random.absolute(-1, 1)

        if self.neurons in Connection.gin:
            self.gin = Connection.gin[self.neurons]
        else:
            Connection.gin[self.neurons] = max(list(Connection.gin.values()))+1

class Species():

    species = []

    def __init__(self, population):
        self.population = population
        self.representative = random.choice(self.population)
        
    def add(self, new_network):
        self.population.append(new_network)
        
def compatibility(c1, c2, c3, network1, network2, threshold):
    neurons_larger = max(len(network_1.neurons), len(network_2.neurons))

    excess = (max(len(network_1.connections), len(network_2.connections)) -
              min(len(network_1.connections), len(network_2.connections)))

    weight_diff_matching = []
    disjoint = 0

    for i in range(min(len(network_1.connections), len(network_2.connections))):
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
    
def crossover(network_1, network_2):
    fitter_net = None
    if network_1.fitness > network_2.fitness:
        fitter_net = network_1
    elif network_2.fitness > network_1.fitness:
        fitter_net = network_2
    
    larger_network = network_1
    
    if len(network_1.connections) < len(network_2.connections):
        larger_network = network_2
    
    new_connections = []
    new_neurons = []
    
    for i in range(len(larger_network.connections)
        try:
            if network_1.connections[i].gil == network_2.connections[i].gil:
                new_connections.append(
                    random.choice(
                        network_1.connections[i], 
                        network_2.connections[i]
                    )
                )
            else:
                new_connections.append(fitter_net.connections[i])
                        
        except IndexError:
            if larger_network == fitter_net:
                new_connections.append(larger_network.connections[i])
    
    for connection in new_connections:
        if connection.neurons[0] not in new_neurons:
            new_neurons.append(connection.nuerons[0])
        if connection.neurons[1] not in new_neurons:
            new_neurons.append(connection.neurons[1])
            
    return Network(
        new_connections,
        new_neurons,
        network_1.n_outputs
    )