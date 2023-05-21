from domain.entities.genetic import GeneticAlgorithm


def train():
    population = input("Population size: ")
    generation = input("Max generations: ")
    algorithm = GeneticAlgorithm()
    algorithm.create_population(int(population))
    marios = algorithm.train(algorithm, int(generation))
    best_mario = max(marios, key=lambda mario: mario.fitness) if marios else None
    write_genome_on_file(best_mario)


def write_genome_on_file(mario):
    file = open("genome.txt", "w")
    file.write(str(mario.genome))
    file.write(str(mario.genomeOutput))
    file.close()
