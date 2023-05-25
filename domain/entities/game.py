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
        self.last_speed_increase = 0
        self.max_speed = 12
        self.pipe_interval = 2500  # Intervalo entre a criação de novos Pipes
        self.last_pipe_time = pygame.time.get_ticks()

    def increase_speed(self, elapsed_time):
        if elapsed_time - self.last_speed_increase >= 10:
            self.speed += 2
            self.last_speed_increase = elapsed_time

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
                3,
                6,
                1,
                self.mario.genome,
                self.mario.genomeOutput,
            )

            saida = nn.forward([distance_to_pipe, self.speed, self.pipes[0].height])[0]
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

    def __init__(self, marios, genetic_algorithm, generation):
        super().__init__()
        self.marios = marios
        self.genetic_algorithm = genetic_algorithm
        self.generation = generation

    def run(self):
        pipes = [Pipe.create_pipe() for _ in range(len(self.marios))]
        dead_marios = []
        running = True
        teste = 0

        while running:
            self.clock.tick(30)

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

                if self.collided(i, mario, pipes):
                    dead_marios.append(mario)
                    self.marios.pop(i)  # Remove o Mario que colidiu do array

                    if len(self.marios) == 0:
                        running = False

                try:
                    if distances_to_pipe[i] < mario.x:
                        mario.fitness += 100
                except:
                    pass

                mario.fitness += 1

            for i, pipe in enumerate(pipes):
                pipe.update(self.speed)

            current_time = pygame.time.get_ticks()

            if current_time - self.last_pipe_time > self.pipe_interval:
                pipes.append(Pipe.create_pipe())
                self.last_pipe_time = current_time

            pipes = [pipe for pipe in pipes if pipe.x + pipe.width > 0]

            elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
            self.screen.fill((0, 0, 0))
            # for mario in self.marios:
            #     mario.draw(screen)

            for pipe in pipes:
                pipe.draw(self.screen)

            for i, mario in enumerate(self.marios):
                mario.draw(self.screen)

                nn = NeuralNetwork(3, 6, 1, mario.genome, mario.genomeOutput)

                try:
                    output = nn.forward([distances_to_pipe[i], self.speed, pipes[i].height])[0]
                    if output <= 0.5:
                        mario.lower()

                    if output > 0.5:
                        mario.jump()
                except (IndexError, ValueError):
                    pass

            if elapsed_time - self.last_speed_increase >= 10 and self.speed < self.max_speed:
                self.speed += 2
                self.last_speed_increase = elapsed_time

            self.write_speed(self.speed, self.screen)
            self.write_generation(self.generation, self.screen)

            font = pygame.font.Font(None, 36)
            text = font.render("Time: {}s".format(elapsed_time), True, WHITE)
            text_rect = text.get_rect()
            text_rect.topleft = (10, 10)
            self.screen.blit(text, text_rect)

            pygame.display.flip()

        pygame.quit()
        return dead_marios

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
