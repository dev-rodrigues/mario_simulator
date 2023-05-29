import sys

import pygame
from abc import ABC, abstractmethod

from domain.entities.neural_network import NeuralNetwork
from domain.entities.pipe import Pipe
from domain.valueble.commons import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE


class JumpMario(ABC):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Jump Mario")
        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()
        self.speed = 5  # Velocidade inicial
        self.max_speed = 12  # Velocidade máxima
        self.last_speed_increase = 0
        self.pipe_interval = 2500  # Intervalo entre a criação de novos Pipes
        self.last_pipe_time = pygame.time.get_ticks()

    def increase_speed(self, elapsed_time):
        if elapsed_time - self.last_speed_increase >= 60:
            if self.speed <= self.max_speed:
                self.speed += 1
                self.last_speed_increase = elapsed_time

    def delete_genome_on_file(self):
        file = open("genome.txt", "w")
        file.write("")
        file.close()

    def exist_genome_on_file(self):
        try:
            file = open("genome.txt", "r")
            file.close()
            return True
        except IOError:
            return False

    def write_genome_on_file(self, mario):
        file = open("genome.txt", "w")

        for gene in mario.genome:
            file.write(str(gene) + "\n")

        file.write(str(mario.genomeOutput))

        file.close()

    def update_genome(self, mario):
        if not self.exist_genome_on_file():
            self.write_genome_on_file(mario)
        else:
            self.delete_genome_on_file()
            self.write_genome_on_file(mario)

    @abstractmethod
    def run(self):
        pass


class Game(JumpMario):
    def __init__(self, mario):

        super().__init__()
        self.mario = mario
        self.pipes = [Pipe.create_pipe()]

    def run(self):
        running = True
        teste = 0

        while running:
            self.clock.tick(30)

            if teste == 0:
                self.mario.jump()

            teste += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.mario.update()

            for pipe in self.pipes:
                pipe.update(self.speed)

            current_time = pygame.time.get_ticks()

            if current_time - self.last_pipe_time > self.pipe_interval:
                self.pipes.append(Pipe.create_pipe())
                self.last_pipe_time = current_time

            self.pipes = [pipe for pipe in self.pipes if pipe.x + pipe.width > 0]

            for pipe in self.pipes:
                if (
                        self.mario.x + self.mario.width > pipe.x
                        and self.mario.x < pipe.x + pipe.width
                        and self.mario.y + self.mario.height > pipe.y
                ):
                    print("Game Over")
                    running = False

            elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
            self.screen.fill((0, 0, 0))
            self.mario.draw(self.screen)

            for pipe in self.pipes:
                pipe.draw(self.screen)

            distance_to_pipe = self.pipes[0].x - (self.mario.x + self.mario.width)
            print("Distância do Mario para o Pipe:", distance_to_pipe)
            print("Altura do Pipe:", self.pipes[0].height)

            nn = NeuralNetwork(
                4,
                8,
                1,
                self.mario.genome,
                self.mario.genomeOutput,
            )

            altura = abs(self.mario.y - 550)
            saida = nn.forward([distance_to_pipe, self.speed, self.pipes[0].height, altura])[0]
            print("O valor da saida é ", saida)

            if saida <= 0.5:
                self.mario.lower()

            if saida > 0.5:
                self.mario.jump()

            self.increase_speed(elapsed_time)

            # Renderiza o texto na tela
            font = pygame.font.Font(None, 36)
            text = font.render("Tempo: {}s".format(elapsed_time), True, WHITE)
            text_rect = text.get_rect()
            text_rect.topleft = (10, 10)
            self.screen.blit(text, text_rect)

            pygame.display.flip()

        pygame.quit()


class GameSimulation(JumpMario):

    def __init__(self, marios, genetic_algorithm, generation, record):
        super().__init__()
        self.marios = marios
        self.genetic_algorithm = genetic_algorithm
        self.generation = generation
        self.record = record

    def run(self):
        pipes = [Pipe.create_pipe() for _ in range(200)]
        dead_marios = []
        running = True
        new_record = 0
        first_jump = 0

        while running:
            self.clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            distances_to_pipe = [pipe.x - (mario.x + mario.width) for mario, pipe in zip(self.marios, pipes)]

            if first_jump == 0:
                for i, mario in enumerate(self.marios):
                    mario.jump()

            first_jump = first_jump + 1

            for i, mario in enumerate(self.marios):
                mario.update()

                if self.collided(i, mario, pipes):
                    dead_marios.append(mario)
                    self.marios.pop(i)  # Remove o Mario que colidiu do array

                    if len(self.marios) == 0:
                        running = False
                        pygame.display.flip()
                        break

                    if self.speed == self.max_speed:
                        self.speed = 5
                else:
                    new_record += 1

                try:
                    if distances_to_pipe[i] < mario.x:
                        mario.fitness += 100
                except:
                    mario.update()
                    pass

                mario.fitness += 1

            for i, pipe in enumerate(pipes):
                pipe.update(self.speed)

            current_time = pygame.time.get_ticks()

            if current_time - self.last_pipe_time > self.pipe_interval:
                pipes.append(Pipe.create_pipe())
                self.last_pipe_time = current_time

            # if len(pipes) == 0:
            #     pipes = [Pipe.create_pipe() for _ in range(100)]

            pipes = [pipe for pipe in pipes if pipe.x + pipe.width > 0]

            if len(pipes) == 0:
                pipes = [Pipe.create_pipe() for _ in range(200)]

            elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
            self.screen.fill((0, 0, 0))

            for pipe in pipes:
                pipe.draw(self.screen)

            for i, mario in enumerate(self.marios):
                mario.draw(self.screen)

                nn = NeuralNetwork(4, 8, 1, mario.genome, mario.genomeOutput)

                try:
                    output = nn.forward([
                        abs(distances_to_pipe[i]),
                        self.speed,
                        pipes[i].height,
                        abs(mario.y - 550)]
                    )[0]

                    if output <= 0.5:
                        mario.lower()

                    if output > 0.5:
                        mario.jump()
                except (IndexError, ValueError):
                    pass

            self.increase_speed(elapsed_time)
            self.write_speed(self.speed, self.screen)
            self.write_generation(self.generation, self.screen)
            self.score(new_record, self.screen)
            self.write_record(self.record, self.screen)
            # self.updated_record(new_record, self.record, elapsed_time)

            font = pygame.font.Font(None, 36)
            text = font.render("Time: {}s".format(elapsed_time), True, WHITE)
            text_rect = text.get_rect()
            text_rect.topleft = (10, 10)
            self.screen.blit(text, text_rect)
            pygame.display.flip()

        pygame.quit()
        return dead_marios, new_record, self.speed

    def collided(self, i, mario, pipes):
        try:
            return mario.x + mario.width > pipes[i].x and mario.x < pipes[i].x + pipes[
                i].width and mario.y + mario.height > pipes[i].y
        except IndexError:
            return True

    def write_speed(self, speed, screen):
        font = pygame.font.Font(None, 36)
        text = font.render("Speed level: {}".format(speed), True, WHITE)
        text_rect = text.get_rect()
        text_rect.topleft = (10, 30)
        screen.blit(text, text_rect)
        pygame.display.flip()

    def write_generation(self, generation, screen):
        font = pygame.font.Font(None, 36)
        text = font.render("Generation: {}".format(generation), True, WHITE)
        text_rect = text.get_rect()
        text_rect.topleft = (10, 50)
        screen.blit(text, text_rect)
        pygame.display.flip()

    def score(self, new_record, screen):
        font = pygame.font.Font(None, 36)
        text = font.render("Score: {}".format(new_record), True, WHITE)
        text_rect = text.get_rect()
        text_rect.topleft = (10, 70)
        screen.blit(text, text_rect)
        pygame.display.flip()

    def write_record(self, record, screen):
        font = pygame.font.Font(None, 36)
        text = font.render("Record: {}".format(record), True, WHITE)
        text_rect = text.get_rect()
        text_rect.topleft = (10, 90)
        screen.blit(text, text_rect)
        pygame.display.flip()

    def updated_record(self, new_record, record, elapsed_time):
        if new_record > record:
            #print("New record: {}s".format(new_record))
            if new_record > record:
                self.record = new_record
