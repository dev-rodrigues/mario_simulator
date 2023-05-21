import random
import sys

import pygame

from domain.valueble.commons import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE
from domain.entities.neural_network import NeuralNetwork
from domain.entities.pipe import Pipe


class Game:
    def __init__(self, mario):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Jump Mario")

        self.clock = pygame.time.Clock()
        self.mario = mario
        self.pipes = [Pipe.create_pipe()]
        self.start_time = pygame.time.get_ticks()
        self.speed = 5  # Velocidade inicial
        self.last_speed_increase = 0
        self.pipe_interval = 2000  # Intervalo entre a criação de novos Pipes
        self.last_pipe_time = pygame.time.get_ticks()

    def increase_speed(self, elapsed_time):
        if elapsed_time - self.last_speed_increase >= 10:
            self.speed += 2
            self.last_speed_increase = elapsed_time
            print("Velocidade aumentada para:", self.speed)

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
                3,
                6,
                1,
                self.mario.genome,
                self.mario.genomeOutput,
            )

            saida = nn.forward([distance_to_pipe, self.speed, self.pipes[0].height])[0]
            print("O valor da saida é ", saida)
            if saida > 0.5:
                self.mario.jump()

            # aumentando a velocidade a cada 60 segundos:
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


class GameSimulation:
    def __init__(self, marios, genetic_algorithm):
        self.marios = marios
        self.genetic_algorithm = genetic_algorithm

    def run_simulation(self, generation):
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
                # print("Velocidade aumentada para:", speed)

            self.write_speed(speed, screen)
            self.write_generation(generation, screen)

            font = pygame.font.Font(None, 36)
            text = font.render("Time: {}s".format(elapsed_time), True, WHITE)
            text_rect = text.get_rect()
            text_rect.topleft = (10, 10)
            screen.blit(text, text_rect)

            pygame.display.flip()

        return dead_marios

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
