#!/usr/bin/env python3
# __main__
    # This is the main script for the dino game, with the game logic/graphics
    # being handled by game.py

#
# __outputs__
    # There are 2 Outputs:
        # jump
        # duc
        # NB: If neither condition has a confidence >= .5, then the player wil continue as usual

## TODO: Allow multiple plays - Maybe handled by game.py

#Prebuilt Libraries
import random
import math
import sys

#Helper Script
import game

c1 = 1.0
c2 = 1.0
c3 = 0.4

threshold = 3.0

class Network():

    def __init__(self, connections, neurons, outputs):
        self.connections = connections
        self.neurons = neurons + outputs
        self.outputs = outputs
        self.mutate_weight_uniform = 0.72
        self.mutate_weight_random = 0.08
        self.add_connection_rate = 0.05
        self.add_node_rate = 0.03
        self.species = self.speciate()
        self.fitness = -1
        self.adjusted_fitness = -1

    def speciate(self):
        for species in Species.species:
            if compatibility(c1,c2,c3, self, species.representative, threshold):
                species.population.append(self)
                return species
        else:
            return Species([self])

    def activate(self):
        for neuron in self.neurons:
            neuron.activate()

        confidence = 0
        output = None

        for neuron in self.outputs:
            if neuron.output > confidence:
                confidence = neuron.output
                output = neuron

        if confidence >= .5:
            return output

        else:
            return None

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
                neuron_1),
                random.absolute(-1,1)
            ))

    def mutate_connection_edit(self):
        if random.random() <= self.mutate_weight_uniform:
            random_add = random.absolute(-1, 1)
            connection = random.choice(self.connections)
            connection.weight += random_add
        elif random.random() <= self.mutate_weight_random:
            connection = random.choice(self.connections)
            connection.weight = random.absolute(-1, 1)

    def mutate_node_add(self):
        min_layer = 0
        max_layer = 0

        for neuron in self.neurons:
            if neuron.layer.index < min_layer:
                min_layer = neuron.layer.index
            elif neuron.layer.index < max_layer:
                max_layer = neuron.layer.index

        layer_index = random.randint(min_layer+1, max_layer-1)
        layer = Layer.layers[layer_index]

        connections = []

        for connection in self.connections:
            if connection.neurons[0] == layer_index-1 and connection.neurons[1] == layer_index+1:
                connection.append(connection)

        split_connection = random.choice(connections)



        new_neuron = Neuron(
            split_connection.neurons[1].inputs,
            layer
        )

        self.neurons.append(new_neuron)

        self.connections[self.connections.index(split_connection.neurons[0])].activated = False

        self.connections.append(Connection(
            (split_connection.neurons[0],
            new_neuron,
            layer
        )))

        self.connnections.append(Connection(
            (new_neuron,
            split_connection.neurons[1]),
            split_connection.weight
        ))

    def adjusted_fitness(self):
        return self.fitness / len(self.species.population)

    def speciate(self):
        for species in Species.species:
            if compatibility(c1, c2, c3, self, species.representative, threshold):
                species.add(self)
                return None
        Species.species.append(Species([self]))


class Neuron():

    def __init__(self, inputs, layer, output=None, md="Hidden"):
        self.inputs = inputs #Dict: {Neuron: Weight}
        self.output = output
        self.layer = layer
        layer.neurons.append(self) #Add self to list of neurons in layer
        self.md = md #Determine if output neuron later

    def activate(self):

        if self.output:
            return self.output

        weighted_input = 0
        for input in self.inputs:
            weighted_input += input.out * self.inputs[input]
        self.output = max(0, weighted_input)


class Connection():

    gin = {}

    def __init__(self, neurons, weight):
        self.neurons = neurons
        self.activated = True
        self.weight = weight

        if self.neurons in Connection.gin:
            self.gin = Connection.gin[self.neurons]
        else:
            Connection.gin[self.neurons] = max(list(Connection.gin.values()))+1

class Species():

    species = []

    def __init__(self, population):
        self.population = population
        self.representative = random.choice(self.population)
        Species.species.append(self)

    def fitness(self):
        fitnesses = game.play(self.population)
        for network in self.population:
            network.fitness = fitnesses[network]

    def add(self, new_network):
        self.population.append(new_network)

class Layer():

    layers = []

    def __init__(self, index, neurons):
        self.index = index
        self.neurons = neurons
        Layer.layers.append(self)

def compatibility(c1, c2, c3, network1, network2, threshold):
    neurons_larger = max(len(network1.neurons), len(network2.neurons))

    excess = (max(len(network1.connections), len(network2.connections)) -
              min(len(network1.connections), len(network2.connections)))

    weight_diff_matching = []
    disjoint = 0

    for i in range(min(len(network1.connections), len(network2.connections))):
        if network1.connections[i].gin == network2.connections[i].gin:
            weight_diff_matching.append(abs(
                network1.connections[i].gin - network2.connections[i].gin
            ))

        else:
            disjoint += 1
    try:
        avg_w_diff = sum(weight_diff_matching) / len(weight_diff_matching)
    except ZeroDivisionError:
        avg_w_diff = sum(weight_diff_matching)

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

    for i in range(len(larger_network.connections)):
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
        network_1.outputs
    )

def create_population(size, inputs, input_layer, n_outputs, bias):

    population = []

    output_layer = Layer(
        float('inf'),
        []
    ) #Generate output layer - +Inf so all behind it

    for i in range(size):
        outputs = []
        md = [
            "jump",
            "duck"
        ] #

        for i in range(n_outputs):
            outputs.append(Neuron(
                {},
                output_layer,
                md=md[0]
            )) #Create outputs

            md.remove(md[0])

        population.append(Network(
            [],
            inputs + [bias],
            outputs
        )) #Create empty network with only outputs and inputs

    return population

def rank(in_dict): #Ranks a dict by key - [Highest, ..., Lowest]
    sorted_out = {}
    in_keys = list(in_dict.keys())
    in_vals = list(in_dict.values())
    sorted_vals = sorted(in_vals)[::-1]
    while len(in_dict) != len(sorted_out):
        for val in sorted_vals:
            for key in in_keys:
                if in_dict[key] == val:
                    sorted_out[key] = val
    return dict(sorted_out)

def main():

    #Create input layer - Neurons added in Neuron.__init__
    input_layer = Layer(
        0,
        []
    )

    #Bias Neuron Generation
    bias = Neuron(
        [],
        input_layer,
        output=1,
        md="Bias"
    )

    #Generation of inputs
    inputs = []
    for i in range(7):
        inputs.append(Neuron(
            [],
            input_layer,
            md="input"
        ))

    population = create_population(50, inputs, input_layer, 2, bias)

    for species in Species.species:
        species.fitness()

    while True:
        pop_scored = {}
        for network in population:
            pop_scored[network] = network.fitness

        ranked = rank(pop_scored)
        print("The top score was", list(ranked.values())[0])
        population = []

        ranked = list(ranked.keys())

        for net in ranked[:5]: #Keep the top 5 from curr population
            population.append(net)
            ranked.remove(net) #Remove so not used in XOver

        for i in range(0, len(ranked)-1, 2):
            population.append(crossover(ranked[i], ranked[i+1]))

        for i in range(49 - len(population)): #Mutate enough to fill population to 50
            if random.random() <= .5: #Select random number, if <= .5 chance to mutate connection
                if random.random() <= .5: #Do same thing, if <= .5 chance to add connection
                    ranked[random.randint(0, len(ranked)-1)].mutate_connection_add()
                else: #Else chance to mutate connection
                    ranked[random.randint(0, len(ranked)-1)].mutate_connection_edit()
            else: #Otherwise chance to add neuron
                ranked[random.randint(0, len(ranked)-1)].mutate_node_add()

        population.append(ranked[-1]) #Keep lowest-performing network to prevent local maximum

if __name__ == "__main__":
    main()