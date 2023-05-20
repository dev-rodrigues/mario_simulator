from domain.game import Game
from domain.genetic import GeneticAlgorithm
from domain.mario import Mario


if __name__ == "__main__":
    algorithm = GeneticAlgorithm()
    algorithm.create_population(5)
    best_marios = algorithm.train(algorithm, 1000)
    best_best_mairos = max(best_marios, key=lambda mario: mario.fitness) if best_marios else None

    game = Game(Mario(best_best_mairos.genome, best_best_mairos.genomeOutput))
    print("executando jogo a vera")
    game.run()
