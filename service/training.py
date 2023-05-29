from domain.entities.genetic import GeneticAlgorithm


def train():
    population = input("Population size: ")
    generation = input("Max generations: ")
    algorithm = GeneticAlgorithm()
    algorithm.create_population(int(population))
    marios = algorithm.train(algorithm, int(generation))
    return max(marios, key=lambda mario: mario.fitness) if marios else None

