from domain.entities.game import Game
from domain.entities.genetic import GeneticAlgorithm
from domain.entities.mario import Mario

if __name__ == "__main__":
    # algorithm = GeneticAlgorithm()
    # algorithm.create_population(5)
    # best_marios = algorithm.train(algorithm, 3)
    # best_best_mairos = max(best_marios, key=lambda mario: mario.fitness) if best_marios else None

    # game = Game(Mario(best_best_mairos.genome, best_best_mairos.genomeOutput))
    randomGenomeInput = [0.5, 0.5, 0.5]
    randomGenomeOutput = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    game = Game(Mario(randomGenomeInput, randomGenomeOutput))
    print("executando jogo a vera")
    game.run()
