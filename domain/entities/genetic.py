import random
import numpy as np
from tqdm import tqdm

from domain.entities.game import GameSimulation
from domain.entities.mario import Mario


class GeneticAlgorithm:
    def __init__(self):
        self.marios = []
        self.crossover_count = 0

    def create_population(self, population_size):
        for _ in range(population_size):
            genome = np.random.uniform(-1, 1, 4)  # criação aleatória de genoma
            genome_output = np.random.uniform(-1, 1, 1)
            mario = Mario(genome, genome_output)
            self.marios.append(mario)

    def mutate(self, mario):
        mutated_genome = mario.genome  # Implemente a lógica de mutação adequada para o seu problema
        # adicionar um valor aleatório pequeno a cada gene
        mutated_genome += np.random.uniform(-0.1, 0.1, len(mutated_genome))
        mario.genome = mutated_genome
        mario.genomeOutput += np.random.uniform(-0.1, 0.1, len(mario.genomeOutput))

    def crossover(self, parent1, parent2):
        if parent1 is None or parent2 is None:
            return None
        child_genome = np.mean([parent1.genome, parent2.genome], axis=0)  # média dos genomas dos pais
        child_genome_output = np.mean([parent1.genomeOutput, parent2.genomeOutput], axis=0)
        child = Mario(child_genome, child_genome_output)
        self.crossover_count += 1
        return child

    def select_parent(self):
        tournament_size = min(3, len(self.marios))  # Limitar o tamanho do torneio ao tamanho da população
        tournament_candidates = random.sample(self.marios, tournament_size)  # Seleciona Marios aleatoriamente

        if not tournament_candidates:  # Verifica se a lista de candidatos está vazia
            return None

        best_mario = max(tournament_candidates, key=lambda mario: mario.distance_to_pipe)
        return Mario(best_mario.genome.copy(), best_mario.genomeOutput.copy())

    def create_new_mario(self):
        parent1 = self.select_parent()
        parent2 = self.select_parent()
        child = self.crossover(parent1, parent2)
        if child is not None:
            self.mutate(child)
        return child

    def train(self, genetic_algorithm, max_generations):
        the_best_marios = []
        record = 0

        for i in tqdm(range(max_generations)):
            simulation = GameSimulation(self.marios, genetic_algorithm, i, record)
            dead_marios, record_output = simulation.run()
            self.marios = dead_marios
            record = record_output

            new_generation = []
            best_mario = max(self.marios, key=lambda mario: mario.fitness) if self.marios else None

            the_best_marios.append(best_mario)

            if best_mario:
                new_generation.append(best_mario)

            while len(new_generation) < len(self.marios):
                parent1 = None
                parent2 = None

                # Seleção dos pais
                while parent1 is None:
                    parent1 = self.select_parent()

                while parent2 is None or parent2 == parent1:
                    parent2 = self.select_parent()

                # Aplicar cruzamento para criar um filho
                child = self.crossover(parent1, parent2)

                # if child is not None and random.random() < 0.1:  # 10% de chance de mutação
                self.mutate(child)

                new_generation.append(child)

            self.marios = new_generation

        return the_best_marios
