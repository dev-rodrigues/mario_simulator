import configurations.menu
from configurations import menu
from domain.entities.game import Game
from domain.entities.genetic import GeneticAlgorithm
from domain.entities.mario import Mario

if __name__ == "__main__":
    menu.menu()
    # algorithm = GeneticAlgorithm()
    # algorithm.create_population(20)
    # best_marios = algorithm.train(algorithm, 3)
    # best_best_mairos = max(best_marios, key=lambda mario: mario.fitness) if best_marios else None
    # print("Melhor Mario:", best_best_mairos.fitness if best_best_mairos else None)
    # game = Game(Mario(best_best_mairos.genome, best_best_mairos.genomeOutput))

    # randomGenomeInput = [-0.31023617, -0.67976612, 0.77477795]
    # randomGenomeOutput = [0.9282922730091716]
    # game = Game(Mario(randomGenomeInput, randomGenomeOutput))
    # print("executando jogo a vera")
    # game.run()
