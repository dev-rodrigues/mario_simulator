import uuid

import numpy as np
import pygame
import sys
import random

# Definindo as dimensões da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Definindo as cores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)


class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size, w1, w2):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        # Inicialização dos pesos
        self.W1 = w1  # np.random.randn(self.input_size, self.hidden_size)
        self.W2 = w2  # np.random.randn(self.hidden_size, self.output_size)

    def forward(self, x):
        # Cálculo da camada oculta
        self.hidden_layer = np.dot(x, self.W1)
        self.hidden_activation = self.sigmoid(self.hidden_layer)

        # Cálculo da camada de saída
        output_layer = np.dot(self.hidden_activation, self.W2)
        output_activation = self.sigmoid(output_layer)

        return output_activation

    def relu(self, x):
        return max(0, x)

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))


class Mario:
    def __init__(self, genome, genomeOutput):
        self.id = uuid.uuid4()
        self.x = 50
        self.y = SCREEN_HEIGHT - 100
        self.width = 50
        self.height = 50
        self.velocity = 0
        self.is_jumping = False
        self.distance_to_pipe = 0
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.genome = genome
        self.genomeOutput = genomeOutput
        self.fitness = 0

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.velocity = -15

    def update(self):
        if self.is_jumping:
            self.velocity += 1
            self.y += self.velocity
            if self.y >= SCREEN_HEIGHT - self.height:
                self.y = SCREEN_HEIGHT - self.height
                self.is_jumping = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))


class Pipe:
    def __init__(self, height, x):
        self.x = x
        self.width = 50
        self.height = height
        self.y = SCREEN_HEIGHT - self.height

    def update(self, speed):
        self.x -= speed

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))

    @staticmethod
    def create_pipe():
        height = random.randint(15, 30)  # Altura aleatória entre 15 e 30
        x = SCREEN_WIDTH
        return Pipe(height, x)


class Game:
    def __init__(self, mario):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Jump Mario")

        self.clock = pygame.time.Clock()
        self.mario = mario
        self.pipe = Pipe.create_pipe()
        self.start_time = pygame.time.get_ticks()
        self.speed = 5  # Velocidade inicial
        self.last_speed_increase = 0

    def increase_speed(self, elapsed_time):
        if elapsed_time - self.last_speed_increase >= 10:
            self.speed += 2
            self.last_speed_increase = elapsed_time
            print("Velocidade aumentada para:", self.speed)

    def run(self):
        running = True

        while running:
            self.clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.mario.jump()

            self.mario.update()
            self.pipe.update(self.speed)

            if self.pipe.x + self.pipe.width < 0:
                self.pipe = Pipe.create_pipe()

            if self.mario.x + self.mario.width > self.pipe.x and \
                    self.mario.x < self.pipe.x + self.pipe.width and \
                    self.mario.y + self.mario.height > self.pipe.y:
                print("Game Over")
                running = False

            elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
            self.screen.fill((0, 0, 0))
            self.mario.draw(self.screen)
            self.pipe.draw(self.screen)

            # Calcula a distância a partir da parte frontal do Pipe
            distance_to_pipe = self.pipe.x - (self.mario.x + self.mario.width)
            print("Distância do Mario para o Pipe:", distance_to_pipe)
            print("Altura do Pipe:", self.pipe.height)

            nn = NeuralNetwork(
                3,
                6,
                1,
                self.mario.genome,
                self.mario.genomeOutput,
            )

            saida = nn.forward([distance_to_pipe, self.speed, self.pipe.height])[0]
            print("O valor da saida é ", saida)
            if saida > 0.5:
                self.mario.jump()

            """
                aumentando a velocidade a cada 60 segundos:
            """
            self.increase_speed(elapsed_time)

            # Renderiza o texto na tela
            font = pygame.font.Font(None, 36)
            text = font.render("Tempo: {}s".format(elapsed_time), True, WHITE)
            text_rect = text.get_rect()
            text_rect.topleft = (10, 10)
            self.screen.blit(text, text_rect)

            pygame.display.flip()

        pygame.quit()
        sys.exit()


class SimulationGame:
    def __init__(self, marios, genetic_algorithm):
        self.marios = marios
        self.genetic_algorithm = genetic_algorithm

    def run_simulation(self):
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Jump Mario")

        clock = pygame.time.Clock()
        pipes = [Pipe.create_pipe() for _ in range(len(self.marios))]
        start_time = pygame.time.get_ticks()
        speed = 5  # Velocidade inicial
        last_speed_increase = 0
        max_speed = 20
        dead_marios = []

        running = True
        teste = 0

        while running:
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            distances_to_pipe = [pipe.x - (mario.x + mario.width) for mario, pipe in zip(self.marios, pipes)]

            if teste == 0:
                for i, mario in enumerate(self.marios):
                    mario.jump()

            teste = teste + 1

            for i, mario in enumerate(self.marios):
                mario.update()
                if mario.x + mario.width > pipes[i].x and mario.x < pipes[i].x + pipes[
                    i].width and mario.y + mario.height > pipes[i].y:
                    dead_marios.append(mario)
                    self.marios.pop(i)  # Remove o Mario que colidiu do array

                    if len(self.marios) == 0:
                        running = False

                if distances_to_pipe[i] < mario.x:
                    mario.fitness += 100

                mario.fitness += 1

            for i, pipe in enumerate(pipes):
                pipe.update(speed)
                if pipe.x + pipe.width < 0:
                    pipes[i] = Pipe.create_pipe()

            elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
            screen.fill((0, 0, 0))
            for mario in self.marios:
                mario.draw(screen)

            for pipe in pipes:
                pipe.draw(screen)

            for i, mario in enumerate(self.marios):
                genome = mario.genome

                nn = NeuralNetwork(3, 6, 1, genome, mario.genomeOutput)
                output = nn.forward([distances_to_pipe[i], speed, pipes[i].height])[0]

                if output > 0.5:
                    mario.jump()

            if elapsed_time - last_speed_increase >= 10 and speed < max_speed:
                speed += 2
                last_speed_increase = elapsed_time
                print("Velocidade aumentada para:", speed)

            font = pygame.font.Font(None, 36)
            text = font.render("Tempo: {}s".format(elapsed_time), True, WHITE)
            text_rect = text.get_rect()
            text_rect.topleft = (10, 10)
            screen.blit(text, text_rect)

            pygame.display.flip()

        # pygame.quit()
        # sys.exit()
        return dead_marios


class GeneticAlgorithm:
    def __init__(self):
        self.marios = []
        self.crossover_count = 0

    def create_population(self, population_size):
        for _ in range(population_size):
            genome = np.random.uniform(-1, 1, 3)  # criação aleatória de genoma
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
        print("Cruzamento número:", self.crossover_count)
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
        generation = 0
        the_best_marios = []

        while generation < max_generations:
            simulation = SimulationGame(self.marios, genetic_algorithm)
            dead_marios = simulation.run_simulation()
            self.marios = dead_marios

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

                if child is not None and random.random() < 0.1:  # 10% de chance de mutação
                    self.mutate(child)

                new_generation.append(child)

            self.marios = new_generation
            generation += 1
            print("Geração:", generation)

        return the_best_marios


if __name__ == "__main__":
    algorithm = GeneticAlgorithm()
    algorithm.create_population(5)
    best_marios = algorithm.train(algorithm, 1000)
    print("Melhores Marios:", best_marios)
    best_best_mairos = max(best_marios, key=lambda mario: mario.fitness) if best_marios else None

    game = Game(Mario(best_best_mairos.genome, best_best_mairos.genomeOutput))
    print("executando jogo a vera")
    game.run()
