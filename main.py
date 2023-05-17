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


# [
# distanci
# velocidade
# altura
# ]

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
    def __init__(self):
        self.id = uuid.uuid4()
        self.x = 50
        self.y = SCREEN_HEIGHT - 100
        self.width = 50
        self.height = 50
        self.velocity = 0
        self.is_jumping = False
        self.distance_to_pipe = 0

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
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))


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


class GeneticAlgorithm:
    def __int__(self):
        self.marios = self.create_population()

    def create_population(self):
        for i in range(10):
            self.marios.append(Mario())

    def train(self):
        for n in range(100):
            SimulationGame(self.marios)


class SimulationGame:
    def __init__(self, marios):
        self.marios = marios


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Jump Mario")

        self.clock = pygame.time.Clock()
        self.mario = Mario()
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
                np.random.uniform(-1, 1, 3),
                np.random.uniform(-1, 1, 1),
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


if __name__ == "__main__":
    game = Game()
    game.run()
