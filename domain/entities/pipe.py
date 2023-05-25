import pygame
import random

from domain.valueble.commons import SCREEN_HEIGHT, GREEN, SCREEN_WIDTH


class Pipe:
    def __init__(self, height, x):
        self.x = x
        self.width = 50
        self.height = height
        self.y = SCREEN_HEIGHT - self.height

    def update(self, speed):
        self.x -= speed

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, (self.x, self.y, self.width, self.height))

    @staticmethod
    def create_pipe():
        height = random.randint(15, 30)  # Altura aleatória entre 15 e 30
        x = SCREEN_WIDTH
        return Pipe(height, x)
